import timm
from PIL import Image
import torch
import torch.nn as nn
import json
import torchvision.transforms as transforms

# 确定使用的设备（GPU或CPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def preprocess_img(img_path):
    # 定义图像预处理的转换操作
    transform_test = transforms.Compose([
        transforms.Resize((112, 112)),  # 调整图像大小
        transforms.ToTensor(),  # 转换为张量
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),  # 归一化
    ])
    input_image = Image.open(img_path)  # 打开图像
    input_tensor = transform_test(input_image)  # 进行转换
    input_batch = input_tensor.unsqueeze(0).to(device)  # 添加批次维度并转移到指定设备
    return input_batch

def load_labelmap(labelmap_path):
    # 加载标签映射文件
    with open(labelmap_path, 'r') as f:
        return json.load(f)

def predict(img_path, model_path='./model/ResNet50_model.pth', 
             labelmap=load_labelmap('./model/ResNet_labelmap.json'), device=device,weight_only = True):
    # 创建模型并加载预训练权重
    model = timm.create_model('resnet50d', pretrained=False)
    nums = model.fc.in_features
    model.fc = nn.Linear(nums, 176)  # 修改输出层以适应176个类别
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=False))  # 加载模型权重

    model.eval()  # 设置为评估模式
    model.to(device)  # 转移到指定设备

    with torch.no_grad():  # 在评估模式下，不计算梯度
        x = preprocess_img(img_path)  # 预处理图像
        logit = model(x)  # 前向传播获取预测结果
        top5_probabilities, top5_class_indices = torch.topk(logit.softmax(dim=1), k=5)  # 获取前5个预测
        pred = torch.argmax(logit, dim=1).cpu().numpy()  # 获取最终预测的类别
        pred_i = str(pred[0])  # 转换为字符串格式

    value = labelmap.get(pred_i)  # 从标签映射中获取标签名称
    prob = "{:.2f}".format(top5_probabilities[0][0])  # 格式化置信度
    r = {
        "name": value,
        "class": pred_i,
        "confidence": prob
    }
    return json.dumps(r)  # 返回预测结果的JSON格式


if __name__ == '__main__':
    img_path = './test/58.jpg'
    res = predict( img_path)  # 进行预测
    print(f"res: {res}")  # 打印预测结果
