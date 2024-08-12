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

  

classify_leaves< br >
    |__model    #模型的权重文件< br > 
    |    |__best.pt #YOLO训练中效果最好的权重< br >
    |    |__last.pt #YOLO训练中最终的权重< br >
    |    |__ResNet50_model.pth  #ResNet模型文件< br >
    |< br >
    |__static< br >
    |     |__style_index.css    #css样式< br >
    |< br >
    |__templates    #模板< br >
    |       |__index.html   #主页< br >
    |       |__recognition.html #预测页面< br >
    |< br >
    |__prepossess   #预处理函数< br >
    |    |__divide.py  #将数据集划分为训练集和测试集< br >
    |    |__convert_to_yolo.py  #将原数据集转换为适合YOLO的数据集< br >
    |< br >
    |__test  #测试< br >
    |     |__ test.jpg< br >
    |< br >
    |__uplodas  #上传的图片< br > 
    |     |__update.jpg< br >
    |< br >
    |__requirements.txt< br >
    |< br >
    |__YOLOv8_predict_api.py    #YOLO预测函数< br >
    |< br >
    |__ResNet50_Predict.py  #ResNet50预测函数< br >
    |< br >
    |__ResNet_labelmap.json #ResNet标签字典< br >
    |< br >
    |__start.py #启动函数< br >
    |< br >
    |__README.md< br >
    
