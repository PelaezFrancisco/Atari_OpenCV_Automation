from typing import Sized
import pyautogui 
import cv2 
import numpy as np 
import importlib
import webbrowser
from Controlador.functions import *


#Video config
pyautogui.PAUSE = 0
resolution = (1920, 1080) 
codec = cv2.VideoWriter_fourcc(*"XVID") 
filename = "Recording.avi" 
fps = 20.0  
out = cv2.VideoWriter(filename, codec, fps, resolution) 

#imgs imports
b = cv2.imread("./images/bola2.png", cv2.IMREAD_GRAYSCALE)
wB, hB = b.shape[::-1]

j = cv2.imread("./images/jugador2.png", cv2.IMREAD_GRAYSCALE)
wJ, hJ = j.shape[::-1]

#window instantiate  
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL) 
cv2.resizeWindow("Frame", 500, 400)  

posJ = (0,0)
posB = (0,0)

while True: 
    
    #transform frame
    img = pyautogui.screenshot() 
    frame = np.array(img) 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    #out.write(frame) 

    #threshold to frame
    image1 = frame
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 
    ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)      
    ret2, thresh2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    #cv2.imshow('Umbralizacion-Inv', thresh1) 

    frame1 = frame
    gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    #Encuentra la bola
    resB = cv2.matchTemplate(gray_frame, b, cv2.TM_CCOEFF_NORMED)
    locB = np.where(resB >= 0.96)
    
    for pt in zip(*locB[::-1]):
        posB=pt #Capturamos la pocion en Y
        cv2.rectangle(frame1, pt, (pt[0] + wB, pt[1] + hB), (0, 255, 0), 3)

    #Encuentra al jugador
    width_cutoff = gray_frame.shape[1] // 2
    left1 = gray_frame[:, :width_cutoff]
    resJ = cv2.matchTemplate(left1, j, cv2.TM_CCOEFF_NORMED)
    locJ = np.where(resJ >= 0.9)

    for pt in zip(*locJ[::-1]):
        posJ=pt #Capturamos la pocion en Y
        cv2.rectangle(frame1, pt, (pt[0] + wJ, pt[1] + hJ), (0, 0, 255), 3)
    
    #Si la bola esta mas arriba, este sube
    pyautogui.PAUSE = 0.12
    if (posB != (0,0)): #4Check cuanod inicializa
        if(posB[1]!=posJ[1]):   #Check para saber si las posciones son distintas
            #Si la bola esta arriba esta sube
            if(posB[1]>(posJ[1]-3)):
                #print('presiona Down')
                pyautogui.keyDown("down")
                pyautogui.keyUp("down")
            #Si la bola esta mas abajo, este baja
            if(posB[1]<(posJ[1]+3)):
                #print('presiona UP')
                pyautogui.keyDown("up")
                pyautogui.keyUp("up")
        
    
    cv2.imshow("Frame", frame1)

    if cv2.waitKey(1) == ord('q'): 
        break 
out.release() 
  
cv2.destroyAllWindows()
