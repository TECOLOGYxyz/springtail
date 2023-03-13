import cv2
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


### ORIGINAL ###

# # #Load data
# scores = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\results\original\detect\x_20230227Original_scores.txt"
# resolutions = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\petripixels\petriPixels.txt'
# objects = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\objects.txt'

# scores = pd.read_csv(scores)
# resolutions = pd.read_csv(resolutions)
# objects = pd.read_csv(objects)

# # Merge
# x = scores.merge(resolutions, how = 'inner')
# x = x.merge(objects, how = 'inner')

# x['f1'] = 2*((x['precision']*x['recall'])/(x['precision']+x['recall']))

# d = {"A":1,
#     "B":2,
#     "C":3,
#     "D":4}

# groupL = x['image'].str[:1]
# group = [d[k] for k in groupL]

# x['group'] = groupL
# x['id'] = group
# print(x)
# # Plot
# #f = plt.figure()    
# f, axes = plt.subplots(nrows = 3, ncols = 1, sharex=True)

# axes[0].set_title("Standard")
# k = axes[0].scatter(x['petriPixels'], x['precision'], s = (x['objects']/9285)*10000, c = x['id'], alpha=0.6, edgecolors="black", label = x['group'])
# axes[0].set_ylabel("Precision")
# axes[0].set_ylim(0,1)
# # for i, txt in enumerate(x['id']):
# #     axes[0].annotate(x['image'], (x['petriPixels'], x['precision']))

# axes[1].scatter(x['petriPixels'], x['recall'], s = (x['objects']/9285)*10000, c = x['id'], alpha=0.6, edgecolors="black")
# axes[1].set_ylabel("Recall")
# axes[1].set_ylim(0,1)

# axes[2].scatter(x['petriPixels'], x['f1'], s = (x['objects']/9285)*10000, c = x['id'], alpha=0.6, edgecolors="black")
# axes[2].set_ylabel("F1")
# axes[2].set_ylim(0,1)
# axes[2].set_xlabel("Petri dish resolution (pixels)")


# plt.savefig("data/x_20230227/results/figures/PRF1_Standard.png", dpi=600)
# plt.show()



##### Accuracy vs pixels per object #####

#Read in hitlist

# hitPath = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\results\original\detect\annotationHits"
# hitFiles = [os.path.join(hitPath, i) for i in os.listdir(hitPath) if i.endswith(".txt")]

# hitFrame = pd.DataFrame()

# hitFileList = []

# for h in hitFiles:
#     p = pd.read_csv(h)
#     p.columns = ["class", "xc", "xy", "w", "h", "hit"]
#     bn = os.path.splitext(os.path.basename(h))[0][8:]
#     hitFileList.append(bn)
#     p['id'] = bn

#     hitFrame = hitFrame.append(p)

# print(hitFileList)


# pixelPath = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\pixelCount"
# pixelFiles = [os.path.join(pixelPath, i + "_pixelCount.txt") for i in hitFileList]

# pixelFrame = pd.DataFrame()

# for h in pixelFiles:
#     p = pd.read_csv(h, header=None, sep=" ")
#     p.columns = ["class", "xc", "xy", "w", "h", "pixels"]
#     bn = os.path.splitext(os.path.basename(h))[0][:-11]
#     print(bn)
#     p['id'] = bn
#     pixelFrame = pixelFrame.append(p)

# m = hitFrame.merge(pixelFrame)

# m0_100 = m[m['pixels'] <= 100]
# m100_above = m[m['pixels'] > 100]

# f = plt.figure()
# f, ax = plt.subplots(nrows = 1, ncols = 2)
# plt.suptitle("Standard")

# sns.histplot(data=m0_100, x="pixels", hue="hit", multiple="stack", binwidth=5, ax=ax[0], color = "r")
# ax[0].get_legend().remove()


# sns.histplot(data=m100_above, x="pixels", hue="hit", multiple="stack", binwidth=5, ax=ax[1])
# plt.legend(title='Detected', loc='upper right', labels=['Yes', 'No'])
# ax[1].set(ylabel=None)
# plt.savefig("data/x_20230227/results/figures/original_annotationHits_fullPixelRange.png", dpi = 600)
# plt.show()



