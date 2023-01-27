from cmath import inf
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import imutils
import statistics as st
import time
from scipy.spatial.distance import cdist
import matplotlib.animation as animation

pathDat = r'data\2nd sending - photos F. candida test ends\A34.1\Results_A34.1.csv'
dat = pd.read_csv(pathDat, sep=';')

xs = dat['X'].tolist()
ys = dat['Y'].tolist()
xysearch = list(zip(xs, ys))
ptsSearch = np.array(xysearch)


# import cv2
origImg = r'data\2nd sending - photos F. candida test ends\A34.1\A34.1.jpg' 
pathImg = r'data\2nd sending - photos F. candida test ends\A34.1\A34.1_ed1.tif' 
whiteImg = r'data\2nd sending - photos F. candida test ends\A34.1\A34.1_ed2.tif'

orim = cv2.imread(origImg)
im = cv2.imread(pathImg, cv2.IMREAD_GRAYSCALE)
imW = cv2.imread(whiteImg)

# Find contours of the b&w image
_, binary = cv2.threshold(im, 225, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Find centroids of the contours
conx = []
cony = []

for c in contours:
    M = cv2.moments(c)
    x,y,w,h = cv2.boundingRect(c)
    
    print(f'BB coordinates: {x}, {y}, {w}, {h}')

    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        conx.append(cx)
        cony.append(cy)
        cv2.drawContours(orim, [c], -1, (0, 255, 0), 2)
        cv2.rectangle(orim,(x,y),(x+w,y+h),(255,0,0),2)
        #cv2.circle(orim, (cx, cy), 4, (0, 0, 255), -1)
        #cv2.putText(im, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    #print(f"x: {cx} y: {cy}")

for c in contours:
    M = cv2.moments(c)

    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        conx.append(cx)
        cony.append(cy)
        cv2.drawContours(imW, [c], -1, (0, 255, 0), 2)
        cv2.circle(imW, (cx, cy), 4, (0, 0, 255), -1)
        #cv2.putText(im, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    #print(f"x: {cx} y: {cy}")


cv2.imwrite("Contours&Centroids_Orig_BB.png", orim)
cv2.imwrite("Contours&Centroids_BW_BB.png", imW)

# Find coordinates of 
xyref = list(zip(conx, cony))
ptsRef = np.array(xyref)


#Before referencing
# plt.scatter(ptsRef[:, 0], ptsRef[:, 1], marker="x", color="red", s=2)
# plt.scatter(ptsSearch[:, 0], ptsSearch[:, 1], marker="x", color="blue", s=2)
# plt.show()


def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)

def closest_node(node, nodes):
    pt = []
    dist = inf
    for i, n in enumerate(nodes):
        if distance(node, n) <= dist:
            dist = distance(node, n)
            pt = n
            ind = i
    #print(f'Index of closest node: {ind}')
    return ind


def avDist(ptsSearch, ptsRef, xlist):
        avdist = []
        for i, v in enumerate(xlist):
            p = closest_node(ptsSearch[i], ptsRef)
            d = round(math.dist(ptsSearch[i], ptsRef[p]), 3)
            avdist.append(d)
    
        avdist = round(st.fmean(avdist), 3)
        return avdist


def getFact(mid, step):
    r = np.arange(mid - 3 * step, mid + 3 * step, step)
    r = [round(i, 3) for i in r if i > 0]
    print(r)

    return r

def adjustCoord(ptsSearch, ptsRef):
    mul = 25
    factors = getFact(50, mul)
    figN = 0

    pd = avDist(ptsSearch, ptsRef, xs)
    print(f'First average distance: {pd}')
    std = inf

    
    # plt.xlim((0,3000))
    # plt.ylim((3209, 0))
    # plt.imshow(orim)
    # plt.scatter(ptsRef[:, 0], ptsRef[:, 1], marker="x", color="red", s=2)
    # plt.scatter(ptsSearch[:, 0], ptsSearch[:, 1], marker="x", color="blue", s=2)
    # plt.savefig(f'b_{figN}.png')
    figN += 1

    while True:
        d = []
        for i,r in enumerate(factors):
            k = ptsSearch*r
            pd = avDist(k, ptsRef, xs)
            d.append(pd)
            print(f'Distance: {pd} with factor {r}')

            # plt.clf()
            # plt.xlim((0,3000))
            # plt.ylim((3209, 0))
            # plt.imshow(orim)
            # plt.scatter(ptsRef[:, 0], ptsRef[:, 1], marker="x", color="red", s=2)
            # plt.scatter(k[:, 0], k[:, 1], marker="x", color="blue", s=2)
            # plt.savefig(f'b_{figN}.png')
            figN += 1

        minDistInd = d.index(min(d))
        print("MIN", minDistInd)
        print(factors[minDistInd])
        std = st.pstdev(factors)




        if std < 0.002: # 0.002
            print(f'Factor {factors[minDistInd]} gives {min(d)}.')
            break
        else:
            mul = mul * 0.2
            factors = getFact(factors[minDistInd], mul)
            print(f'Standard dev of factor: {st.pstdev(factors)}')


adjustCoord(ptsSearch, ptsRef)


# ptsSearch1 = ptsSearch
# plt.scatter(ptsRef[:, 0], ptsRef[:, 1], marker="x", color="red", s=2)
# plt.scatter(ptsSearch1[:, 0], ptsSearch1[:, 1], marker="x", color="blue", s=2)
# plt.show()

# ptsSearch2 = ptsSearch * 20.126953125
# plt.scatter(ptsRef[:, 0], ptsRef[:, 1], marker="x", color="red", s=2)
# plt.scatter(ptsSearch2[:, 0], ptsSearch2[:, 1], marker="x", color="blue", s=2)
# plt.show()


# ptsSearch2 = ptsSearch * 20.126953125
#plt.scatter(ptsRef[:, 0], ptsRef[:, 1], marker="x", color="red", s=2)
# plt.scatter(ptsSearch2[:, 0], ptsSearch2[:, 1], marker="x", color="blue", s=2)
# plt.show()

# plt.imshow(im)
# plt.scatter(ptsSearch2[:, 0], ptsSearch2[:, 1], marker="x", color="red", s=2)
# plt.show()
