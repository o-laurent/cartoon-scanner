# load and show an image with Pillow
from PIL import Image
import numpy as np
from imageTools import sharpenImage

# to load the list of files
from os import listdir
from os.path import isfile, join


def isBlack(arr):
    var = int(arr[0])+int(arr[1])+int(arr[2])
    return (var < 320) and arr[0] < 120 and arr[1] < 120 and arr[2] < 120


def isWhite(arr):
    var = int(arr[0])+int(arr[1])+int(arr[2])
    return (var > 500)


def transX(sX, x):
    return x*sX


def transY(sY, y):
    return y*sY


def isCorner(image, i, j):
    boolean = True
    while boolean and j > 172:
        boolean = not isBlack(image[i][j])
        j -= 1
    #print([i, j])
    return boolean


"""imagePIL = Image.open(imgName)
imageGPIL = imagePIL.convert('L')

# get the size of the image
width = imagePIL.size[0]
height = imagePIL.size[1]

# matrixize and sharpen the image
#image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)
image = np.array(imagePIL)
# find the real dimensions 
# on commence par le haut au milieu, on cherche le premier pixel noir 
found = False 
mid = width//2
maxI = 0
i = 100
while not found and i < height:
    if isBlack(image[i][mid]):
        j = -round(width/40)
        stop = False
        while not stop and j<round(width/40):
            foundJ = False 
            varI = -round(height/50)
            while not foundJ and varI < round(height/50):
                foundJ = isBlack(image[i+varI][mid+j])
                varI += 1
            stop = not foundJ #si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
            if foundJ:
                maxI = i
            j += 1
        if not stop:
            found = True
    i += 1

upperThreshold = maxI - 172
print('upper : '+str(maxI))

found = False
maxI = 0
i = height - 101
while not found and i > upperThreshold + 100:
    if isBlack(image[i][mid]):
        j = -round(width/40)
        stop = False
        while not stop and j<round(width/40):
            foundJ = False 
            varI = -round(height/50)
            while not foundJ and varI < round(height/50):
                foundJ = isBlack(image[i+varI][mid+j])
                varI += 1
            stop = not foundJ #si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
            if foundJ:
                maxI = i
            j += 1
        if not stop:
            found = True
    i -= 1

lowerThreshold = maxI + 172
print('lower : '+str(maxI))

found = False
mid = height//2
maxJ = 0
j = 100
while not found and j < width:
    if isBlack(image[mid][j]):
        i = -round(height/40)
        stop = False
        while not stop and i<round(height/40):
            foundI = False 
            varJ = -round(width/50)
            while not foundI and varJ < round(width/50):
                foundI = isBlack(image[mid+i][j+varJ])
                varJ += 1
            stop = not foundI #si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
            if stop:
                print('missed')
                print(mid+i)
            if foundI:
                maxJ = j
            i += 1
        if not stop:
            found = True
    j += 1

leftThreshold = maxJ - 172
print('left : '+str(maxJ))

found = False
maxJ = 0
j = width-101
while not found and j > leftThreshold + 100:
    if isBlack(image[mid][j]):
        i = -round(height/40)
        stop = False
        while not stop and i<round(height/40):
            foundI = False 
            varJ = -round(width/50)
            while not foundI and varJ < round(width/50):
                foundI = isBlack(image[mid+i][j+varJ])
                varJ += 1
            stop = not foundI #si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
            if stop:
                print('missed')
                print(mid+i)
            if foundI:
                maxJ = j
            i += 1
        if not stop:
            found = True
    j -= 1

rightThreshold = maxJ + 172
print('right : '+str(maxJ))"""

# Coin supérieur gauche


def left_top_edge(image, upperThreshold, width):
    """ runs along the cartoon strokes to find the left top edge """
    i = upperThreshold + 172
    j = width//2
    corner = False
    while not corner:
        while isBlack(image[i][j]):
            j -= 1
        up = 0
        for varI in range(1, 11):
            up += int(isBlack(image[i-varI][j]))

        down = 0
        for varI in range(1, 11):
            down += int(isBlack(image[i+varI][j]))

        left = 0
        for varI in range(-5, 6):
            for varJ in range(1, 6):
                left += int(isBlack(image[i+varI][j-varJ]))

        if left < 10:
            corner = True
        if up >= down:
            i -= up//2
        else:
            i += down//2
    print(i, j-1)
    return [i, j-1]

# Coin supérieur droit


def right_top_edge(image, upperThreshold, width):
    """ runs along the cartoon strokes to find the right top edge """
    i = upperThreshold + 172
    j = width//2
    corner = False
    while not corner:
        while isBlack(image[i][j]):
            j += 1
        up = 0
        for varI in range(1, 11):
            up += int(isBlack(image[i-varI][j]))

        down = 0
        for varI in range(1, 11):
            down += int(isBlack(image[i+varI][j]))

        right = 0
        for varI in range(-5, 6):
            for varJ in range(1, 6):
                right += int(isBlack(image[i+varI][j+varJ]))

        if right < 10:
            corner = True
        if up >= down:
            i -= up//2
        else:
            i += down//2
    print(i, j+1)
    return [i, j+1]

# Coin inférieur gauche


def left_low_edge(image, lowerThreshold, width):
    """ runs along the cartoon strokes to find the left low edge """
    i = lowerThreshold - 172
    j = width//2
    corner = False
    while not corner:
        while isBlack(image[i][j]):
            j -= 1
        up = 0
        for varI in range(1, 11):
            up += int(isBlack(image[i-varI][j]))

        down = 0
        for varI in range(1, 11):
            down += int(isBlack(image[i+varI][j]))

        left = 0
        for varI in range(-5, 6):
            for varJ in range(1, 6):
                left += int(isBlack(image[i+varI][j-varJ]))

        if left < 10:
            corner = True
        if up >= down:
            i -= up//2
        else:
            i += down//2
    print(i, j-1)
    return [i, j-1]

# Coin inférieur droit


def right_low_edge(image, lowerThreshold, width):
    """ runs along the cartoon strokes to find the right low edge """
    i = lowerThreshold - 172
    j = width//2
    corner = False
    while not corner:
        while isBlack(image[i][j]):
            j += 1
        up = 0
        for varI in range(1, 11):
            up += int(isBlack(image[i-varI][j]))

        down = 0
        for varI in range(1, 11):
            down += int(isBlack(image[i+varI][j]))

        right = 0
        for varI in range(-5, 6):
            for varJ in range(1, 6):
                right += int(isBlack(image[i+varI][j+varJ]))

        if right < 10:
            corner = True
        if up >= down:
            i -= up//2
        else:
            i += down//2
    print(i, j+1)
    return [i, j+1]


def intersection_right(image, width, leftLowEdge, lower_length):
    i = leftLowEdge[0]
    j = min(width-1, round(leftLowEdge[1] + 1.2*lower_length))
    stack = [False]*7
    comp = [True]*7
    found = False
    while not found:
        if stack == comp:
            found = True
        else:
            j -= 1
            stack.pop(0)
            stack.append(isBlack(image[i][j]))
    return [i, j+7]
