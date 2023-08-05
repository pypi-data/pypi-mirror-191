# What are you doing here?)
import cv2 # pip install opencv-python
from numpy import* # pip install numpy
from os import getcwd

def downoladimage(image = 'image.png', imagefilter = 'none'):

    if imagefilter == 'none':
        cv2.imwrite(image)
    else:
        cv2.imwrite(image, imagefilter)

def bw(path = getcwd().replace('\\', '/') + '/', image = 'image.png'):

    file = cv2.imread(path + image)

    bw = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

    return bw

def removebackground(path = getcwd().replace('\\', '/') + '/', image = 'image.png'):

    file = cv2.imread(path + image)

    gray = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
    mask = 255 - mask

    kernel = ones((3,3), uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = (2*(mask.astype(float32))-255).clip(0, 255).astype(uint8)

    result = file.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    return result

def blur(path = getcwd().replace('\\', '/') + '/', image = 'image.png', stage = 'minimum'):

    file = cv2.imread(path + image)

    if stage == 'extra':
        blur = cv2.GaussianBlur(file, (99, 99), 0)
    elif stage == 'meddium':
        blur = cv2.GaussianBlur(file, (75, 75), 0)
    else:
        blur = cv2.GaussianBlur(file, (51, 51), 0)

    return blur

def cartoon(path = getcwd().replace('\\', '/') + '/', image = 'image.png'):

    file = cv2.imread(path + image)

    gray = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    color = cv2.bilateralFilter(file, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, file, mask = edges)
    
    return cartoon

def rotate(path = getcwd().replace('\\', '/') + '/', image = 'image.png', gradus = 180):

    file = cv2.imread(path + image)

    (height, weight, d) = file.shape
    center = (weight // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, gradus, 1.0)
    rotate = cv2.warpAffine(file, matrix, (weight, height))

    return rotate

def getimamageresolution(path = getcwd().replace('\\', '/') + '/', image = 'image.png', sizetype = 'numeric'):

    file = cv2.imread(path + image)

    (height, weight) = file.shape[:2]
    bigger = max(height, weight)
    if bigger >= 2048:
        resolution = f'{max(height, weight) // 1024}K'
    elif bigger >= 1620:
        resolution = 'QuadHD+'
    elif bigger >= 1440:
        resolution = 'QuadHD'
    elif bigger >= 1280:
        resolution = 'FullHD+'
    elif bigger >= 1080:
        resolution = 'FullHD'
    elif bigger >= 900:
        resolution = 'HD+'
    elif bigger >= 720:
        resolution = 'HD'
    elif bigger >= 540:
        resolution = 'qHD'
    elif bigger >= 480:
       resolution = 'SD'
    else:
        resolution = '<SD'

    if sizetype == 'pixels':
        resolution = f'{weight}px x {height}px'
    elif sizetype == 'name':
        if bigger >= 2048:
            resolution = f'{max(height, weight) // 1024}K'
        elif bigger >= 1620:
            resolution = 'QuadHD+'
        elif bigger >= 1440:
            resolution = 'QuadHD'
        elif bigger >= 1280:
            resolution = 'FullHD+'
        elif bigger >= 1080:
            resolution = 'FullHD'
        elif bigger >= 900:
            resolution = 'HD+'
        elif bigger >= 720:
            resolution = 'HD'
        elif bigger >= 540:
            resolution = 'qHD'
        elif bigger >= 480:
           resolution = 'SD'
        else:
            resolution = '<SD'
    elif sizetype == 'orientation':
        if weight > height:
            resolution = 'wertical'
        elif height > weight:
            resolution = 'horizontal'
        else:
            form = 'cube'
    return resolution