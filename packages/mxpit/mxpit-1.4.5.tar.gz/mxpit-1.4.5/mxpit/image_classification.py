import torch,os
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import cv2
import mxpit
from mxpit.clsdat.ClsDataset import MyDataset,to_trainval
from mxpit.clsdat.Clsquantizer import quantizer
import torchvision
from torch.autograd import Variable
from collections import OrderedDict
import onnxruntime as ort
import numpy as np


class cls():
    def __init__(self,data_path,save_path,batch_size=16,lr=0.001,max_epochs=10,onnx=True):
        self.batch_size = batch_size
        # 批次的大小
        self.lr = lr
        # 优化器的学习率
        self.max_epochs = max_epochs
        self.data_path=data_path
        self.save_path=save_path
        self.onnx=onnx
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    def train(self):
        data_transform = {
            'train': transforms.Compose([
                    transforms.Resize(256),
                    transforms.RandomCrop(224),
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]),
                'val': transforms.Compose([
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]),
        }

        _,_,labels=to_trainval(self.data_path)
        print(labels)
        classifier = nn.Sequential(OrderedDict([('classifier', nn.Linear(in_features=1280, out_features=len(labels), bias=True))]))
        train_data = MyDataset(self.data_path,'train' ,transform=data_transform['train'])
        val_data = MyDataset(self.data_path,'val', transform=data_transform['val'])
        train_loader = torch.utils.data.DataLoader(train_data, batch_size=self.batch_size, num_workers=4, shuffle=True, drop_last=True)
        val_loader = torch.utils.data.DataLoader(val_data, batch_size=self.batch_size, num_workers=4, shuffle=False)
        print('训练集数量:{} 测试集数量:{}'.format(len(train_data),len(val_data)))
        weights=torch.load(os.path.dirname(mxpit.__file__).replace('\\','/')+'/clsdat/mobilenet_v2-b0353104.pth')
        model=torchvision.models.mobilenet_v2(weights=weights)
        model.classifier=classifier
        model.to(self.device)
        optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)
        criterion = nn.CrossEntropyLoss().to(self.device)
        loss_fn = nn.CrossEntropyLoss().to(self.device)
        best_acc=0
        for epoch in range(self.max_epochs):
            model.train()
            train_loss=0
            test_loss=0
            correct = 0
            for i, (images, labels) in enumerate(train_loader):
                images = Variable(images)
                labels = Variable(labels)
                images, labels = images.to(self.device), labels.to(self.device)
                optimizer.zero_grad()
                output = model(images)
                loss = criterion(output,labels)
                loss.backward()
                optimizer.step()
                train_loss += loss.item()*images.size(0)
                train_loss = train_loss/len(train_loader.dataset)
            print('Epoch: {} \tTraining Loss: {:.6f}'.format(epoch, train_loss))
            model.eval()
            for i, (images, labels) in enumerate(val_loader):
                images = Variable(images)
                labels = Variable(labels)
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = model(images)
                loss = loss_fn(outputs, labels)
                test_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum()
            test_accuracy=(correct / len(val_data))
            if test_accuracy>best_acc:
                best_model=model
                best_acc=test_accuracy
            print('Epoch: {} \tVal acc: {:.5f} \tBest_acc:{:.5f}'.format(epoch, test_accuracy,best_acc))
        torch.save(model, os.path.join(self.save_path,'model_Acc_{:.5f}.pth'.format(test_accuracy)))
        torch.save(best_model, os.path.join(self.save_path,'best_model_Acc_{:.5f}.pth'.format(best_acc)))
        if self.onnx:
            self.to_onnx(model,os.path.join(self.save_path,'model_Acc_{:.5f}.onnx'.format(test_accuracy)))
            self.to_onnx(best_model,os.path.join(self.save_path,'best_model_Acc_{:.5f}.onnx'.format(best_acc)))
            print('Strat quantization onnx')
            quantizer(os.path.join(self.save_path,'best_model_Acc_{:.5f}.onnx'.format(best_acc)),os.path.join(self.save_path,'qt_best_model_Acc_{:.5f}.onnx'.format(best_acc)),self.data_path)
            quantizer(os.path.join(self.save_path,'model_Acc_{:.5f}.onnx'.format(test_accuracy)),os.path.join(self.save_path,'qt_model_Acc_{:.5f}.onnx'.format(best_acc)),self.data_path)
        print('Train End!')
        print('Model Save : ',os.path.join(self.save_path))
        


    def to_onnx(self,model,save_path):
        model.eval()
        x = torch.randn(1, 3, 224, 224, requires_grad=True).to(self.device)
        torch.onnx.export(model,         # model being run
                    x,       # model input (or a tuple for multiple inputs) 
                    save_path,       # where to save the model
                    export_params=True,  # store the trained parameter weights inside the model file
                    opset_version=13,    # onnx opset的库版本
                    do_constant_folding=True,  # whether to execute constant folding for optimization 
                    input_names = ['input'],   # # 模型输入结点的名字，有几个输入就定义几个，如['input1','input2']
                    output_names = ['output'], #模型输出节点的名字，同样可以有多个输出
        )


