import cv2
import numpy as np
import pyautogui
from tkinter import *

#display screen resolution, get it from OS settings
root=Tk()

#
pyautogui.KEYBOARD_KEYS

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
SCREEN_SIZE = (width, height)
#define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
#create the video write object
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (width, height))


#break with q key
while True:
    #make a screenshot
    img = pyautogui.screenshot()
    #convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    #Convert color from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #write the framew
    out.write(frame)
    #show the frame
    #cv2.imshow("screenshot",frame)
    


    if(True):
        pyautogui.keyDown("left")
        pyautogui.keyUp("left")
    

    #exit
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
out.release()