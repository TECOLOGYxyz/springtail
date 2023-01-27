
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


def yolofile_to_lists(path, file):
    with open(os.path.join(path, file)) as fd:
            freader = csv.reader(fd, delimiter='\t') 
            l = []
            for ld in freader:
                l.append([float(i) for i in ld[0].split(" ")])
            print(f'{file}: {len(l)}')
            return l


d = 0 # detections

#pathAnno = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\smallExp1280\training\test'
pathAnno = r'O:\Tech_zoo\candida\3rd sending - photos F. candida tes ends\HjalteTest\anno'
annotations = [i for i in os.listdir(pathAnno) if i.endswith('.txt')]

for det in annotations:
    db = os.path.splitext(os.path.basename(det))[0] # Get name without extension
    listDet = yolofile_to_lists(pathAnno, det)
    d += len(listDet)

print(d)


