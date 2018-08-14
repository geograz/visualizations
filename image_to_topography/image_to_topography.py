# This is an application that converts images into topographies. It takes the
# pixel's X- & Y- coordinates and calculates the height from the respective
# pixel value.
#
# One can either use the given methods for generating a contour or 3D scatter
# plot (3D scatter plots may become computationally very expensive), or export
# the X, Y, Z coordinates for further processing in other programs like QGIS,
# CloudCompare etc....

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from PIL import Image


class image_to_topography:

    def __init__(self, filename, max_height=150):

        self.filename = filename
        self.max_height = max_height

    def data_import(self):

        im = Image.open(self.filename)
        print('data imported')

        return im

    def preprocessing(self):

        data = np.asarray(self.data_import(), dtype="int32")

        # handle for RGB of grayscale images:
        #   grayscale image -> len(data.shape) == 2
        #   RGB image -> len(data.shape) == 3

        # Z value is either taken directly from the grayscale value, or
        # calculated from the mean of the respective RGB values

        if len(data.shape) == 2:
            Z = data
        else:
            Z = np.mean(data, axis=2)

        # set max_height of Z values, because a range from 255 to 0 creates
        # very steep valleys/mountains
        max_height = self.max_height

        Z = max_height - (Z/Z.max()*max_height)

        # flip along X-axis because the coordinate origin of images is in the
        # upper, right corner -> results in upside down image when pixel
        # coordinates are treated as cartesian coordinates
        Z = np.flip(Z, axis=0)
        print('Z values calculated')

        return Z

    def contour_plot(self, cmap,
                     colors=None, linewidths=0.5,
                     levels=np.arange(1000, step=7)):

        Z = self.preprocessing()

        fig, ax = plt.subplots()

        ax.axis('equal')
        ax.axis([0, Z.shape[1], 0, Z.shape[0]])
        ax.set_axis_off()

        ax.contour(Z, colors=colors,
                   cmap=cmap, levels=levels,
                   linewidths=linewidths)

    def calc_coords(self):

        Z = self.preprocessing()

        # generates coordinates according to the shape of the pixel values
        X, Y = np.arange(Z.shape[1]), np.arange(Z.shape[0])
        X, Y = np.meshgrid(X, Y)

        X = X.flatten()
        Y = Y.flatten()
        Z = Z.flatten()

        return X, Y, Z

    def threeD_plot(self):

        X, Y, Z = self.calc_coords()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(X, Y, Z)

    def coords_export(self, filename='test.xyz'):

        X, Y, Z = self.calc_coords()

        df = pd.DataFrame({'X': X, 'Y': Y, 'Z': Z})
        df.to_csv(filename, sep=';', index=False)
        print('points exported')


itt = image_to_topography('test.jpg')

itt.contour_plot(levels=np.arange(1000, step=7), colors=None, cmap='bone_r')
plt.savefig('test_modified.jpg', dpi=300)

# change file ending to '.txt', or '.csv' if preferred
itt.coords_export('test_modified.xyz')
