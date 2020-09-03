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


# Coin supérieur gauche


def left_top_edge(image, upperThreshold, width):
    """ runs along the cartoon strokes to find the left top edge """
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
        j += 1
    return [i, j]

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
        j -= 1
    return [i, j]

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
        j += 1
    return [i, j]


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
