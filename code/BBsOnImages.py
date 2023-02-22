import cv2
import os
import csv




pathImgs = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\sliced\test'
pathAnno = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\sliced/test'
pathDet = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\pickles'


imgs = [i for i in os.listdir(pathImgs) if i.endswith(".jpg")]
annotations = [i for i in os.listdir(pathAnno) if i.endswith(".txt")]
detections = [i for i in os.listdir(pathDet) if i.endswith(".txt")]

def yolofile_to_lists(path, file):
    with open(os.path.join(path, file)) as fd:
            freader = csv.reader(fd, delimiter='\t') 
            l = []
            for ld in freader:
                l.append([float(i) for i in ld[0].split(" ")])
            return l


def yolo_to_poly(box, imgWidth, imgHeight):
    """
    #YOLOv5 annotations are xc, yc, w, h (standardized to image dimensions)
    #This converts to xmin, ymin, xmax, ymax

    """
    xc, yc, w, h = int(box[1]*imgWidth), int(box[2]*imgHeight), int(box[3]*imgWidth), int(box[4]*imgHeight) # First item in list ignored skipped as this is the object class

    xmin = int(xc-(w/2))
    ymin = int(yc-(h/2))
    xmax = int(xc+(w/2))
    ymax = int(yc+(h/2))

    return [xmin, ymin, xmax, ymax]


for i in imgs:
    print("yep")
    im = cv2.imread(os.path.join(pathImgs, i))
    ib = os.path.splitext(os.path.basename(i))[0]
    
    imgWidth, imgHeight = im.shape[1], im.shape[0]

    for ann in annotations:
        if ann.startswith(ib):
            listAnno = yolofile_to_lists(pathAnno, ann)
    for det in detections:
        if det.startswith(ib):
            listDet = yolofile_to_lists(pathDet, det)


    for b in listAnno:
        col = (0, 255, 0)
        b = yolo_to_poly(b, imgWidth, imgHeight)
        cv2.rectangle(im,(b[0]-1,b[1]-1),(b[2]+1,b[3]+1),col,1)

    for b in listDet:
        col = (0, 0, 255)
        b = yolo_to_poly(b, imgWidth, imgHeight)
        cv2.rectangle(im,(b[0]-4,b[1]-4),(b[2]+4,b[3]+4),col,1)
    
    cv2.imwrite(os.path.join(pathImgs, "bb_" + ib + ".jpg"), im)