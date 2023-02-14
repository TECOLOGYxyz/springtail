import matplotlib.pyplot as plt
import pandas as pd

dat = pd.read_csv(r"C:\Users\au309263\OneDrive - Aarhus Universitet\Desktop\candida\petripixels\petriPixels.txt")
print(dat)
print(dat['petriPixels'].dtype)
group = dat['image'].str[:1]
print(group)
names = dat['image']
values = dat['petriPixels'].astype(int)

d = {"A":1,
    "B":2,
    "C":3,
    "D":4}

group = [d[k] for k in group]
print(group)

print(max(values))

fig, axs = plt.subplots(1, 1, figsize=(5, 7), sharey=True)
axs.set_ylim([0,23000000])
axs.scatter(names, values, c = group)

fig.suptitle('Categorical Plotting')
plt.show()