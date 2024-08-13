from flask import Flask, request, render_template, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import YOLOv8_predict_api as YOLO
import ResNet50_Predict as Res
from werkzeug.utils import secure_filename
import os
import uuid
import json

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
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['leafImage']
    model = request.form.get('model')  # 默认模型为 YOLO

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]  # 使用 UUID 创建唯一文件名
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 确保上传文件夹存在
        file.save(filepath)

        try:
            # 根据选择的模型进行预测
            if model == 'YOLO':
                res_obj = json.loads(YOLO.predict(filepath))
            elif model == 'ResNet':
                res_obj = json.loads(Res.predict(filepath))
            else:
                return jsonify({'error': '不支持的模型类型'}), 400

            print(res_obj)
            # 解析结果
            if isinstance(res_obj, list) and len(res_obj) > 0:
                res_dict = res_obj[0]
            else:
                return jsonify({'error': '预测结果格式无效'}), 400
            print(res_dict)
            # 查询类别介绍信息
            if 'name' in res_dict:
                category_name = res_dict['name']
                """
                数据库部分
                category_info = LeafCategory.query.filter_by(category_name=category_name).first()
                if category_info:
                    res_dict['chinese_name'] = category_info.chinese_name
                    res_dict['description'] = category_info.description
                else:
                    res_dict['chinese_name'] = "未定义"
                    res_dict['description'] = "没有找到该类别的描述信息"
                """
                res_dict['chinese_name'] = "未定义"
                res_dict['description'] = "没有找到该类别的描述信息"

            # 返回结果
            return jsonify(res_dict)
        except Exception as e:
            return jsonify({'error': f'模型预测失败: {str(e)}'}), 500
    
    return jsonify({'error': '不支持的文件类型'}), 400

# 错误处理器
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


if __name__ == '__main__':
    app.run(port=8080, debug=True, host='0.0.0.0')
