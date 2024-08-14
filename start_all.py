import init_database,start

if __name__ == '__main__':
    flag = input("[INFO]\tWould you like to initialize the database? (yes or y/no or n)\n")
    if flag == 'yes' or 'y':
        init_database.init_DB()
        init_database.create()
        print("[INFO]\tThe database has been successfully initialized!\n")
    print("[INFO]\tThe system has been successfully loaded!!\n")
    start.app.run(port=8080, debug=True, host='0.0.0.0')
    