
import argparse
import functools
import yaml
from Soundcls.create_data import get_data_list
from Soundcls.macls.trainer import PPAClsTrainer
from Soundcls.macls.utils.utils import add_arguments, print_arguments


class cls:
    def __init__(self):

        '''parser = argparse.ArgumentParser(description=__doc__)
        add_arg = functools.partial(add_arguments, argparser=parser)
        add_arg('configs',          str,    'Soundcls/configs/ecapa_tdnn.yml',      '配置文件')
        add_arg("local_rank",       int,    0,                             '多卡训练需要的参数')
        add_arg("use_gpu",          bool,   True,                          '是否使用GPU训练')
        add_arg('augment_conf_path',str,    'Soundcls/configs/augmentation.json',   '数据增强的配置文件，为json格式')
        add_arg('save_model_path',  str,    'models/',                  '模型保存的路径')
        add_arg('resume_model',     str,    None,                       '恢复训练，当为None则不使用预训练模型')
        add_arg('pretrained_model', str,    None,                       '预训练模型的路径，当为None则不使用预训练模型')
        args = parser.parse_args()'''

        self.pretrained_model=None  #预训练模型的路径，当为None则不使用预训练模型
        self.resume_model=None  #恢复训练，当为None则不使用预训练模型
        self.save_model_path='' #模型保存的路径
        self.augment_conf_path='Soundcls/configs/augmentation.json' #数据增强的配置文件，为json格式
        self.use_gpu=True #是否使用GPU
        self.local_rank=0

        # 读取配置文件

        self.configs = {'dataset_conf': 
                        {   'batch_size': 32, 
                            'num_class': 2, 
                            'num_workers': 4, 
                            'min_duration': 0.1, 
                            'chunk_duration': 1, 
                            'do_vad': False, 
                            'sample_rate': 16000, 
                            'use_dB_normalization': True, 
                            'target_dB': -20, 
                            'train_list': 'train_list.txt', 
                            'test_list': 'test_list.txt', 
                            'label_list_path': 'label_list.txt'
                        }, 
                    'preprocess_conf': {'feature_method': 'MelSpectrogram'}, 
                    'feature_conf': {'sample_rate': 16000, 'n_fft': 1024, 'hop_length': 320, 'win_length': 1024, 'f_min': 50.0, 'f_max': 14000.0, 'n_mels': 64}, 
                    'optimizer_conf': {'learning_rate': 0.001, 'weight_decay': '1e-6'}, 
                    'model_conf': {'embd_dim': 192, 'channels': 512}, 
                    'train_conf': {'max_epoch': 30, 'log_interval': 10}, 
                    'use_model': 'ecapa_tdnn'
                }
        # 获取训练器
        self.trainer = PPAClsTrainer(configs=self.configs, use_gpu=self.use_gpu)

    def train(self):
        self.trainer.train(save_model_path=self.save_model_path,
                    resume_model=self.resume_model,
                    pretrained_model=self.pretrained_model,
                    augment_conf_path=self.augment_conf_path)

cls()
