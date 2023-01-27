

import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np

### First look ###

pathImg = r'data\2nd sending - photos F. candida test ends\A34.1\A34.1_ed1.tif' 
pathDat = r'data\2nd sending - photos F. candida test ends\A34.1\Results_A34.1.csv'

origImg = r'data\2nd sending - photos F. candida test ends\A34.1\A34.1.jpg'

img = cv2.imread(pathImg)
origImg = cv2.imread(origImg)

dat = pd.read_csv(pathDat, sep=';')

xs = dat['X'].tolist()
#xs = [i * (3000/255) for i in xs] 
#xs = [i * (1442/71.25) for i in xs] 

ys = dat['Y'].tolist()
#ys = [i * (3209/255) for i in ys] 
#ys = [i * (1767/87.13) for i in ys] 


xy = list(zip(xs, ys))
pts = np.array(xy)
#xs = xs * int(3000/255)

plt.imshow(origImg)
plt.scatter(pts[:, 0], pts[:, 1], marker="x", color="red", s=2)
plt.show()
#plt.savefig("OrigCoord.png")

