import cv2
import numpy as np
import math

def WhiteBalance(filename):
    img = cv2.imread(filename,cv2.IMREAD_COLOR)
    result = WB(extractWhite(equ_Hist(img)),img)
    cv2.imwrite(filename,result)


def equ_Hist(img):
    b, g, r = cv2.split(img)
    e_r = cv2.equalizeHist(r)
    e_g = cv2.equalizeHist(g)
    e_b = cv2.equalizeHist(b)
    equ = cv2.merge([e_b, e_g, e_r])
    return equ

# extract White point of image & return index of white point
def extractWhite(img):
    b, g, r = cv2.split(img)

    # use YCbCr space
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = 0.564 * (b - y)
    cr = 0.731 * (r - y)

    # mask white point
    mask1 = (y > 200)
    mask2 = (cb > -2) & (cb < 2)
    mask3 = (cr > -2) & (cr < 2)

    mask = (mask1 & mask2 & mask3)
    mask = mask.astype(np.uint8)

    # index of white point
    idx = np.transpose(np.nonzero(mask))

    return idx


# White Balance algorithm
def WB(idx, img):
    b, g, r = cv2.split(img)
    equ = equ_Hist(img)
    b1, g1, r1 = cv2.split(equ)
    y = 0.299 * r1 + 0.587 * g1 + 0.114 * b1

    # Point of Max Y
    result = np.where(y == np.amax(y))

    listOfCordinates = list(zip(result[0], result[1]))

    # calculate avg of RGB of Max Y point
    for cord in listOfCordinates:
        i, j = cord[0], cord[1]
        y_avg = (int(r[i][j]) + int(g[i][j]) + int(b[i][j])) / 3

    count = idx.shape[0]
    r_sum = 0
    g_sum = 0
    b_sum = 0

    # copy of r,g,b
    r_c, g_c, b_c = r, g, b

    # calculate avg of RGB of white Point
    for k in idx:
        i, j = k[0], k[1]
        r_sum += r[i][j]
        g_sum += g[i][j]
        b_sum += b[i][j]

    r_avg = r_sum / count
    g_avg = g_sum / count
    b_avg = b_sum / count

    r_gain = y_avg / r_avg
    g_gain = y_avg / g_avg
    b_gain = y_avg / b_avg

    if r_gain + b_gain + g_gain > 3:
        gain_sum = r_gain + b_gain + g_gain
        r_gain = (3 * r_gain) / gain_sum
        g_gain = (3 * g_gain) / gain_sum
        b_gain = (3 * b_gain) / gain_sum

    r = r * r_gain
    b = b * b_gain
    g = g * g_gain

    r = r.astype(np.uint8)
    g = g.astype(np.uint8)
    b = b.astype(np.uint8)

    # prevent overflow
    for i in np.arange(r.shape[0]):
        for j in np.arange(r.shape[1]):
            if abs(int(r[i][j]) - int(r_c[i][j])) > 200:
                r[i][j] = r_c[i][j]
            if abs(int(g[i][j]) - int(g_c[i][j])) > 200:
                g[i][j] = g_c[i][j]
            if abs(int(b[i][j]) - int(b_c[i][j])) > 200:
                b[i][j] = b_c[i][j]

    return cv2.merge([b, g, r])