from typing import Sized
import pyautogui 
import cv2 
import numpy as np 
import importlib
import webbrowser
from Controlador.functions import *


webbrowser.open(
    'https://www.retrogames.cz/play_064-Atari2600.php'
)

#Video config
resolution = (1920, 1080) 
codec = cv2.VideoWriter_fourcc(*"XVID") 
filename = "Recording.avi" 
fps = 20.0  
out = cv2.VideoWriter(filename, codec, fps, resolution) 

#imgs imports
arrNames = ["./assets/images/1.png", "./assets/images/2.png"]
arrImgs = []
arrW = []
arrH = []
for img in arrNames:
    t = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    w, h = t.shape[::-1]
    arrImgs.append(t)
    arrW.append(w)
    arrH.append(h)

v = cv2.imread("./assets/images/via.png", cv2.IMREAD_GRAYSCALE)
w, h = t.shape[::-1]

#window instantiate
cv2.namedWindow("Umbralizacion-Inv", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Umbralizacion-Inv", 500, 400)   
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Frame", 500, 400)  

while True: 
    
    #transform frame
    img = pyautogui.screenshot() 
    frame = np.array(img) 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    out.write(frame) 

    #threshold to frame
    image1 = frame
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)      
    ret2, thresh2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow('Umbralizacion-Inv', thresh1) 

    frame1 = frame
    gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    #Encuentra la via
    res = cv2.matchTemplate(gray_frame, v, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)
    for pt in zip(*loc[::-1]):
            print(pt[0])
            #print(pt[0]+50)
            if(pt[0]<920):
                print("Izquierda")
                #pyautogui.keyDown("left")
                #pyautogui.keyUp("left")
            if(pt[0]>=847 and pt[0]<910):
                print("Derecha")
                #pyautogui.keyDown("right")
                #pyautogui.keyUp("right")
            cv2.rectangle(frame1, pt, (pt[1] + h, pt[0] + (w)), (255, 0, 0), 3)

    #Encuentra Obstaculos
    for i in range(0,len(arrImgs)):
        res = cv2.matchTemplate(gray_frame, arrImgs[i], cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)
        
        for pt in zip(*loc[::-1]):
            #print(pt)
            cv2.rectangle(frame1, pt, (pt[0] + arrW[i], pt[1] + arrH[i]), (0, 255, 0), 3)
        
    cv2.imshow("Frame", frame1)



    if cv2.waitKey(1) == ord('q'): 
        break 
out.release() 
  
cv2.destroyAllWindows()
