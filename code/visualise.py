import cv2
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd


# Load data
# scores = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\scores.txt'
# resolutions = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\petripixels\petriPixels.txt'
# objects = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\objects.txt'

# scores = pd.read_csv(scores)
# resolutions = pd.read_csv(resolutions)
# objects = pd.read_csv(objects)

# print(scores)
# print(resolutions)
# # Merge
# x = scores.merge(resolutions, how = 'inner')
# x = x.merge(objects, how = 'inner')

# x['f1'] = 2*((x['precision']*x['recall'])/(x['precision']+x['recall']))


# d = {"A":1,
#     "B":2,
#     "C":3,
#     "D":4}

# group = x['image'].str[:1]
# group = [d[k] for k in group]

# x['id'] = group
# print(x)
# # Plot
# #f = plt.figure()    
# f, axes = plt.subplots(nrows = 3, ncols = 1, sharex=True)

# axes[0].scatter(x['petriPixels'], x['precision'], s = x['objects'], c = x['id'])


# # for i, txt in enumerate(x['id']):
# #     axes[0].annotate(x['image'], (x['petriPixels'], x['precision']))

# axes[1].scatter(x['petriPixels'], x['recall'], s = x['objects'], c = x['id'], facecolor = None)
# axes[2].scatter(x['petriPixels'], x['f1'], s = x['objects'], c = x['id'])


# annotations=x['image'].tolist()
# print(annotations)
# print("hello")

# for i, label in enumerate(annotations):
#     plt.annotate(label, (x['petriPixels'][i], x['objects'][i]))



# plt.show()


# ###
# f, axes = plt.subplots(nrows = 3, ncols = 1, sharex=True)

# axes[0].scatter(x['objects'], x['precision'], c = x['id'])
# axes[1].scatter(x['objects'], x['recall'], c = x['id'], facecolor = None)
# axes[2].scatter(x['objects'], x['f1'], c = x['id'])


# annotations=x['image'].tolist()
# print(annotations)
# print("hello")

# for i, label in enumerate(annotations):
#     plt.annotate(label, (x['petriPixels'][i], x['objects'][i]))



# plt.show()
























