import motmetrics as mm
import pandas as pd
import os

# """
# SAHI outputs predictions in .pickle files. Below we convert these to text files in yolov5 format.
# """

# pathPickles = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\results\1280_e705_s256\pickles'
# pickles = [os.path.join(pathPickles, i) for i in os.listdir(pathPickles)]
# factor = 1280

# for p in pickles:
#     pick = pd.read_pickle(p)
#     print(p)
#     pb = os.path.splitext(p)[0]
#     print(pb)
#     with open(os.path.join(pb + ".txt"), 'w') as f:
#         for o in pick:
#             l = vars(vars(o)['bbox'])
#             print(l)

#             xmin = l['minx']
#             ymin = l['miny']
#             xmax = l['maxx']
#             ymax = l['maxy']

#             c = 0
#             xc = ((xmin + xmax)/2)/factor
#             yc = ((ymin + ymax)/2)/factor
#             w = (xmax - xmin)/factor
#             h = (ymax - ymin)/factor
            
#             f.write(f'{c} {xc} {yc} {w} {h}\n')
            

########################################

from shapely.geometry import Polygon
import numpy as np
import os
import csv



def yolo_to_poly(box):
    #YOLOv5 annotations are xc, yc, w, h (standardized to image dimensions)
    #Shapely iou calculation takes tl, tr, bl, br.


    #xc, yc, w, h = int(box[1]*factor), int(box[2]*factor), int(box[3]*factor), int(box[4]*factor)
    xc, yc, w, h = box[1], box[2], box[3], box[4]

    tl = [(xc-(w/2)), (yc-(h/2))]
    tr = [(xc+(w/2)), (yc-(h/2))]
    bl = [(xc-(w/2)), (yc+(h/2))]
    br = [(xc+(w/2)), (yc+(h/2))]
    
    # tl = [int(box[1]*factor-(box[3]*factor/2)), int(box[2]*factor-(box[4]*factor/2))]
    # tr = [int(box[1]*factor+(box[3]*factor/2)), int(box[2]*factor+(box[4]*factor/2))]
    # bl = [int(box[1]*factor-(box[3]*factor/2)), int(box[2]*factor+(box[4]*factor/2))]
    # br = [int(box[1]*factor+(box[3]*factor/2)), int(box[2]*factor-(box[4]*factor/2))]


    return [tl, tr, br, bl]


def calculate_iou(box_1, box_2):
    """
    #[[tl], [tr], [br], [bl]]
    #Note: The origin of Coordinate Systems in shapely library is left-bottom where origin in computer graphics is left-top.
    #This difference does not affect the IoU calculation, but if you do other types of calculation, this information might be helpful.
    """

    poly_1 = Polygon(box_1)
    poly_2 = Polygon(box_2)

    # print("Box 1 area: ", poly_1.area)
    # print("Box 2 area: ", poly_2.area)
    # print("Intersection: ", poly_1.intersection(poly_2).area)
    # print("Union: ", poly_1.union(poly_2).area)

    iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
    #print("iou: ", iou)
    return iou

def findHits(annotations, detections):
    em = np.zeros((len(detections), len(annotations)), dtype=float)
    for i1, b1 in enumerate(detections):
        b1 = yolo_to_poly(b1)
        for i2, b2 in enumerate(annotations):
            b2 = yolo_to_poly(b2)
            #print(b2)
            iou = calculate_iou(b1,b2)
            #print("iou: ", iou)
            em[i1,i2] = iou
    # How many predictions overlap with a ground truth (positives)
    #p += sum(np.any(em >= thres,axis = 1))
    # How many predicitons does not overlap with a ground truth (false positives)
    #fp += sum(np.all(em < thres,axis = 1))
    # How many ground truth does not overlap with a prediction (false negatives)
    #fn += sum(np.all(em < thres,axis = 0))
    return sum(np.any(em >= thres,axis = 1)), sum(np.all(em < thres,axis = 1)), sum(np.all(em < thres,axis = 0))

def yolofile_to_lists(path, file):
    with open(os.path.join(path, file)) as fd:
            freader = csv.reader(fd, delimiter='\t') 
            l = []
            for ld in freader:
                l.append([float(i) for i in ld[0].split(" ")])
            return l


##### DEFINE SOME VARIABLES #####
factor = 1280
thres = 0.3

d = 0 # detections
a = 0 # annotations
cp = 0 # correct predictions
fp = 0 # false positive
fn = 0 # false negatives

#pathAnno = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\training\test'
pathAnno = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\HjalteTest\anno'
annotations = [i for i in os.listdir(pathAnno) if i.endswith('.txt')]

# Pickles:
#pathDet = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\results\1280_e705_s64\pickles'

#pathDet = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\results\1280_e705\runs\detect\1280_e705\labels'
pathDet = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\HjalteTest\det'
detections = [i for i in os.listdir(pathDet) if i.endswith('.txt')]


#### RUN OVER DETECTIONS/ANNOTATIONS ####
for det in detections:
    db = os.path.splitext(os.path.basename(det))[0] # Get name without extension
    listDet = yolofile_to_lists(pathDet, det)
    d += len(listDet)
    for ann in annotations:
        if ann.startswith(db):
            listAnno = yolofile_to_lists(pathAnno, ann)
            a += len(listAnno)
            localCP, localFP, localFN = findHits(listAnno, listDet)
            cp += localCP
            fp += localFP
            fn += localFN
            print("")
            print(db)
            print(f'Local precision: {localCP/(localCP+localFP)}')
            print(f'Local recall: {localCP/(localCP+localFN)}')


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

