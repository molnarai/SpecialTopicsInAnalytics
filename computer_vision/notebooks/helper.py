import cv2

def load_and_scale(file_name, size = (400, 300)):
    img = cv2.imread(file_name)
    img = cv2.resize(img, size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
    
    