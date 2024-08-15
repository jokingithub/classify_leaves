from flask import Flask, request, render_template, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import YOLOv8_predict_api as YOLO
import ResNet50_Predict as Res
from werkzeug.utils import secure_filename
import os
import csv
import uuid
import json

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config['HOST'] = '0.0.0.0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)


class LeafCategory(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    category_name = DB.Column(DB.String(50), unique=True, nullable=False)
    chinese_name = DB.Column(DB.String(50), nullable=False)
    description = DB.Column(DB.Text, nullable=False)

    def __repr__(self):
        return f'<LeafCategory {self.category_name}>'


class Feedback(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    email = DB.Column(DB.String(120), nullable=False)
    message = DB.Column(DB.Text, nullable=False)
    reg_date = DB.Column(DB.DateTime, default=DB.func.current_timestamp())

    def __repr__(self):
        return f'<Feedback {self.name}>'


def export_feedback_to_csv():
    with app.app_context():  # 进入应用上下文
        export_path = './instance/feedback.csv'
        feedbacks = Feedback.query.all()
        with open(export_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Name', 'Email', 'Message', 'Date'])
            for feedback in feedbacks:
                writer.writerow([feedback.id, feedback.name, feedback.email, feedback.message, feedback.reg_date])


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


@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        feedback = Feedback(name=name, email=email, message=message)
        DB.session.add(feedback)
        DB.session.commit()

        return redirect('/thank_you.html')

    return render_template('contact.html')


@app.route('/thank_you.html', methods=['GET'])
def thank_you():
    return render_template('thank_you.html')


@app.route('/')
def get_redirect():
    return redirect('/index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'leafImage' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['leafImage']
    model = request.form.get('model')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        try:
            if model == 'YOLO':
                res_obj = json.loads(YOLO.predict(filepath))
            elif model == 'ResNet':
                res_obj = json.loads(Res.predict(filepath))
            else:
                return jsonify({'error': '不支持的模型类型'}), 400

            if isinstance(res_obj, list) and len(res_obj) > 0:
                res_dict = res_obj[0]
            else:
                return jsonify({'error': '预测结果格式无效'}), 400

            if 'name' in res_dict:
                category_name = res_dict['name']
                category_info = LeafCategory.query.filter_by(category_name=category_name).first()
                if category_info:
                    res_dict['chinese_name'] = category_info.chinese_name
                    res_dict['description'] = category_info.description
                else:
                    res_dict['chinese_name'] = "未定义"
                    res_dict['description'] = "没有找到该类别的描述信息"

            return jsonify(res_dict)
        except Exception as e:
            return jsonify({'error': f'模型预测失败: {str(e)}'}), 500

    return jsonify({'error': '不支持的文件类型'}), 400


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


if __name__ == '__main__':
    with app.app_context():
        DB.create_all()
    app.run(port=8080, debug=True, host='0.0.0.0')
    export_feedback_to_csv()
