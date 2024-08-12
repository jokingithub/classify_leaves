import os
import shutil
import pandas as pd
from tqdm import tqdm  # 导入 tqdm 以显示进度条

# 设置目录路径
img_dir = "./classify-leaves/images"  # 图片文件夹
csv_path = "./classify-leaves/test.csv"  # 标签CSV文件路径
output_dir = "./classified_images"  # 分类后图片存储路径

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 读取CSV文件
labels_df = pd.read_csv(csv_path, header=None, names=["filename", "label"])

# 去除文件名中的前缀 'images/'
labels_df["filename"] = labels_df["filename"].str.replace("images/", "", regex=False)


# 遍历CSV文件中的每一行
for index, row in tqdm(labels_df.iterrows(), total=labels_df.shape[0], desc="Processing images"):
    image_name = row["filename"].strip()  # 图片文件名
    label = row["label"].strip()  # 图片标签

    # 创建标签目录（如果不存在）
    label_dir = os.path.join(output_dir, label)
    os.makedirs(label_dir, exist_ok=True)

    # 源图片路径
    src_image_path = os.path.join(img_dir, image_name)
    # 目标图片路径
    dst_image_path = os.path.join(label_dir, image_name)


    # 复制图片到相应标签目录
    if os.path.exists(src_image_path):
        shutil.copy(src_image_path, dst_image_path)
    else:
        print(f"[WARNING] 图片 {src_image_path} 不存在，跳过")

print("[INFO] 图片分类完成")
