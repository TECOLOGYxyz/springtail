


import motmetrics as mm
import pandas as pd
import os
import cv2

from shapely.geometry import Polygon
import numpy as np
import os
import csv

from tqdm import tqdm

### Detection Accuracy ###

##### DEFINE SOME VARIABLES #####
thres = 0.2


def yolo_to_poly(box):
    #YOLOv5 annotations are xc, yc, w, h (standardized to image dimensions)
    #Shapely iou calculation takes tl, tr, bl, br.

    xc, yc, w, h = box[1], box[2], box[3], box[4]

    tl = [(xc-(w/2)), (yc-(h/2))]
    tr = [(xc+(w/2)), (yc-(h/2))]
    bl = [(xc-(w/2)), (yc+(h/2))]
    br = [(xc+(w/2)), (yc+(h/2))]
    
    return [tl, tr, br, bl]


def calculate_iou(box_1, box_2):
    """
    #[[tl], [tr], [br], [bl]]
    #Note: The origin of Coordinate Systems in shapely library is left-bottom where origin in computer graphics is left-top.
    #This difference does not affect the IoU calculation, but if you do other types of calculation, this information might be helpful.
    """

    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)

    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    return iou

def findHits(annotations, detections):
    em = np.zeros((len(detections), len(annotations)), dtype=float)
    print(em.shape)
    for i1, b1 in tqdm(enumerate(detections)):
        hit = 0
        b1 = yolo_to_poly(b1)
        for i2, b2 in enumerate(annotations):
            b2 = yolo_to_poly(b2)
            iou = calculate_iou(b1,b2)
            em[i1,i2] = iou

    # Which annotations have a hit
    annoHits  = np.where(np.any(em >= thres, axis = 0))
    annoHits = np.array(annoHits).tolist()[0]
    print(annoHits)

    hitList = [1 if i in annoHits else 0 for i,k in enumerate(annotations)]
    print("Hitlist: ", hitList)

    # How many predictions overlap with a ground truth (positives)
    #p += sum(np.any(em >= thres,axis = 1))
    # How many predicitons does not overlap with a ground truth (false positives)
    #fp += sum(np.all(em < thres,axis = 1))
    # How many ground truth does not overlap with a prediction (false negatives)
    #fn += sum(np.all(em < thres,axis = 0))

    return sum(np.any(em >= thres,axis = 1)), sum(np.all(em < thres,axis = 1)), sum(np.all(em < thres,axis = 0)), hitList

def yolofile_to_lists(path, file):
    with open(os.path.join(path, file)) as fd:
            freader = csv.reader(fd, delimiter='\t') 
            l = []
            for ld in freader:
                l.append([float(i) for i in ld[0].split(" ")])
            return l


d = 0 # detections
a = 0 # annotations
cp = 0 # correct predictions
fp = 0 # false positive
fn = 0 # false negatives

#pathAnno = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\sliced\test'
pathAnno = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\data\test'
annotations = [i for i in os.listdir(pathAnno) if i.endswith('.txt')]

# Pickles:
#pathDet = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\results\1280_e705_s64\pickles'

#pathDet = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\results\1280_e705\runs\detect\1280_e705\labels'
pathDet = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\results\sliced\detectSAHI\pickles'
detections = [i for i in os.listdir(pathDet) if i.endswith('.txt')]

savePath = r'x_20230227Sliced_DEVEL_boxLevel.txt'

with open(os.path.join(savePath), 'w') as f:
    f.write(f'image,precision,recall\n')


#### RUN OVER DETECTIONS/ANNOTATIONS ####
for det in detections:
    db = os.path.splitext(os.path.basename(det))[0] # Get name without extension
    listDet = yolofile_to_lists(pathDet, det)
    d += len(listDet)
    for ann in annotations:
        if ann.startswith(db):
            listAnno = yolofile_to_lists(pathAnno, ann)
            a += len(listAnno)
            localCP, localFP, localFN, hitList = findHits(listAnno, listDet)
            cp += localCP
            fp += localFP
            fn += localFN
            print("")
            print(db)
            localPrec = localCP/(localCP+localFP)
            localRec = localCP/(localCP+localFN)
            print(f'Local precision: {localPrec}')
            print(f'Local recall: {localRec}')

            #with open(os.path.join(savePath), 'a') as w:
            #    w.write(f'{db},{localPrec},{localRec}\n')
            annoPD = pd.read_csv(os.path.join(pathAnno, ann), header = None, sep=" ")
            print(annoPD)
            annoPD['hit'] = hitList
            print(annoPD)
            annoPD.to_csv(os.path.join(pathAnno, "hitList_" + ann), index=False)


precision = cp/(cp+fp)
recall = cp/(cp+fn)

print("IOU threshold: ", thres)
print("Detections: ", d)
print("Annotations: ", a)
print("Correct detections: ", cp)
print("False positives: ", fp)
print("False negatives: ", fn)
print("Precision: ", precision)
print("Recall: ", recall)






