from torch.utils.data import Dataset, DataLoader
import torch
from PIL import Image
import os


def to_trainval(path,train_num=0.8):
    try:
        labels=[]
        list_file=os.listdir(path)
        for i in list_file:
            if os.path.isdir(os.path.join(path,i)):
                labels.append(i)
        f=open(os.path.join(path,'labels.txt'),'w')
        for l in labels:
            f.write(l+'\n')
        f.close()
        datas_cls=[]
        for i in range(len(labels)):
            data_cls=[]
            files=os.listdir(os.path.join(path,labels[i]))
            for f in files:
                data_cls.append(os.path.join(labels[i],f)+' '+str(i))
            datas_cls.append(data_cls)
        train_data=[]
        val_data=[]
        for i in datas_cls:
            num_list=len(i)
            num_f=int(num_list * train_num)
            train_data += i[:num_f]
            val_data += i[num_f:]
        f=open(os.path.join(path,'train_list.txt'),'w')
        for l in train_data:
            f.write(l+'\n')
        f.close()
        f=open(os.path.join(path,'val_list.txt'),'w')
        for l in val_data:
            f.write(l+'\n')
        f.close()
        return train_data,val_data,labels
    except:
        return False

class MyDataset(Dataset):
    def __init__(self, data_dir, train_val,transform=None):
        """
        Args:
            data_dir: path to image directory.
            info_csv: path to the csv file containing image indexes
                with corresponding labels.
            image_list: path to the txt file contains image names to training/validation set
            transform: optional transform to be applied on a sample.
        """
        if train_val=="train":
            data=os.path.join(data_dir,'train_list.txt')
        elif train_val=='val':
            data=os.path.join(data_dir,'val_list.txt')
        else:
            raise Exception("train_val must be 'train' or 'val'! ")
        image_data=[]
        f=open(data,'r')
        image_infos=f.readlines()
        f.close()
        f=open(os.path.join(data_dir,'labels.txt'),'r')
        label=f.readlines()
        f.close()
        self.data_dir = data_dir
        for im in image_infos:
            image_data.append(im.replace('\n','').split(' '))
        self.image_file = image_data
        label2id=[i for i in range(len(label))]
        self.label_info = dict(zip(label,label2id))
        self.transform = transform



    def __getitem__(self, index):
        """
        Args:
            index: the index of item
        Returns:
            image and its labels
        """
        lists=self.image_file[index]
        image_name = lists[0]
        label = lists[1]
        image_name = os.path.join(self.data_dir, image_name)
        image = Image.open(image_name).convert('RGB')
        if self.transform is not None:
            image = self.transform(image)
        return image, int(label)

    def __len__(self):
        return len(self.image_file)

if __name__=="__main__":
    data=MyDataset('test_set','train')
    print(data[0])
