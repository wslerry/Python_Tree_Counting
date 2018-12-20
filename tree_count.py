# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:52:04 2018

@author: lerryw
"""

import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage import exposure

raster = 'PATH/TO/YOUR/CHM/DATA'
img = gdal.Open(raster,gdal.GA_ReadOnly)
img = img.ReadAsArray()
image = np.array(img, dtype=float)
p2, p98 = np.percentile(img, (2, 98))
img_rescale = exposure.rescale_intensity(image, in_range=(p2, p98))

image_max = ndi.maximum_filter(image, size=3, mode='constant')

coordinates = peak_local_max(image, min_distance=2)
X=coordinates[:, 1]
y=coordinates[:, 0]

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