def predict_pth(model_path, img):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model=torch.load(model_path).to(device)
    model.eval()
    data_transform = {
        'train': transforms.Compose([
                transforms.Resize(256),
                transforms.RandomCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
    }
	# 将输入的图像从array格式转为image
    img=cv2.imread(img)
    TURN=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img=Image.fromarray(TURN)
    # 自己定义的pytorch transform方法
    img = data_transform['train'](img)
    img = img.view(1, 3, 224, 224).to(device)
    output = model(img)
    predict = torch.softmax(output,dim=1)  # 得到概率分布
    _, prediction = torch.max(output, 1)
    #将预测结果从tensor转为array，并抽取结果
    prediction = prediction.cpu().numpy()
    return (prediction[0],predict.cpu().detach().numpy()[0].tolist())

def predict_onnx(onnx_path,img):
    img=cv2.imread(img)
    sess = ort.InferenceSession(onnx_path,providers=['CUDAExecutionProvider']) # 'CPUExecutionProvider'
    input_name = sess.get_inputs()[0].name
    output_name = [output.name for output in sess.get_outputs()]
    data=preprocess(img)
    outputs = sess.run(output_name, {input_name:data})
    return (np.argmax(outputs),softmax(outputs).tolist())

def softmax(x):
    row_max = np.max(x)
    x = x - row_max
    x_exp = np.exp(x)
    x_sum = np.sum(x_exp)
    s = x_exp / x_sum
    return s[0][0]

def preprocess(image_path):
    def resize_by_short(im, resize_size):
        short_size = min(im.shape[0], im.shape[1])
        scale = 224 / short_size
        new_w = int(round(im.shape[1] * scale))
        new_h = int(round(im.shape[0] * scale))
        return cv2.resize(im, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    def center_crop(im, crop_size):
        h, w, c = im.shape
        w_start = (w - crop_size) // 2
        h_start = (h - crop_size) // 2
        w_end = w_start + crop_size
        h_end = h_start + crop_size
        return im[h_start:h_end, w_start:w_end, :]

    def normalize(im, mean, std):
        im = im.astype("float32") / 255.0
        # to rgb
        im = im[:, :, ::-1]
        mean = np.array(mean).reshape((1, 1, 3)).astype("float32")
        std = np.array(std).reshape((1, 1, 3)).astype("float32")
        return (im - mean) / std

    # resize the short edge to `resize_size`
    im = image_path
    resized_im = resize_by_short(im, 224)
    center_im= center_crop(resized_im, 224)
    #print(center_im.shape)
    # normalize
    normalized_im = normalize(center_im, [0.485, 0.456, 0.406],
                              [0.229, 0.224, 0.225])
    # transpose to NCHW
    data = np.expand_dims(normalized_im, axis=0)
    data = np.transpose(data, (0, 3, 1, 2))

    return data

if __name__ == "__main__":
    Train_net=cls(data_path='D:\Mx-yolov3_EN_3.0.0\datasets\MobileNet\car_dog',save_path='.',batch_size=16,lr=0.001,max_epochs=5,onnx=True)
    Train_net.train()

