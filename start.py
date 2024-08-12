from flask import Flask, request, render_template, abort, jsonify, make_response
import YOLOv8_predict_api as YOLO
import ResNet50_Predict as Res
from werkzeug.utils import secure_filename
import os

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config['HOST'] = '0.0.0.0'
# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recognition.html', methods=['GET'])
def recognition():
    return render_template('recognition.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'leafImage' not in request.files:
        return abort(400, description="No file part")
    
    file = request.files['leafImage']
    
    if file.filename == '':
        return abort(400, description="No selected file")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)

        # 调用YOLOv8模型进行预测
        result = YOLO.predict(filepath)
        
        # 假设result是JSON类型的结果
        return make_response(result)


if __name__ == '__main__':
    app.run(port=8080,debug=False,host='0.0.0.0')
