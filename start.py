from flask import Flask, request, render_template, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import YOLOv8_predict_api as YOLO
import ResNet50_Predict as Res
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config['HOST'] = '0.0.0.0'

# 设置数据库 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)

# 定义数据库模型
class LeafCategory(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    category_name = DB.Column(DB.String(50), unique=True, nullable=False)
    chinese_name = DB.Column(DB.String(50),nullable=False)
    description = DB.Column(DB.Text, nullable=False)

    def __repr__(self):
        return f'<LeafCategory {self.category_name}>'

# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/recognition.html', methods=['GET'])
def recognition():
    return render_template('recognition.html')

@app.route('/contact.html', methods=['GET'])
def contact():
    return render_template('contact.html')



@app.route('/upload', methods=['POST'])
def upload():
    if 'leafImage' not in request.files:
        return abort(400, description="No file part")
    
    file = request.files['leafImage']
    model = request.form.get('model')  # 默认模型为 YOLO

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
            
            # 查询类别介绍信息
            if 'name' in result:
                category_name = result['name']
                category_info = LeafCategory.query.filter_by(category_name=category_name).first()
                if category_info:
                    result['chinese_name'] = category_info.chinese_name
                    result['description'] = category_info.description

                else:
                    result['chinese_name'] = "未定义"
                    result['description'] = "没有找到该类别的描述信息"

            
            # 返回结果
            return jsonify(result)
        except Exception as e:
            return abort(500, description=f"模型预测失败: {str(e)}")
    
    return abort(400, description="不支持的文件类型")


if __name__ == '__main__':
    app.run(port=8080, debug=False, host='0.0.0.0')
