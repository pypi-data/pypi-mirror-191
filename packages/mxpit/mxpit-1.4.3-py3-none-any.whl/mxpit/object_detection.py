import os,time
import math,mxpit
import torch
import argparse
from tqdm import tqdm
from torch import optim
from torchsummary import summary
import onnx
import onnxruntime 
from onnxsim import simplify
from mxpit.FastDev.utils.tool import *
from mxpit.FastDev.utils.datasets import *
from mxpit.FastDev.utils.datase import *
from mxpit.FastDev.utils.evaluation import CocoDetectionEvaluator
from torch.utils.tensorboard import SummaryWriter
from mxpit.FastDev.module.loss import DetectorLoss
from mxpit.FastDev.module.detector import Detector

class FastestDet:
    def __init__(self,img_dirs,xml_dirs,save_path,label,batch_size, lr, epoch ,weight=None):
        msg=manage_data(img_dirs,xml_dirs)
        t=copy_file_txt(img_dirs,xml_dirs,label)
        self.save_path=save_path
        isgpu='cuda' if torch.cuda.is_available() else 'cpu'
        print('启用'+isgpu+"训练！")
        self.device = torch.device(isgpu)
        self.cfg = LoadYaml(os.path.abspath(os.path.dirname(img_dirs)),label,batch_size, lr, epoch)
        # 初始化模型结构
        if weight is not None:
            print("load weight from:%s"%weight)
            self.model = Detector(self.cfg.category_num, True).to(self.device)
            self.model.load_state_dict(torch.load(weight))
        else:
            self.model = Detector(self.cfg.category_num, False).to(self.device)

        # # 打印网络各层的张量维度
        summary(self.model, input_size=(3, self.cfg.input_height, self.cfg.input_width))

        #构建优化器
        print("use SGD optimizer")
        self.optimizer = optim.SGD(params=self.model.parameters(),
                                   lr=self.cfg.learn_rate,
                                   momentum=0.949,
                                   weight_decay=0.0005,
                                   )
        # 学习率衰减策略
        self.scheduler = optim.lr_scheduler.MultiStepLR(self.optimizer,
                                                        milestones=self.cfg.milestones,
                                                        gamma=0.1)

        # 定义损失函数
        self.loss_function = DetectorLoss(self.device)
        
        # 定义验证函数
        self.evaluation = CocoDetectionEvaluator(label, self.device)

        # 数据集加载
        val_dataset = TensorDataset(self.cfg.val_txt,self.cfg.input_width, self.cfg.input_height, False)
        train_dataset = TensorDataset(self.cfg.train_txt,self.cfg.input_width, self.cfg.input_height, True)
        #验证集
        self.val_dataloader = torch.utils.data.DataLoader(val_dataset,
                                                          batch_size=self.cfg.batch_size,
                                                          shuffle=False,
                                                          collate_fn=collate_fn,
                                                          num_workers=2,
                                                          drop_last=False,
                                                          persistent_workers=True
                                                          )
        # 训练集
        self.train_dataloader = torch.utils.data.DataLoader(train_dataset,
                                                            batch_size=self.cfg.batch_size,
                                                            shuffle=True,
                                                            collate_fn=collate_fn,
                                                            num_workers=2,
                                                            drop_last=True,
                                                            persistent_workers=True
                                                            )
    
    def train(self):
        # 迭代训练
        batch_num = 0
        print('Starting training for %g epochs...' % self.cfg.end_epoch)
        for epoch in range(self.cfg.end_epoch + 1):
            #if epoch==10:
                #res = subprocess.Popen(cmd)
            print('---Epoch:'+str(epoch)+'/'+str(self.cfg.end_epoch))
            self.model.train()
            for imgs, targets in self.train_dataloader:
                # 数据预处理
                imgs = imgs.to(self.device).float() / 255.0
                targets = targets.to(self.device)
                # 模型推理
                preds = self.model(imgs)
                # loss计算
                iou, obj, cls, total = self.loss_function(preds, targets)
                # 反向传播求解梯度
                total.backward()
                # 更新模型参数
                self.optimizer.step()
                self.optimizer.zero_grad()

                # 学习率预热
                for g in self.optimizer.param_groups:
                    warmup_num =  5 * len(self.train_dataloader)
                    if batch_num <= warmup_num:
                        scale = math.pow(batch_num/warmup_num, 4)
                        g['lr'] = self.cfg.learn_rate * scale
                    lr = g["lr"]

                # 打印相关训练信息
                info = "Epoch:%d LR:%f IOU:%f Obj:%f Cls:%f Total:%f" % (
                        epoch, lr, iou, obj, cls, total)
                batch_num += 1
            mAP05 = self.evaluation.compute_map(self.val_dataloader, self.model)
            info = "Epoch:%d LR:%f IOU:%f Obj:%f Cls:%f AP:%f Loss:%f" % (
                        epoch, lr, iou, obj, cls, mAP05 ,total)
            print(info)

            # 模型验证及保存
            if epoch % 10 == 0 and epoch > 0:
                # 模型评估
                self.model.eval()
                print("computer mAP...")
                mAP05 = self.evaluation.compute_map(self.val_dataloader, self.model)
                torch.save(self.model.state_dict(), self.save_path+"/weight_AP05_%f_%d-epoch.pth"%(mAP05, epoch))
                savepth=self.save_path+"/weight_AP05_%f_%d-epoch.pth"%(mAP05, epoch)
                save_onnx=self.save_path+"/weight_AP05_%f_%d-epoch.onnx"%(mAP05, epoch)
                self.to_onnx(savepth,save_onnx)
            if epoch==self.cfg.end_epoch:
                # 模型评估
                self.model.eval()
                print("computer mAP...")
                mAP05 = self.evaluation.compute_map(self.val_dataloader, self.model)
                torch.save(self.model.state_dict(), self.save_path+"/weight_AP05_%f_%d-epoch.pth"%(mAP05, epoch))
                savepth=self.save_path+"/weight_AP05_%f_%d-epoch.pth"%(mAP05, epoch)
                save_onnx=self.save_path+"/weight_AP05_%f_%d-epoch.onnx"%(mAP05, epoch)
                self.to_onnx(savepth,save_onnx)
            # 学习率调整
            self.scheduler.step()
        print('训练结束.')
    def to_onnx(self,savepth,saveonnx):
        # 模型加载
        print("load weight from:%s"%savepth)
        model = Detector(self.cfg.category_num, True).to(self.device)
        model.load_state_dict(torch.load(savepth, map_location=self.device))
        #sets the module in eval node
        model.eval()
        
        # 数据预处理
        img=torch.randn(1, 3, 352, 352, requires_grad=True).to(self.device)

        # 导出onnx模型
        torch.onnx.export(model,                     # model being run
                        img,                       # model input (or a tuple for multiple inputs)
                        saveonnx,       # where to save the model (can be a file or file-like object)
                        export_params=True,        # store the trained parameter weights inside the model file
                        opset_version=11,          # the ONNX version to export the model to
                        do_constant_folding=True)  # whether to execute constant folding for optimization
        # onnx-sim
        onnx_model = onnx.load(saveonnx)  # load onnx model
        model_simp, check = simplify(onnx_model)
        assert check, "Simplified ONNX model could not be validated"
        print("onnx sim sucess...")
        onnx.save(model_simp, saveonnx)  

