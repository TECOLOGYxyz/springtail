import cv2
import math
import os
import pandas as pd
from shapely.geometry import Polygon
from PIL import Image


split_width = 640
split_height = 640


def start_points(dim, slice_size):
    ratio = dim/(slice_size)
    canfit = math.floor(ratio)
    if canfit == 0: # If dimension can't fit a single slice, use the image as is.
        return [0]
    splits = math.ceil(ratio)
    surplus = (splits-ratio)*(slice_size)
    surplusPerSlice = surplus/canfit

    # print(f'Image dimension: {dim}')
    # print(f'Slice size is {slice_size}. Without overlap slice size is {slice_size}')
    # print("Slices per dimension ", ratio)
    # print(f'We can fit {canfit} slices of size {slice_size}')
    # print(f'We will make {splits} slices')
    # print(f'We have a surplus of {surplus}')
    # print(f"That's {surplusPerSlice} per slice")

    l = []
    c = 0

    for i in range(splits):
        l.append(int(((slice_size)-surplusPerSlice)*c))
        c += 1
    return l


def slice(basename, img, imgDim, anno, xs, ys): 
    
    count = 0
    suffix = 'slice'
    frmt = 'jpg'

    # we need to rescale coordinates from 0-1 to real image height and width
    anno[['x1', 'w']] = anno[['x1', 'w']] * imgDim[0]
    anno[['y1', 'h']] = anno[['y1', 'h']] * imgDim[1]

    boxes = []

    # convert bounding boxes to shapely polygons. Invert Y and find polygon vertices from center points
    for row in anno.iterrows():
        x1 = row[1]['x1'] - (row[1]['w']/2)
        y1 = (imgDim[1] - (row[1]['y1']) - row[1]['h']/2)
        x2 = row[1]['x1'] + (row[1]['w']/2)
        y2 = (imgDim[1] - (row[1]['y1']) + row[1]['h']/2)

        boxes.append((int(row[1]['class']), Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])))
    #print("Main boxes: ", boxes)

    for i in ys:
        for j in xs:
            split = img[i:i+split_height, j:j+split_width]
            cv2.imwrite(r'C:\Users\au309263\Desktop\tempCandida\debug/slice/{}_{}_{}.{}'.format(basename, suffix, count, frmt), split)
            #print(f'Image slice _{count}_ written')
            
            xmin =  j
            ymin = imgDim[1] - i
            xmax = j + split_width
            ymax = imgDim[1] - i - split_height

            pol = Polygon([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)])

            slice_labels = []
            slice_labels_path = r'C:\Users\au309263\Desktop\tempCandida\debug/slice/{}_{}_{}.txt'.format(basename, suffix, count)
            for box in boxes:
                if pol.intersects(box[1]):
                    inter = pol.intersection(box[1])        
                    #print(f'Annotation {box[1]} intersects with slice {pol}')

                    new_box = inter.envelope # get smallest rectangular polygon (with sides parallel to the coordinate axes) that contains the intersection
                    
                    centre = new_box.centroid # get central point for the new bounding box 
                    
                    x, y = new_box.exterior.coords.xy # get coordinates of polygon vertices
                    
                    new_width = round((max(x) - min(x)) / split.shape[1], 6) #imgDim[0] # get bounding box width and height normalized to slice size
                    new_height = round((max(y) - min(y)) / split.shape[0], 6) #imgDim[1]
                    
                    new_x = round((centre.coords.xy[0][0] - xmin) / split.shape[1], 6) # Normalize center x and invert y for yolo format
                    new_y = round((ymin - centre.coords.xy[1][0]) / split.shape[0], 6)

                    #print(f'Old x {centre.coords.xy[0][0]}; New x {new_x}. Xmin was {xmin}.')
                    #print(f'Old y {centre.coords.xy[1][0]}; New y {new_y}. Ymin was {ymin}')
                    if (new_width * split.shape[1] < 1) | (new_height * split.shape[0] < 1):
                        continue
                    
                    d = new_x + (new_width/2) - 1
                    if d > 0:
                        print(slice_labels_path)
                        print("d ", d)
                        print("x before: ", new_x)
                        new_x -= d
                        new_x = round(new_x, 6)
                        print("x after: ", new_x)
                    
                    d = new_x - (new_width/2)
                    if d < 0:
                        print(slice_labels_path)
                        print("d ", d)
                        print("x before: ", new_x)
                        new_x -= d
                        new_x = round(new_x, 6)
                        print("x after: ", new_x)



                    d = new_y + (new_height/2) - 1
                    if d > 0:
                        print(slice_labels_path)
                        print("d ", d)
                        print("x before: ", new_y)
                        new_y -= d
                        new_y = round(new_y, 6)
                        print("x after: ", new_y)

                    d = new_y - (new_height/2)
                    if d < 0:
                        print(slice_labels_path)
                        print("d ", d)
                        print("x before: ", new_y)
                        new_y -= d
                        new_y = round(new_y, 6)
                        print("x after: ", new_y)


                    slice_labels.append([box[0], new_x, new_y, new_width, new_height])
            
                slice_df = pd.DataFrame(slice_labels, columns=['class', 'x1', 'y1', 'w', 'h'])
                slice_df.to_csv(slice_labels_path, sep=' ', index=False, header=False, float_format='%.6f')
            count += 1    


path = r'C:\Users\au309263\Desktop\tempCandida\debug/orig'
imgPaths = [os.path.join(path, i) for i in os.listdir(path) if i.endswith('.jpg')]

for image in imgPaths:
    basename = os.path.splitext(os.path.basename(image))[0]

    img = cv2.imread(image)
    img_h, img_w, _ = img.shape

    xs = start_points(img_w, split_width)
    ys = start_points(img_h, split_height)

    anno = pd.read_csv(os.path.join(path, basename) + ".txt", sep=' ', names=['class', 'x1', 'y1', 'w', 'h'])

    slice(basename, img, (img_w, img_h), anno, xs, ys)



