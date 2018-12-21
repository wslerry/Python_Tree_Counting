# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:52:04 2018

@author: lerryw
"""
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage import exposure

# import dataset into python using rasterio
raster = 'test_data.tif'
with rasterio.open(raster) as source:
    img = source.read(1) # Read raster band 1 as a numpy array
    affine = source.affine
# rescale image if needeed
p2, p98 = np.percentile(img, (2, 98))
img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

# apply amaximum filter 
image_max = ndi.maximum_filter(image, size=3, mode='constant')

# locate all the mximum peak
coordinates = peak_local_max(image, min_distance=2)
X=coordinates[:, 1]
y=coordinates[:, 0]

#reproject data array into original dataset 
xs, ys = affine * (X, y)

# create some datasheet
df = pd.DataFrame({'X':xs, 'Y':ys})

# count trees
count = df['X'].count()
print('Total counted tree : {i}'.format(i = count))
df.to_csv(r'C:\\Map\\Misc\\T2E_volume\\CHM_process\\test_output.csv')
df.to_json(r'C:\\Map\\Misc\\T2E_volume\\CHM_process\\test_output.json')

# lets do some plotting
fig, axes = plt.subplots(1, 3, figsize=(10, 10), sharex=True, sharey=True)
cmap=plt.cm.gist_earth
ax = axes.ravel()
ax[0].imshow(img_rescale, cmap)
ax[0].axis('off')
ax[0].set_title('Original')

ax[1].imshow(image_max, cmap)
ax[1].axis('off')
ax[1].set_title('Maximum filter')

ax[2].imshow(img_rescale, cmap)
ax[2].autoscale(False)
ax[2].plot(X,y, 'r.')
ax[2].axis('off')
ax[2].set_title('Peak local max')

fig.tight_layout()
plt.show()
