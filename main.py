

import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np

### First look ###

pathImg = r'data\2nd sending - photos F. candida test ends\A34.1\A34.1.jpg' 
pathDat = r'data\2nd sending - photos F. candida test ends\A34.1\Results_A34.1.csv'

img = cv2.imread(pathImg)
dat = pd.read_csv(pathDat, sep=';')

xs = dat['X'].tolist()
xs = [i * (3000/150) for i in xs] 

ys = dat['Y'].tolist()
ys = [i * (3209/150) for i in ys] 

xy = list(zip(xs, ys))
pts = np.array(xy)
xs = xs * int(3000/255)

plt.imshow(img)
plt.scatter(pts[:, 0], pts[:, 1], marker="x", color="red", s=2)
plt.show()

