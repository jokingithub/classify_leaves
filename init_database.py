from start import app, DB, LeafCategory
def init_DB():
    with app.app_context():
        DB.create_all()

def create():
    with app.app_context():
        # 清空表格中的所有数据
        DB.session.query(LeafCategory).delete()
        DB.session.commit()

        # 添加一些示例数据
        categories = [
            LeafCategory(category_name='Oak', chinese_name='xxx', description='A type of deciduous tree.'),
            LeafCategory(category_name='Maple', chinese_name='xxx', description='A tree known for its colorful leaves.'),
            # 可以添加更多类别
        ]
        
        DB.session.bulk_save_objects(categories)
        DB.session.commit()

if __name__ == '__main__':
    init_DB()
    create()