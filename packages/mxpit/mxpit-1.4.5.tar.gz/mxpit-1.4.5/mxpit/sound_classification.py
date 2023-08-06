
import os
from mxpit.Soundcls.create_data import get_data_list
from mxpit.Soundcls.macls.trainer import PPAClsTrainer
from mxpit.Soundcls.macls.predict import PPAClsPredictor
from mxpit.Soundcls.macls.utils.record import RecordAudio
from mxpit.Soundcls.macls.utils.utils import add_arguments, print_arguments


class cls:
    def __init__(self,data_path,save_model_path,batch_size,learning_rate=0.001,max_epoch=30,chunk_duration=3):
        self.data_path=data_path
        num=get_data_list(self.data_path,self.data_path)

        self.pretrained_model=None  #预训练模型的路径，当为None则不使用预训练模型
        self.resume_model=None  #恢复训练，当为None则不使用预训练模型
        self.save_model_path=save_model_path #模型保存的路径
        self.augment_conf_path='' #数据增强的配置文件，为json格式
        self.use_gpu=True #是否使用GPU
        self.local_rank=0

        # 读取配置文件

        self.configs = {'dataset_conf': 
                        {   'batch_size': batch_size, 
                            'num_class': num, 
                            'num_workers': 4, 
                            'min_duration': 0.1, 
                            'chunk_duration': chunk_duration, 
                            'do_vad': False, 
                            'sample_rate': 16000, 
                            'use_dB_normalization': True, 
                            'target_dB': -20, 
                            'train_list': self.data_path+'/train_list.txt', 
                            'test_list': self.data_path+'/test_list.txt', 
                            'label_list_path': self.data_path+'/label_list.txt'
                        }, 
                    'preprocess_conf': {'feature_method': 'MelSpectrogram'}, 
                    'feature_conf': {'sample_rate': 16000, 'n_fft': 1024, 'hop_length': 320, 'win_length': 1024, 'f_min': 50.0, 'f_max': 14000.0, 'n_mels': 64}, 
                    'optimizer_conf': {'learning_rate': 0.001, 'weight_decay': '1e-6'}, 
                    'model_conf': {'embd_dim': 192, 'channels': 512}, 
                    'train_conf': {'max_epoch': max_epoch, 'log_interval': 1}, 
                    'use_model': 'ecapa_tdnn'
                }
        # 获取训练器
        self.trainer = PPAClsTrainer(configs=self.configs, use_gpu=self.use_gpu)

    def train(self):
        self.trainer.train(save_model_path=self.save_model_path,
                    resume_model=self.resume_model,
                    pretrained_model=self.pretrained_model,
                    augment_conf_path='')
        print('训练结束！')

def predict(model_path,audio_path):
    use_gpu=True
    # 读取配置文件
    configs={'dataset_conf': {'batch_size': 32, 'num_class': 2, 'num_workers': 4, 'min_duration': 0.1, 'chunk_duration': 1, 'do_vad': False, 'sample_rate': 16000, 'use_dB_normalization': True, 'target_dB': -20, 'train_list': 'train_list.txt', 'test_list': 'test_list.txt', 'label_list_path': 'label_list.txt'}, 'preprocess_conf': {'feature_method': 'MelSpectrogram'}, 'feature_conf': {'sample_rate': 16000, 'n_fft': 1024, 'hop_length': 320, 'win_length': 1024, 'f_min': 50.0, 'f_max': 14000.0, 'n_mels': 64}, 'optimizer_conf': {'learning_rate': 0.001, 'weight_decay': '1e-6'}, 'model_conf': {'embd_dim': 192, 'channels': 512}, 'train_conf': {'max_epoch': 30, 'log_interval': 10}, 'use_model': 'ecapa_tdnn'}

    # 获取识别器
    predictor = PPAClsPredictor(configs=configs,
                                model_path=model_path.format(configs['use_model'],
                                                                configs['preprocess_conf']['feature_method']),
                                use_gpu=use_gpu)
    label, score = predictor.predict(audio_data=audio_path)
    return [label,score]

class Sound_pre():
    def __init__(self,model_path,record_seconds):
        self.use_gpu=True
        self.record_seconds=record_seconds
        # 读取配置文件
        self.configs={'dataset_conf': {'batch_size': 32, 'num_class': 2, 'num_workers': 4, 'min_duration': 0.1, 'chunk_duration': 1, 'do_vad': False, 'sample_rate': 16000, 'use_dB_normalization': True, 'target_dB': -20, 'train_list': 'train_list.txt', 'test_list': 'test_list.txt', 'label_list_path': 'label_list.txt'}, 'preprocess_conf': {'feature_method': 'MelSpectrogram'}, 'feature_conf': {'sample_rate': 16000, 'n_fft': 1024, 'hop_length': 320, 'win_length': 1024, 'f_min': 50.0, 'f_max': 14000.0, 'n_mels': 64}, 'optimizer_conf': {'learning_rate': 0.001, 'weight_decay': '1e-6'}, 'model_conf': {'embd_dim': 192, 'channels': 512}, 'train_conf': {'max_epoch': 30, 'log_interval': 10}, 'use_model': 'ecapa_tdnn'}
        # 获取识别器
        self.predictor = PPAClsPredictor(configs=self.configs,
                                    model_path=model_path.format(self.configs['use_model'],
                                                                    self.configs['preprocess_conf']['feature_method']),
                                    use_gpu=self.use_gpu)
        self.record_audio = RecordAudio()
    
    def predict(self):
        # 加载数据
        audio_path = self.record_audio.record(record_seconds=self.record_seconds)
        # 获取预测结果
        label, s = self.predictor.predict(audio_path)
        return [label,s]

if __name__=='__main__':
    pass
    #model=cls('D:\Mx-yolov3_EN_3.0.0\datasets\sound','',20,0.1,3)
    #model.train()

    #model_path=r'ecapa_tdnn_MelSpectrogram\best_model\model.pt'
    #audio_path=r'D:/Mx-yolov3_EN_3.0.0/datasets/sound/hello/sound1650082825 - 副本 (2).wav'
    #predict(model_path,audio_path,['hello','poll'])

    #model_path=r'ecapa_tdnn_MelSpectrogram\best_model\model.pt'
    #s=Sound_pre(model_path,['hello','poll'],0.5)
    #while 1:
        #print(s.predict())