# ### SLICED ###
# #Load data
# scores = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\results\sliced\detectSAHI\x_20230227_SlicedScores.txt"
# resolutions = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\petripixels\petriPixels.txt'
# objects = r'C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\objects.txt'

# scores = pd.read_csv(scores)
# resolutions = pd.read_csv(resolutions)
# objects = pd.read_csv(objects)

# # Merge
# x = scores.merge(resolutions, how = 'inner')
# x = x.merge(objects, how = 'inner')

# x['f1'] = 2*((x['precision']*x['recall'])/(x['precision']+x['recall']))

# d = {"A":1,
#     "B":2,
#     "C":3,
#     "D":4}

# groupL = x['image'].str[:1]
# group = [d[k] for k in groupL]

# x['group'] = groupL
# x['id'] = group
# print(x)
# # Plot
# #f = plt.figure()    
# f, axes = plt.subplots(nrows = 3, ncols = 1, sharex=True)

# axes[0].set_title("Slicing")
# k = axes[0].scatter(x['petriPixels'], x['precision'], s = (x['objects']/9285)*10000, c = x['id'], alpha=0.6, edgecolors="black", label = x['group'])
# axes[0].set_ylabel("Precision")
# axes[0].set_ylim(0,1)

# axes[1].scatter(x['petriPixels'], x['recall'], s = (x['objects']/9285)*10000, c = x['id'], alpha=0.6, edgecolors="black")
# axes[1].set_ylabel("Recall")
# axes[1].set_ylim(0,1)

# axes[2].scatter(x['petriPixels'], x['f1'], s = (x['objects']/9285)*10000, c = x['id'], alpha=0.6, edgecolors="black")
# axes[2].set_ylabel("F1")
# axes[2].set_ylim(0,1)
# axes[2].set_xlabel("Petri dish resolution (pixels)")

# plt.savefig("data/x_20230227/results/figures/PRF1_Slicing.png", dpi=600)
# plt.show()




##### Accuracy vs pixels per object #####

# hitPath = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\results\sliced/detectSAHi\annotationHits"
# hitFiles = [os.path.join(hitPath, i) for i in os.listdir(hitPath) if i.endswith(".txt")]

# hitFrame = pd.DataFrame()

# hitFileList = []

# for h in hitFiles:
#     p = pd.read_csv(h)
#     p.columns = ["class", "xc", "xy", "w", "h", "hit"]
#     bn = os.path.splitext(os.path.basename(h))[0][8:]
#     hitFileList.append(bn)
#     p['id'] = bn

#     hitFrame = hitFrame.append(p)

# print(hitFileList)


# pixelPath = r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\data\x_20230227\pixelCount"
# pixelFiles = [os.path.join(pixelPath, i + "_pixelCount.txt") for i in hitFileList]

# pixelFrame = pd.DataFrame()

# for h in pixelFiles:
#     p = pd.read_csv(h, header=None, sep=" ")
#     p.columns = ["class", "xc", "xy", "w", "h", "pixels"]
#     bn = os.path.splitext(os.path.basename(h))[0][:-11]
#     print(bn)
#     p['id'] = bn
#     pixelFrame = pixelFrame.append(p)

# m = hitFrame.merge(pixelFrame)

# m0_100 = m[m['pixels'] <= 100]
# m100_above = m[m['pixels'] > 100]

# f = plt.figure()
# f, ax = plt.subplots(nrows = 1, ncols = 2)
# plt.suptitle("Slicing")

# sns.histplot(data=m0_100, x="pixels", hue="hit", multiple="stack", binwidth=5, ax=ax[0], color = "r")
# ax[0].get_legend().remove()


# sns.histplot(data=m100_above, x="pixels", hue="hit", multiple="stack", binwidth=5, ax=ax[1])
# plt.legend(title='Detected', loc='upper right', labels=['Yes', 'No'])
# ax[1].set(ylabel=None)
# plt.savefig("data/x_20230227/results/figures/sliced_annotationHits_fullPixelRange.png", dpi = 600)
# plt.show()


