import os
import shutil
import random
from tqdm import tqdm  # 导入 tqdm 以显示进度条

# 设置目录路径
classified_images_dir = "./classified_images"  # 已分类的图片目录
output_train_dir = "./train"  # 训练集输出目录
output_test_dir = "./test"  # 测试集输出目录
train_ratio = 0.8  # 训练集比例

# 创建输出目录（如果不存在）
os.makedirs(output_train_dir, exist_ok=True)
os.makedirs(output_test_dir, exist_ok=True)

# 获取所有类别标签
labels = os.listdir(classified_images_dir)

# 遍历每个标签类别
for label in tqdm(labels, desc="Processing labels"):
    label_dir = os.path.join(classified_images_dir, label)
    if not os.path.isdir(label_dir):
        continue
    
    # 获取该类别中的所有图片文件
    image_files = os.listdir(label_dir)
    
    # 打乱图片文件顺序
    random.shuffle(image_files)
    
    # 计算分割点
    split_idx = int(len(image_files) * train_ratio)
    
    # 划分训练集和测试集
    train_files = image_files[:split_idx]
    test_files = image_files[split_idx:]
    
    # 创建类别目录
    os.makedirs(os.path.join(output_train_dir, label), exist_ok=True)
    os.makedirs(os.path.join(output_test_dir, label), exist_ok=True)
    
    # 复制训练集图片
    for image_file in train_files:
        src = os.path.join(label_dir, image_file)
        dst = os.path.join(output_train_dir, label, image_file)
        shutil.copy(src, dst)
    
    # 复制测试集图片
    for image_file in test_files:
        src = os.path.join(label_dir, image_file)
        dst = os.path.join(output_test_dir, label, image_file)
        shutil.copy(src, dst)

print("[INFO] 数据集划分完成")
