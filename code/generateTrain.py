"""
Generate candida training data 

For each white/black image
Pad to 640x640
Find contours
Generate bounding boxes
Output yolo annotations format
"""
#from cmath import inf
#import pandas as pd
from pyexpat.errors import XML_ERROR_INCOMPLETE_PE
import cv2
import matplotlib.pyplot as plt
import numpy as np
#import math
#import imutils
#import statistics as st
#import time
#from scipy.spatial.distance import cdist
#import matplotlib.animation as animation
import os
import shutil

filePath = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\x_20220127'

filesOrig = [i for i in os.listdir(filePath) if i.endswith(".jpg")]
filesWhite = [i for i in os.listdir(filePath) if i.endswith(".tif")]

print(f'Original files: {filesOrig}')
print(f'Original files: {filesWhite}')

def generateBB(origName, white):
    whiteBin = cv2.cvtColor(white, cv2.COLOR_BGR2GRAY)
    print(whiteBin.shape)
    whiteBinHeight = whiteBin.shape[0]
    whiteBinWidth = whiteBin.shape[1]
    #whiteBin = cv2.imread(os.path.join(filePath, w), cv2.IMREAD_GRAYSCALE) # Read the white/black image
    _, binary = cv2.threshold(whiteBin, 225, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(os.path.join(filePath, "binaryImages", "binayImage_" + origName + ".jpg"), binary)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    numContours = 0

    with open(os.path.join(filePath, "data",  origName + ".txt"), 'w') as f:
        
        for c in contours:
            M = cv2.moments(c)
            x,y,w,h = cv2.boundingRect(c)
            #print("xywh", x, y, w, h)
            #print(f'BB coordinates: {x}, {y}, {w}, {h}')
            # if M['m00'] != 0:
            #     cx = int(M['m10']/M['m00'])
            #     cy = int(M['m01']/M['m00'])
            #     numContours += 1
            # else:
            #     cx, cy = 0, 0 #continue # excludes contours without area # To keep:  
             

            cv2.drawContours(white, [c], -1, (0, 255, 0), 1)
            cv2.rectangle(white,(x,y),(x+w,y+h),(255,0,0),1)
            
            clas = "0"
            xYolo = round((x+w/2)/whiteBinWidth, 4)
            yYolo = round((y+h/2)/whiteBinHeight, 4)
            wYolo = round(w/whiteBinWidth, 4)
            hYolo = round(h/whiteBinHeight, 4)

            wYolo += wYolo*0.1 # Expand yolo detections with 10%
            hYolo += hYolo*0.1
            
            
            f.write(f'{clas} {xYolo} {yYolo} {wYolo} {hYolo}\n')
        
        cv2.imwrite(os.path.join(filePath, "boxImages", "binayBoxes_" + origName + ".jpg"), white)
        print("Image saved")

    with open(os.path.join(filePath, "data", "stats.txt"), 'a') as w:
        w.write(f'{origName}, {len(contours)}\n')

    print(len(contours), numContours)
    print("Stats saved")


for i in filesOrig:
    print(i)
    fn = os.path.splitext(os.path.basename(i))[0] # Get name without extension
    shutil.copy(os.path.join(filePath, i), os.path.join(filePath, "data", fn + ".jpg"))
    for w in filesWhite:
        if w.startswith(fn):
            #imW = cv2.imread(os.path.join(filePath, w), cv2.IMREAD_GRAYSCALE) # Read the white/black image
            imW = cv2.imread(os.path.join(filePath, w)) 
            generateBB(fn, imW)
  