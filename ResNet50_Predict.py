import sys

import timm
from PIL import Image
import pandas as pd
import torch
import torch.nn as nn
import json
import torchvision.transforms as transforms


def preprocess_img(img_path):
    transform_test = transforms.Compose([
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    input_image = Image.open(img_path)
    input_tensor = transform_test(input_image)

    # 创建一个 batch
    input_batch = input_tensor.unsqueeze(0)  # 添加一个批次维度

    # 如果你的模型在 GPU 上，确保数据也被发送到 GPU
    input_batch_cuda = input_batch.to('cuda')
    return input_batch_cuda


def predict(model_path, img_path, labelmap_path):
    # 定义模型 加载自定义预训练权重
    model = timm.create_model('resnet50d', pretrained=False)

    # 替换最后一个全连接层  修改输出节点为176个 匹配176类叶片
    nums = model.fc.in_features  # 获取最后一层的输入特征数
    model.fc = nn.Linear(nums, 176)  # 更改输出层的大小

    model.load_state_dict(torch.load(model_path, weights_only=False,
                                      map_location=(torch.device('gpu') if torch.cuda.is_available() else torch.device('cpu'))))

    model.eval()
    model.cuda()

    with torch.no_grad():  # 确保在评估模式下不计算梯度
        x = preprocess_img(img_path)
        logit = model(x)
        top5_probabilities, top5_class_indices = torch.topk(logit.softmax(dim=1) * 100, k=5)
        pred = torch.argmax(logit, dim=1).cpu().numpy()
        pred_i = str(pred[0])
        # print(pred_i)

    with open(labelmap_path, 'r') as f:
        labelmap = json.load(f)

    value = labelmap.get(pred_i)
    if value is not None:
        prob = "{:.2f}".format(top5_probabilities[0][0])
        print(f"该叶片预测为：{value}, 准确概率为{prob}%")
    else:
        print(f"键'{pred}'不存在于字典中")


if __name__ == '__main__':
    model_path = './model/ResNet50_model.pth'
    img_path = './test/58.jpg'
    labelmap_path = './labelmap.json'

    predict(model_path, img_path, labelmap_path)
