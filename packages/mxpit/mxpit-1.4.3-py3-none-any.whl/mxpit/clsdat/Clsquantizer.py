# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint:disable=redefined-outer-name,logging-format-interpolation
'''
parser = argparse.ArgumentParser(
        description="Googlenet fine-tune examples for image classification tasks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--model_path',
        type=str,
        default='model_Acc_0.86905.onnx',
        help="Pre-trained model on onnx file"
    )
    parser.add_argument(
        '--dataset_location',
        type=str,
        default=r"D:\Mx-yolov3_EN_3.0.0\datasets\MobileNet\car_dog",
        help="Imagenet data path"
    )
    parser.add_argument(
        '--benchmark',
        action='store_true', \
        default=False
    )
    parser.add_argument(
        '--tune',
        action='store_true', \
        default=True,
        help="whether quantize the model"
    )
    parser.add_argument(
        '--output_model',
        type=str,
        default="save.onnx",
        help="output model path"
    )
    parser.add_argument(
        '--mode',
        type=str,
        default="performance",
        help="benchmark mode of performance or accuracy"
    )
    parser.add_argument(
        '--quant_format',
        type=str,
        default='QDQ', 
        choices=['default', 'QDQ', 'QOperator'],
        help="quantization format"
    )
    args = parser.parse_args()
'''

import argparse
import cv2

import numpy as np
import onnx
import re
import os
from PIL import Image
import onnxruntime as ort
from sklearn.metrics import accuracy_score



class Squeeze:
    def __call__(self, sample):
        preds, labels = sample
        return np.squeeze(preds), labels
    
def _topk_shape_validate(preds, labels):
    # preds shape can be Nxclass_num or class_num(N=1 by default)
    # it's more suitable for 'Accuracy' with preds shape Nx1(or 1) output from argmax
    if isinstance(preds, int):
        preds = [preds]
        preds = np.array(preds)
    elif isinstance(preds, np.ndarray):
        preds = np.array(preds)
    elif isinstance(preds, list):
        preds = np.array(preds)
        preds = preds.reshape((-1, preds.shape[-1]))

    # consider labels just int value 1x1
    if isinstance(labels, int):
        labels = [labels]
        labels = np.array(labels)
    elif isinstance(labels, tuple):
        labels = np.array([labels])
        labels = labels.reshape((labels.shape[-1], -1))
    elif isinstance(labels, list):
        if isinstance(labels[0], int):
            labels = np.array(labels)
            labels = labels.reshape((labels.shape[0], 1))
        elif isinstance(labels[0], tuple):
            labels = np.array(labels)
            labels = labels.reshape((labels.shape[-1], -1))
        else:
            labels = np.array(labels)
    # labels most have 2 axis, 2 cases: N(or Nx1 sparse) or Nxclass_num(one-hot)
    # only support 2 dimension one-shot labels
    # or 1 dimension one-hot class_num will confuse with N

    if len(preds.shape) == 1:
        N = 1
        class_num = preds.shape[0]
        preds = preds.reshape([-1, class_num])
    elif len(preds.shape) >= 2:
        N = preds.shape[0]
        preds = preds.reshape([N, -1])
        class_num = preds.shape[1]

    label_N = labels.shape[0]
    assert label_N == N, 'labels batch size should same with preds'
    labels = labels.reshape([N, -1])
    # one-hot labels will have 2 dimension not equal 1
    if labels.shape[1] != 1:
        labels = labels.argsort()[..., -1:]
    return preds, labels

class TopK:
    def __init__(self, k=1):
        self.k = k
        self.num_correct = 0
        self.num_sample = 0

    def update(self, preds, labels, sample_weight=None):
        preds, labels = _topk_shape_validate(preds, labels)
        preds = preds.argsort()[..., -self.k:]
        if self.k == 1:
            correct = accuracy_score(preds, labels, normalize=False)
            self.num_correct += correct

        else:
            for p, l in zip(preds, labels):
                # get top-k labels with np.argpartition
                # p = np.argpartition(p, -self.k)[-self.k:]
                l = l.astype('int32')
                if l in p:
                    self.num_correct += 1

        self.num_sample += len(labels)

    def reset(self):
        self.num_correct = 0
        self.num_sample = 0

    def result(self):
        if self.num_sample == 0:
            print("Sample num during evaluation is 0.")
            return 0
        elif getattr(self, '_hvd', None) is not None:
            allgather_num_correct = sum(self._hvd.allgather_object(self.num_correct))
            allgather_num_sample = sum(self._hvd.allgather_object(self.num_sample))
            return allgather_num_correct / allgather_num_sample
        return self.num_correct / self.num_sample

class Dataloader:
    def __init__(self, dataset_location, image_list):
        self.batch_size = 1
        self.image_list = []
        self.label_list = []
        with open(image_list, 'r') as f:
            for s in f:
                image_name, label = re.split(r"\s+", s.strip())
                src = os.path.join(dataset_location, image_name)
                if not os.path.exists(src):
                    continue

                self.image_list.append(src)
                self.label_list.append(int(label))

    def __iter__(self):
        for src, label in zip(self.image_list, self.label_list):
            image=cv2.imread(src)
            image=self.preprocess(image)
            yield image, label

    def preprocess(self,image_path):
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

def eval_func(model, dataloader, metric, postprocess):
    metric.reset()
    sess = ort.InferenceSession(model.SerializeToString(), providers=ort.get_available_providers())
    ort_inputs = {}
    input_names = [i.name for i in sess.get_inputs()]
    for input_data, label in dataloader:
        output = sess.run(None, dict(zip(input_names, [input_data])))
        output, label = postprocess((output, label))
        metric.update(output, label)
    return metric.result()

def quantizer(model_path,output_model,dataset_location,benchmark=False,tune=True,mode='accuracy',quant_format='default'):
    print("Evaluating ONNXRuntime full precision accuracy and performance:")
    model = onnx.load(model_path)
    data_path = dataset_location
    label_path = os.path.join(dataset_location, 'val_list.txt')
    dataloader = Dataloader(data_path, label_path)
    top1 = TopK()
    postprocess = Squeeze()
    def eval(onnx_model):
        return eval_func(onnx_model, dataloader, top1, postprocess)

    if benchmark:
        if mode == 'performance':
            from neural_compressor.benchmark import fit
            from neural_compressor.config import BenchmarkConfig
            conf = BenchmarkConfig(warmup=10, iteration=1000, cores_per_instance=4, num_of_instance=1)
            fit(model, conf, b_dataloader=dataloader)
        elif mode == 'accuracy':
            acc_result = eval(model)
            print("Batch size = %d" % dataloader.batch_size)
            print("Accuracy: %.5f" % acc_result)
    if tune:
        from neural_compressor import quantization, PostTrainingQuantConfig
        config = PostTrainingQuantConfig(quant_format=quant_format)
 
        q_model = quantization.fit(model, config, calib_dataloader=dataloader,
			     eval_func=eval)
        q_model.save(output_model)

if __name__ == "__main__":
    quantizer('model_Acc_0.86905.onnx','save1.onnx','D:\Mx-yolov3_EN_3.0.0\datasets\MobileNet\car_dog')
    
