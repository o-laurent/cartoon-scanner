# load and show an image with Pillow
from PIL import Image
import numpy as np 
from imageTools import sharpenImage

# to load the list of files
from os import listdir
from os.path import isfile, join

def isBlack(arr):
    var = int(arr[0])+int(arr[1])+int(arr[2])
    return (var<320) and arr[0]<120 and arr[1]<120 and arr[2]<120

def isWhite(arr):
    var = int(arr[0])+int(arr[1])+int(arr[2])
    return (var>500)

def transX(sX, x):
    return x*sX

def transY(sY, y):
    return y*sY

def isCorner(image, i, j):
    boolean = True
    while boolean and j>172:
        boolean = not isBlack(image[i][j])
        j-=1
    #print([i, j])
    return boolean

imgName = 'plaid_2_d.jpg'

imagePIL = Image.open(imgName)
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
print('right : '+str(maxJ))

# Find the edges 
leftTopEdge = [upperThreshold, leftThreshold]
rightTopEdge = [upperThreshold, rightThreshold]
rightLowerEdge = [lowerThreshold, rightThreshold]
leftLowerEdge = [lowerThreshold, leftThreshold]


# Coin supérieur gauche 
i = upperThreshold + 172
j = width//2
corner = False 
while not corner:
    while isBlack(image[i][j]):
        j -= 1
    if int(isBlack(image[i+1][j]))+int(isBlack(image[i+2][j]))+int(isBlack(image[i+3][j])) >= 2:
        i += 1
    elif int(isBlack(image[i-1][j]))+int(isBlack(image[i-2][j]))+int(isBlack(image[i-3][j])) >= 2:
        i -= 1
    else:
        corner = True
leftTopEdge = [i, j-1]

# Coin supérieur droit 
i = upperThreshold + 172
j = width//2
corner = False 
while not corner:
    while isBlack(image[i][j]):
        j += 1
    if int(isBlack(image[i+1][j]))+int(isBlack(image[i+2][j]))+int(isBlack(image[i+3][j])) >= 2:
        i += 1
    elif int(isBlack(image[i-1][j]))+int(isBlack(image[i-2][j]))+int(isBlack(image[i-3][j])) >= 2:
        i -= 1
    else:
        corner = True
rightTopEdge = [i, j]

# Coin supérieur gauche 
i = lowerThreshold - 172
j = width//2
corner = False 
while not corner:
    while isBlack(image[i][j]):
        j -= 1
    if int(isBlack(image[i+1][j]))+int(isBlack(image[i+2][j]))+int(isBlack(image[i+3][j])) >= 2:
        i += 1
    elif int(isBlack(image[i-1][j]))+int(isBlack(image[i-2][j]))+int(isBlack(image[i-3][j])) >= 2:
        i -= 1
    else:
        corner = True
leftLowEdge = [i, j-1]

# Coin supérieur droit 
i = lowerThreshold - 172
j = width//2
corner = False 
while not corner:
    while isBlack(image[i][j]):
        j += 1
    if int(isBlack(image[i+1][j]))+int(isBlack(image[i+2][j]))+int(isBlack(image[i+3][j])) >= 2:
        i += 1
    elif int(isBlack(image[i-1][j]))+int(isBlack(image[i-2][j]))+int(isBlack(image[i-3][j])) >= 2:
        i -= 1
    else:
        corner = True
rightLowEdge = [i, j]

print(leftTopEdge)
print(rightTopEdge)
print(leftLowEdge)
print(rightLowEdge)

print('longueur côté haut : '+str((leftTopEdge[1]**2+rightTopEdge[1]**2)**(1/2))+'pixels')
print('longueur côté bas : '+str((leftLowEdge[1]**2+rightLowEdge[1]**2)**(1/2))+'pixels')
print('longueur côté gauche : '+str((leftTopEdge[0]**2+leftLowEdge[0]**2)**(1/2))+'pixels')
print('longueur côté droite : '+str((rightLowEdge[0]**2+rightTopEdge[0]**2)**(1/2))+'pixels')