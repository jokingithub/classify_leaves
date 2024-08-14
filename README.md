# classify_leaves  
#### 本项目旨在通过深度学习模型对 176 个类别的叶子进行分类识别。该项目使用 Flask 作为 Web 框架，采用 YOLOv8 和 ResNet50 作为分类模型，并使用来自 Kaggle 竞赛的数据集进行训练和测试。 

## 项目结构

classify_leaves  
 |__model    #模型的权重文件  
 | |__best.pt #YOLO训练中效果最好的权重  
 | |__last.pt #YOLO训练中最终的权重  
 | |__ResNet50_model.pth  #ResNet模型文件  
 | |__ResNet_labelmap.json #ResNet标签字典 
 |  
 |__instance  #数据库  
 |  
 |__static  
 | |__css    #css样式  
 | | |__style_index.css  
 | | |__recog_styles.css  
 | |_imgs   #图片资源  
 | | |__...  
 | |__js    #脚本文件  
 |   |__imgshow.js  #主界面轮播图脚本  
 |   |__model-select-btn.js #模型选择按钮脚本  
 |  
 |__templates    #模板  
 |  |__index.html   #主页  
 |  |__recognition.html #预测页面  
 |  
 |__prepossess   #预处理函数  
 | |__divide.py  #将数据集划分为训练集和测试集  
 | |__convert_to_yolo.py  #将原数据集转换为适合YOLO的数据集  
 |  
 |__test  #测试  
 | |_ test.jpg  
 |  
 |__uplodas  #上传的图片  
 | |__update.jpg  
 |  
 |__train  
 | |__yolo_train.py #YOLO训练函数  
 | |__ResNet_train.ipynb # ResNet训练函数  
 |  
 |__init_database.py # 数据库初始化与加载函数  
 |  
 |__requirements.txt  
 |  
 |__YOLOv8_predict_api.py    #YOLO预测函数  
 |  
 |__ResNet50_Predict.py  #ResNet50预测函数  
 |  
 |__start.py #启动函数  
 |  
 |__start__all.py #数据库初始化与框架启动函数  
 |  
 |__README.md  

## 框架:  
    Flask  
  
## 模型与数据集
- **YOLOv8**: 用于实时目标检测的模型。
- **ResNet50**: 用于图像分类的深度残差网络模型。
- **数据集**: 使用 Kaggle 的 [叶子分类竞赛数据集](https://www.kaggle.com/c/classify-leaves)，该数据集包含 176 个类别的叶子图像，共有 18,353 张训练图像和 8,800 张测试图像。
  
## 环境搭建与安装
 ### Windows 系统
```bash
conda create -n cl python=3.8
conda activate cl
pip install -r requirements.txt
```

### Linux 系统
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 项目运行
 ### Windows 系统
```bash
python start_all.py
```

### Linux 系统
```bash
python3 ./start_all.py
```

## 目录说明:
instance: 数据库。
model: 存储训练好的模型权重文件。  
static: 包含静态资源，如 CSS 样式文件。  
templates: 存储 HTML 模板文件。  
prepossess: 数据预处理相关的 Python 脚本。  
test: 测试图像文件夹。  
train: 模型训练函数。  
uploads: 用户上传图像的存储目录。  
requirements.txt: 项目依赖的 Python 库列表。  
YOLOv8_predict_api.py: YOLOv8 模型的预测接口。  
ResNet50_Predict.py: ResNet50 模型的预测接口。  
init_database.py: 项目数据库初始化。
start.py: 项目的启动脚本。  
start_all.py: 项目的启动脚本(包含数据库初始化和启动Flask框架)。 
  
## 数据集来源
该项目的数据集来源于 Kaggle 竞赛树叶分类。任务是预测叶子图像的类别。数据集包含 176 个类别、18353 张训练图像、8800 张测试图像。评估指标为分类准确度。

## 贡献
jokinmail@163.com  
eligahwsw@163.com

## 许可
本项目遵循 MIT 许可协议。详细信息请参阅 LICENSE 文件。
