# classify_leaves  
## 本程序是对176 个类别的叶子进行分类识别  

## framework:  
    Flask  
  
## model:  
    YOLOv8  ResNet50  
  
## Install：
    
    Win:
        conda create -n cl python=3.8
        conda activate cl
        pip install -r requirements.txt

    Linux:
        python3 venv -m .venv
        source .venv/bin/activate
        pip install -r requirements.txt

## run:
    
    Win:
        start.py
    
    Linux:
        python3 ./start.py

## dataset:
【Kaggle竞赛树叶分类1】https://www.kaggle.com/c/classify-leaves  
任务是预测叶子图像的类别。  
该数据集包含 176 个类别、18353 张训练图像、8800 张测试图像。每个类别至少有 50 张图像用于训练。  
测试集平均分为公共和私人排行榜。本次比赛的评估指标是分类准确度。

  

classify_leaves  
    |__model    #模型的权重文件  
    |    |__best.pt #YOLO训练中效果最好的权重  
    |    |__last.pt #YOLO训练中最终的权重  
    |    |__ResNet50_model.pth  #ResNet模型文件
    |  
    |__static  
    |     |__style_index.css    #css样式  
    |  
    |__templates    #模板  
    |       |__index.html   #主页  
    |       |__recognition.html #预测页面  
    |  
    |__prepossess   #预处理函数  
    |    |__divide.py  #将数据集划分为训练集和测试集  
    |    |__convert_to_yolo.py  #将原数据集转换为适合YOLO的数据集  
    |  
    |__test  #测试  
    |    |__ test.jpg   
    |  
    |__uplodas  #上传的图片  
    |      |__update.jpg  
    |  
    |__requirements.txt  
    |  
    |__YOLOv8_predict_api.py    #YOLO预测函数  
    |  
    |__ResNet50_Predict.py  #ResNet50预测函数  
    |  
    |__ResNet_labelmap.json #ResNet标签字典  
    |  
    |__start.py #启动函数  
    |  
    |__README.md  
    
