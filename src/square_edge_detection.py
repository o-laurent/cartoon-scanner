"""
Module containing all the useful functions to determine the borders 
        and edges of the external square of the drawing
"""

from PIL import Image
import numpy as np
from imageTools import sharpenImage

# to load the list of files
from os import listdir
from os.path import isfile, join

# Utility functions


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


# Border determination functions
def upper_threshold(image, height: int, width: int, shift: int=0):
    """
    Finds the ordinate of the upper stroke
    Input:
    - image: List(List(int))
    - shift: starting abcissa shift in percentage (%)
    Output:
    - ordinate: (int)
    """
    found = False
    mid = width//2+round(shift/100*width)
    maxI = 0
    i = height//30
    while not found and i < height:
        if isBlack(image[i][mid]):
            j = -round(width/40)
            stop = False
            while not stop and j < round(width/40):
                foundJ = False
                varI = -round(height/50)
                while not foundJ and varI < round(height/50):
                    foundJ = isBlack(image[i+varI][mid+j])
                    varI += 1
                # si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
                stop = not foundJ
                if foundJ:
                    maxI = i
                j += 1
            if not stop:
                found = True
        i += 1
    return maxI - 172


def lower_threshold(image, upperThreshold: int, height: int, width: int, shift: int=0):
    """
    Finds the ordinate of the lower stroke
    Input:
    - image: List(List(int))
    - height: (int)
    - width: (int)
    - shift: starting abcissa shift in percentage (%)
    Output:
    - ordinate: (int)
    """
    found = False
    mid = width//2+round(shift/100*width)
    maxI = 0
    i = (29*height)//30
    while not found and i > upperThreshold + 100:
        if isBlack(image[i][mid]):
            j = -round(width/40)
            stop = False
            while not stop and j < round(width/40):
                foundJ = False
                varI = -round(height/50)
                while not foundJ and varI < round(height/50):
                    foundJ = isBlack(image[i+varI][mid+j])
                    varI += 1
                # si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
                stop = not foundJ
                if foundJ:
                    maxI = i
                j += 1
            if not stop:
                found = True
        i -= 1
    return maxI + 172


def left_threshold(image, height, width, shift: int=0):
    """
    Finds the abcissa of the left stroke
    Input:
    - image: List(List(int))
    - height: (int)
    - width: (int)
    - shift: starting ordinate shift in percentage (%)
    Output:
    - abcissa: (int)
    """
    found = False
    mid = height//2+round(shift/100*height)
    maxJ = 0
    j = width//30
    while not found and j < width:
        if isBlack(image[mid][j]):
            i = -round(height/40)
            stop = False
            while not stop and i < round(height/40):
                foundI = False
                varJ = -round(width/50)
                while not foundI and varJ < round(width/50):
                    foundI = isBlack(image[mid+i][j+varJ])
                    varJ += 1
                # si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
                stop = not foundI
                if stop:
                    print('missed')
                    print(mid+i)
                if foundI:
                    maxJ = j
                i += 1
            if not stop:
                found = True
        j += 1
    return maxJ - 172


def right_threshold(image, leftThreshold, height, width, shift: int=0):
    """
    Finds the abcissa of the right stroke
    Input:
    - image: List(List(int))
    - leftThreshold: (int)
    - height: (int)
    - width: (int)
    - shift: starting ordinate shift in percentage (%)
    Output:
    - abcissa: (int)
    """
    found = False
    mid = height//2+round(shift/100*height)
    maxJ = 0
    j = (29*width)//30
    while not found and j > leftThreshold + 100:
        if isBlack(image[mid][j]):
            i = -round(height/40)
            stop = False
            while not stop and i < round(height/40):
                foundI = False
                varJ = -round(width/50)
                while not foundI and varJ < round(width/50):
                    foundI = isBlack(image[mid+i][j+varJ])
                    varJ += 1
                # si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
                stop = not foundI
                if stop:
                    print('missed')
                    print(mid+i)
                if foundI:
                    maxJ = j
                i += 1
            if not stop:
                found = True
        j -= 1
    return maxJ + 172 #172 margin


# Square Edge determination functions
# Coin supérieur gauche
def left_top_edge(image, upperThreshold, width):
    """ 
    runs along the cartoon strokes to find the left top edge of the square.
    """
    i = upperThreshold + 172
    j = width//2
    corner = False
    while not corner:
        while isBlack(image[i][j]) and j > 0:
            j -= 1
        if j == 0:
            print('Error')
            corner = True
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
        j -= 1  # if we are in a hole, just move a little
    return [i, j]

# Coin supérieur droit


def right_top_edge(image, upperThreshold, width):
    """ runs along the cartoon strokes to find the right top edge of the square."""
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
        j += 1
    return [i, j]

# Coin inférieur gauche


def left_low_edge(image, lowerThreshold, width):
    """ runs along the cartoon strokes to find the left low edge of the square."""
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
        j -= 1
    return [i, j]

# Coin inférieur droit


def right_low_edge(image, lowerThreshold, width):
    """ runs along the cartoon strokes to find the right low edge of the square."""
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
        j += 1
    return [i, j]


