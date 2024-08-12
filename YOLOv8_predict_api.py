from ultralytics import YOLO
import json

def clean_json(json_str):
    """去除多余的换行符和缩进"""
    return json.dumps(json.loads(json_str), separators=(',', ':'))

def predict(img, model_path='./model/last.pt', save_img=False):
    '''预测函数'''
    # 输入：图像路径，模型路径
    # 默认使用最后的权重模型
    # 如果需要保存结果图像，将 save_img 设置为 True
    # 输出结果为 JSON 格式

    # 加载模型
    model = YOLO(model_path)  # 加载自定义模型
    imgpath = img

    # 使用模型进行预测
    results = model(imgpath, save=save_img)  # 对图像进行预测

    # 将结果转换为 JSON 字符串并格式化
    if results:
        result_json = results[0].tojson()  # 处理单一结果
    else:
        result_json = '{}'

    # 清理 JSON 格式
    cleaned_result = clean_json(result_json)
    return cleaned_result

if __name__ == '__main__':
    result = predict("test/58.jpg", save_img=True)
    print(result)  # 打印紧凑格式的 JSON 字符串
