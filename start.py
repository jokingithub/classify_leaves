from flask import Flask, request, render_template, jsonify, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import YOLOv8_predict_api as YOLO
import ResNet50_Predict as Res
from werkzeug.utils import secure_filename
import os, csv, uuid, json

# Flask应用初始化
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 数据库初始化
DB = SQLAlchemy(app)

# 定义叶子类别模型
class LeafCategory(DB.Model):
    __tablename__ = 'leaf_category'
    id = DB.Column(DB.Integer, primary_key=True)
    category_name = DB.Column(DB.String(50), unique=True, nullable=False)
    chinese_name = DB.Column(DB.String(50), nullable=False)
    description = DB.Column(DB.Text, nullable=False)

    def __repr__(self):
        return f'<LeafCategory {self.category_name}>'

# 定义反馈模型
class Feedback(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    email = DB.Column(DB.String(120), nullable=False)
    message = DB.Column(DB.Text, nullable=False)
    reg_date = DB.Column(DB.DateTime, default=DB.func.current_timestamp())

    def __repr__(self):
        return f'<Feedback {self.name}>'

# 导出反馈数据到CSV文件
def export_feedback_to_csv():
    export_path = './instance/feedback.csv'
    feedbacks = Feedback.query.all()
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Name', 'Email', 'Message', 'Date'])
        for feedback in feedbacks:
            writer.writerow([feedback.id, feedback.name, feedback.email, feedback.message, feedback.reg_date])

# 路由：导出反馈数据
@app.route('/export_feedback', methods=['GET'])
def export_feedback():
    try:
        export_feedback_to_csv()
        return send_file('./instance/feedback.csv', as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'导出反馈数据失败: {str(e)}'}), 500

# 路由：获取叶子类别列表
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = LeafCategory.query.all()
    categories_list = [
        {
            'id': category.id,
            'category_name': category.category_name,
            'chinese_name': category.chinese_name,
            'description': category.description
        }
        for category in categories
    ]
    return jsonify(categories_list)

# 路由：添加新类别
@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form['category_name']
    chinese_name = request.form['chinese_name']
    description = request.form['description']

    new_category = LeafCategory(
        category_name=category_name,
        chinese_name=chinese_name,
        description=description
    )
    try:
        DB.session.add(new_category)
        DB.session.commit()
        return redirect('/admin.html')
    except Exception as e:
        DB.session.rollback()
        return jsonify({'error': f'添加类别失败: {str(e)}'}), 500

# 路由：删除类别
@app.route('/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = LeafCategory.query.get_or_404(category_id)
    try:
        DB.session.delete(category)
        DB.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    except Exception as e:
        DB.session.rollback()
        return jsonify({'error': f'删除类别失败: {str(e)}'}), 500

# 路由：主页及静态页面
@app.route('/', methods=['GET'])
def redirected():
    return redirect('index.html')

@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/admin.html', methods=['GET'])
def admin():
    categories = LeafCategory.query.all()
    return render_template('admin.html', categories=categories)

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
        try:
            DB.session.add(feedback)
            DB.session.commit()
            return redirect('/thank_you.html')
        except Exception as e:
            DB.session.rollback()
            return jsonify({'error': f'提交反馈失败: {str(e)}'}), 500

    return render_template('contact.html')

@app.route('/thank_you.html', methods=['GET'])
def thank_you():
    return render_template('thank_you.html')

# 路由：文件上传与预测
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# 错误处理
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

# 应用入口
if __name__ == '__main__':
    with app.app_context():
        DB.create_all()
    app.run(port=8080, debug=True, host='0.0.0.0')
