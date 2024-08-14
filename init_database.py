from start import app, DB, LeafCategory
import csv

def init_DB():
    with app.app_context():
        DB.create_all()

def create():
    with app.app_context():
        # 清空表格中的所有数据
        DB.session.query(LeafCategory).delete()
        DB.session.commit()

        categories = []
        # 打开CSV文件
        with open('./instance/leaves2.0.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            
            # 读取文件的所有行
            for row in csvreader:
                # 添加一些示例数据
                categories.append(LeafCategory(category_name=row[0], chinese_name=row[1], description=row[2]))
        
        DB.session.bulk_save_objects(categories)
        DB.session.commit()


if __name__ == '__main__':
    init_DB()
    create()