def predict_onnx(onnx_path, img, confidence=0.65):
    session = onnxruntime.InferenceSession(onnx_path)
    input_width, input_height = 352 ,352
    img=cv2.imread(img)
    bboxes = detection(session, img, input_width, input_height, confidence)
    data=[]
    if bboxes:
        for b in bboxes:
            obj_score, cls_index = b[4], int(b[5])
            x1, y1, x2, y2 = int(b[0]), int(b[1]), int(b[2]), int(b[3])
            data.append([cls_index,obj_score,(x1,y1,x2,y2)])
        return data
    else:
        return None

# sigmoid函数
def sigmoid(x):
    return 1. / (1 + np.exp(-x))

# tanh函数
def tanh(x):
    return 2. / (1 + np.exp(-2 * x)) - 1

# 数据预处理
def preprocess(src_img, size):
    output = cv2.resize(src_img,(size[0], size[1]),interpolation=cv2.INTER_AREA)
    output = output.transpose(2,0,1)
    output = output.reshape((1, 3, size[1], size[0])) / 255
    return output.astype('float32')

# nms算法
def nms(dets, thresh=0.45):
    # dets:N*M,N是bbox的个数，M的前4位是对应的（x1,y1,x2,y2），第5位是对应的分数
    # #thresh:0.3,0.5....
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)  # 求每个bbox的面积
    order = scores.argsort()[::-1]  # 对分数进行倒排序
    keep = []  # 用来保存最后留下来的bboxx下标

    while order.size > 0:
        i = order[0]  # 无条件保留每次迭代中置信度最高的bbox
        keep.append(i)

        # 计算置信度最高的bbox和其他剩下bbox之间的交叉区域
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        # 计算置信度高的bbox和其他剩下bbox之间交叉区域的面积
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h

        # 求交叉区域的面积占两者（置信度高的bbox和其他bbox）面积和的必烈
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        # 保留ovr小于thresh的bbox，进入下一次迭代。
        inds = np.where(ovr <= thresh)[0]

        # 因为ovr中的索引不包括order[0]所以要向后移动一位
        order = order[inds + 1]
    
    output = []
    for i in keep:
        output.append(dets[i].tolist())

    return output


