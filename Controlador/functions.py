import cv2

def cargaImg(url):
    template = cv2.imread(url, cv2.IMREAD_GRAYSCALE)
    return template