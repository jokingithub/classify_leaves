from flask import Flask, request, render_template, abort, jsonify, make_response
import YOLOv8_predict_api as YOLO
import ResNet50_Predict as Res
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config['HOST'] = '0.0.0.0'

# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    model = request.form.get('model', 'YOLO')  # 默认模型为 YOLO

    if file.filename == '':
        return abort(400, description="No selected file")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]  # 使用 UUID 创建唯一文件名
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 确保上传文件夹存在
        file.save(filepath)

        try:
            # 根据选择的模型进行预测
            if model == 'YOLO':
                result = YOLO.predict(filepath)
            elif model == 'ResNet':
                result = Res.predict(filepath)
            else:
                return abort(400, description="不支持的模型类型")
            
            # 假设result是JSON类型的结果
            return jsonify(result)
        except Exception as e:
            return abort(500, description=f"模型预测失败: {str(e)}")
    
    return abort(400, description="不支持的文件类型")

if __name__ == '__main__':
    app.run(port=8080, debug=False, host='0.0.0.0')
