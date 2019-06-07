import itertools
import scipy.interpolate
import cv2
import numpy as np
from skimage import color
from .detect_face import DetectFace
import imutils

class ApplyMakeup:

    def __init__(self, predictor, image):

        self.df = DetectFace(predictor, image)

        self.image = 0
        self.im_copy = 0
        self.img_name = image

        # size of image
        self.width = 0
        self.height = 0
        self.depth = 0

        # r,g,b
        self.red = 0
        self.green = 0
        self.blue = 0

        # flag to distinguish
        self.count = 0

    def read_image(self, file):
        self.image = file
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.im_copy = self.image.copy()
        self.height, self.width, self.depth = self.image.shape
        self.count = 0

    def get_lip_points(self, lips_points):
        ''' get lip points by type : (upper/lower)(outer/inner)'''
        uol = []
        uil = []
        lol = []
        lil = []

        # upper outer lip/ total 7 points
        for i in range(0, 14, 2):
            uol.append([int(lips_points[i]), int(lips_points[i + 1])])

        # lower outer lip / total 7 points
        for i in range(12, 24, 2):
            lol.append([int(lips_points[i]), int(lips_points[i + 1])])
        lol.append([int(lips_points[0]), int(lips_points[1])])

        # upper inner lip
        for i in range(24, 34, 2):
            uil.append([int(lips_points[i]), int(lips_points[i + 1])])

        # lower innner lip
        for i in range(32, 40, 2):
            lil.append([int(lips_points[i]), int(lips_points[i + 1])])
        lil.append([int(lips_points[24]), int(lips_points[25])])

        return uol, uil, lol, lil

    def get_curves_lips(self, uol, uil, lol, lil):
        uol_curve = self.draw_curve(uol)
        uil_curve = self.draw_curve(uil)
        lol_curve = self.draw_curve(lol)
        lil_curve = self.draw_curve(lil)

        return uol_curve, uil_curve, lol_curve, lil_curve

    def draw_curve(self, points):
        ''' get lip_curve points by using interpolation'''
        x_pts = []
        y_pts = []
        curvex = []
        curvey = []
        self.count += 1

        for point in points:
            x_pts.append(point[0])
            y_pts.append(point[1])

        # get curve using interpolation
        curve = scipy.interpolate.interp1d(x_pts, y_pts, 'cubic')

        # upper
        if self.count <= 2:
            for i in np.arange(x_pts[0], x_pts[len(x_pts) - 1] + 1, 1):
                curvex.append(i)
                curvey.append(int(curve(i)))
        # lower
        else:
            for i in np.arange(x_pts[len(x_pts) - 1] + 1, x_pts[0], 1):
                curvex.append(i)
                curvey.append(int(curve(i)))

        return curvex, curvey

    def fill_color(self, uol_c, uil_c, lol_c, lil_c):

        self.fill_lip(uol_c, uil_c)
        self.fill_lip(lol_c, lil_c)
        self.blurring(uol_c, uil_c)
        self.blurring(lol_c, lil_c)

    def fill_lip(self, outer, inner):
        ''' fill color '''
        for i in range(len(inner)):
            inner[i].reverse()

        outer_curve = zip(outer[0], outer[1])
        inner_curve = zip(inner[0], inner[1])
        points = []

        # get lip points
        for point in outer_curve:
            points.append(list(point))

        for point in inner_curve:
            points.append(list(point))
        points = np.array(points, dtype=np.int32)

        # fill color in lips
        cv2.fillPoly(self.image, [points], (self.red, self.green, self.blue))

    def blurring(self, outer, inner):
        '''After blurring, image blending'''
        outer_curve = zip(outer[0], outer[1])
        inner_curve = zip(inner[0], inner[1])
        x_points = []
        y_points = []

        for point in outer_curve:
            x_points.append(point[0])
            y_points.append(point[1])
        for point in inner_curve:
            x_points.append(point[0])
            y_points.append(point[1])

        # black image for blurring
        img_base = np.zeros((self.height, self.width))
        blur_arr = np.array(np.c_[x_points, y_points], dtype='int32')

        # masking except lip_points
        cv2.fillConvexPoly(img_base, blur_arr, 1)

        # lip_color blurring
        img_mask = cv2.blur(img_base, (31, 31))
        img_blur_3d = np.ndarray([self.height, self.width, self.depth], dtype='float')

        for i in range(self.depth):
            img_blur_3d[:, :, i] = img_mask

        # image blending
        self.im_copy = (img_blur_3d * self.image * 0.7 + (1 - img_blur_3d * 0.7) * self.im_copy).astype('uint8')

    def apply_lipstick(self, rlips, glips, blips):

        self.red = rlips
        self.green = glips
        self.blue = blips
        self.read_image(self.df.img)

        lips = self.df.mouth
        lips_points = [item for sublist in lips for item in sublist]

        uol, uil, lol, lil = self.get_lip_points(lips_points)
        uol_c, uil_c, lol_c, lil_c = self.get_curves_lips(uol, uil, lol, lil)

        self.fill_color(uol_c, uil_c, lol_c, lil_c)
        self.im_copy = cv2.cvtColor(self.im_copy, cv2.COLOR_BGR2RGB)

        file_name = self.img_name

        cv2.imwrite(file_name, self.im_copy)






