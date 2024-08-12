from ultralytics import YOLO


def predict(img,model_path='./model./last.pt',save_img=False):
    '''Predict'''
    # input: image, model
    # default model is last weight
    # if you need the result image, set the save_img = true
    # output result json

    # Load a model
    model = YOLO(model_path)  # load a custom model
    imgpath = img
    # Predict with the model
    results = model(imgpath, save=save_img)  # predict on an image
    for result in results:
        rs = result.tojson()
    return rs


if __name__ == '__main__':
    result = predict("test/58.jpg")
    print(result)
