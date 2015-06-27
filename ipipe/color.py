import skimage
import itertools
import time
from skimage import data
from skimage.viewer import ImageViewer
from skimage.color import rgb2gray
from skimage import io
from skimage import exposure


class SizeColor:

    def readImage(imagePath):
        return io.imread(imagePath)

    def viewImage(image):
        viewer = ImageViewer(image)
        viewer.show()

    def convertImage(image):
        return rgb2gray(image)

    # can this be faster

    def getImageBorders(mask):

        n_rows = len(mask)
        n_cols = len(mask[0])
        row_top = n_rows
        col_left = n_cols
        row_bottom = 0
        col_right = 0

        iterator = np.nditer(mask, flags=['multi_index'])

        for val in iterator:
            row = iterator.multi_index[0]
            if val:
                if row < row_top:
                    row_top = row

        iterator.reset()
        for val in iterator:
            col = iterator.multi_index[1]
            if val:
                if col < col_left:
                    col_left = col

        iterator = np.nditer(mask[::-1][::-1], flags=['multi_index'])

        for val in iterator:
            row = iterator.multi_index[0]
            if val:
                if row > row_bottom:
                    row_bottom = row

        iterator.reset()

        for val in iterator:
            col = iterator.multi_index[1]
            if val:
                if col > col_right:
                    col_right = col

        # for i in range(len(mask)):
        #     for j in range(len(mask[0])):
        #         pixel_val = mask[i][j]
        #         if pixel_val:
        #             if i < start_x_index:
        #                 start_x_index = i
        #             if j < start_y_index:
        #                 start_y_index = j

        # for i in reversed(range(len(mask))):
        #     for j in reversed(range(len(mask[0]))):
        #         pixel_val = mask[i][j]
        #         if pixel_val:
        #             if i > end_x_index:
        #                 print "i: " + i
        #                 end_x_index = i
        #             if j > col_right_index:
        #                 print "j: " + j
        #                 col_right_index = j

        return {'row_top': row_top, 'row_bottom': row_bottom, 'col_left':
                col_left, 'col_right': col_right}

    def cropImage(image, threshold):
        mask = image > threshold
        cropWidth = getImageBorders(mask)
        x_dim = cropWidth['row_bottom'] - cropWidth['row_top']
        y_dim = cropWidth['col_right'] - cropWidth['col_left']
        imgCrop = zeros((x_dim, y_dim), dtype=image.dtype)

        # looks slow

        for i1, i2 in zip(range(cropWidth['row_top'],
            cropWidth['row_bottom']), range(len(imgCrop))):
                for j1, j2
            in zip(range(cropWidth['col_left'],
                         cropWidth['col_right']), range(len(imgCrop[0]))):
            imgCrop[i2][j2] = image[i1][j1]

        return imgCrop

    def sPipe(image):
        print "Reading Image"
        t0 = time.time()
        retina = readImage(image)
        t1 = time.time()
        print("Done took %.2f seconds" % (t1 - t0))
        print 'Converting to Grayscale with luminance preservation'
        t0 = time.time()
        retina_gray = convertImage(retina)
        t1 = time.time()
        print("Done took %.2f seconds" % (t1 - t0))
        print 'Cropping image from background'
        t0 = time.time()
        retina_crop = cropImage(retina_gray, 0.05)
        t1 = time.time()
        print("Done took %.2f seconds" % (t1 - t0))
        print 'Logarithmic Correction'
        t0 = time.time()
        retina_adjust = exposure.adjust_log(retina_crop)
        t1 = time.time()
        print("Done took %.2f seconds" % (t1 - t0))
        viewImage(retina_adjust)
        return retina_adjust