def detection(session, img, input_width, input_height, thresh):
    pred = []

    # 输入图像的原始宽高
    H, W, _ = img.shape

    # 数据预处理: resize, 1/255
    data = preprocess(img, [input_width, input_height])

    # 模型推理
    input_name = session.get_inputs()[0].name
    feature_map = session.run([], {input_name: data})[0][0]

    # 输出特征图转置: CHW, HWC
    feature_map = feature_map.transpose(1, 2, 0)
    # 输出特征图的宽高
    feature_map_height = feature_map.shape[0]
    feature_map_width = feature_map.shape[1]

    # 特征图后处理
    for h in range(feature_map_height):
        for w in range(feature_map_width):
            data = feature_map[h][w]

            # 解析检测框置信度
            obj_score, cls_score = data[0], data[5:].max()
            score = (obj_score ** 0.6) * (cls_score ** 0.4)

            # 阈值筛选
            if score > thresh:
                # 检测框类别
                cls_index = np.argmax(data[5:])
                # 检测框中心点偏移
                x_offset, y_offset = tanh(data[1]), tanh(data[2])
                # 检测框归一化后的宽高
                box_width, box_height = sigmoid(data[3]), sigmoid(data[4])
                # 检测框归一化后中心点
                box_cx = (w + x_offset) / feature_map_width
                box_cy = (h + y_offset) / feature_map_height
                
                # cx,cy,w,h => x1, y1, x2, y2
                x1, y1 = box_cx - 0.5 * box_width, box_cy - 0.5 * box_height
                x2, y2 = box_cx + 0.5 * box_width, box_cy + 0.5 * box_height
                x1, y1, x2, y2 = int(x1 * W), int(y1 * H), int(x2 * W), int(y2 * H)

                pred.append([x1, y1, x2, y2, score, cls_index])
    data=np.array(pred)
    if len(data)>0:
        return nms(data)
    else:
        return False
            
if __name__ == "__main__":
    img_path=r'D:\Mx_yolov3\datasets\yolo\masks\images'
    xml_path=r'D:\Mx_yolov3\datasets\yolo\masks\xml'
    save_path='.out'
    label=['Mask','Un_mask']
    batch_size=8
    lr=0.001
    epoch=100
    model = FastestDet(img_path,xml_path,save_path,label,batch_size,lr,epoch)
    model.train()