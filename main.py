#   gérer quand pas assez de largeur autour de l'image
#   améliorer l'interface graphique
#   mettre l'interface graphique dans un autre fichier
#   import tkinter as tk
#   rotation de la photo

# load and show an image with Pillow
from PIL import Image
import numpy as np 
from imageTools import sharpenImage, post_process
from square_edge_detection import left_low_edge, left_top_edge, right_low_edge, right_top_edge, intersection_right
# to load the list of files
from os import listdir
from os.path import isfile, join

#imgName = imgNameInput.get()
seriesName = 'plaidpenche'

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

def instaPrep(seriesName: str):
    # Load list of files 
    file_list = [f for f in listdir() if isfile(f)]
    file_list = [f for f in file_list if f.split('.')[1].lower()=='jpg' and f.split('_')[0]==seriesName and f.split('_')[-1].split('.')[0]!='d' and (f.split('.')[0]+'_d.'+f.split('.')[1] not in file_list)]
    file_list = list(map(lambda x: x.split('.')[0], file_list))
    file_list.sort()
    nb = len(file_list)
    if nb==0:
        print('Aucune photo trouvée. Fin du processus.')

    if nb==1:
        print('1 photo à traiter')
        digitalizeImage(seriesName+'_1.jpg')

    if nb==2:
        print('2 photos à traiter')
        # digitalize separately
        for i in range(1, 3):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            digitalizeImage(seriesName+'_'+str(i)+'.jpg')

    if nb==3:
        print('3 photos à traiter')
        #déterminer laquelle est le rectangle
        # digitalize separately
        for i in range(1, 4):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            digitalizeImage(seriesName+'_'+str(i)+'.jpg')

    if nb==4:
        print('4 photos à traiter')
        images = []
        # digitalize separately
        for i in range(1, 5):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            images.append(digitalizeImage(seriesName+'_'+str(i)+'.jpg'))
        # Merge 
        merge4(seriesName, images[0], images[1], images[2], images[3])

def digitalizeImage(imgName):
    # Open the image form working directory
    imagePIL = Image.open(imgName)
    imageGPIL = imagePIL.convert('L')

    # get the size of the image
    width = imagePIL.size[0]
    height = imagePIL.size[1]

    # matrixize and sharpen the image
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

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
    leftTopEdge = left_top_edge(image, upperThreshold, width)
    rightTopEdge = right_top_edge(image, upperThreshold, width)
    rightLowerEdge = right_low_edge(image, lowerThreshold, width)
    leftLowerEdge = left_low_edge(image, lowerThreshold, width)

    upper_length = ((leftTopEdge[0]-rightTopEdge[0])**2+(leftTopEdge[1]-rightTopEdge[1])**2)**(1/2)
    lower_length = ((leftLowerEdge[0]-rightLowerEdge[0])**2+(leftLowerEdge[1]-rightLowerEdge[1])**2)**(1/2)
    left_length = ((leftTopEdge[0]-leftLowerEdge[0])**2+(leftTopEdge[1]-leftLowerEdge[1])**2)**(1/2)
    right_length = ((rightLowerEdge[0]-rightTopEdge[0])**2+(rightLowerEdge[1]-rightTopEdge[1])**2)**(1/2)

    print(lower_length)
    print('longueur côté haut : '+str(upper_length)+' pixels')
    print('longueur côté bas : '+str(lower_length)+' pixels')
    print('longueur côté gauche : '+str(left_length)+' pixels')
    print('longueur côté droite : '+str(right_length)+' pixels')

    # Rotation 
    #On considère la droite passant par les deux coins droits et on cherche son intersection avec l'horizontale passant par le coin en bas à gauche
    i_A = leftLowerEdge[0]
    i_C = rightTopEdge[0]
    i_D = rightLowerEdge[0]
    j_A = leftLowerEdge[1]
    j_C = rightTopEdge[1]
    j_D = rightLowerEdge[1]
    is_C = -i_C + i_A
    is_D = -i_D + i_A
    jp_C = j_C - j_A
    jp_D = j_D - j_A
    
    a = (is_C-is_D)/(jp_C-jp_D)
    b = -jp_D*a

    right_intersection = [i_A, j_A-b/a]
    rightLowEdge_dist = ((right_intersection[0]-rightLowerEdge[0])**2 + (right_intersection[1]-rightLowerEdge[1])**2)**(1/2)

    angleRLE = np.arctan(rightLowEdge_dist/lower_length)*180/np.pi
    if i_A > i_D: #negative angle
        angleRLE *= -1

    print(angleRLE)

    # Crop and sharpen the image
    box = (leftThreshold, upperThreshold, rightThreshold, lowerThreshold) #left upper right lower
    imagePIL = imagePIL.rotate(angleRLE).crop(box)
    imageGPIL = imagePIL.convert('L')

    width = imagePIL.size[0]
    height = imagePIL.size[1]
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

    newImage = np.zeros((2800, 2800, 3))

    sX = height/2800
    sY = width/2800

    # Build the new image 

    for x in range(2800):
        for y in range(2800):
            color = image[int(transX(sX,x))][int(transY(sY, y))]
            if not isWhite(color):
                newImage[x][y] = color
            else: 
                newImage[x][y] = [255,255,255]
    newImage = post_process(newImage)
    numImagePIL = Image.fromarray(newImage.astype('uint8'), 'RGB')

    signaturePIL = Image.open('./signature/signature.jpg').resize((75, 600))
    box = (2800-172-50-50, 2800-172-50-600, 2800-172-25, 2800-172-50)
    numImagePIL.paste(signaturePIL, box)
    numImagePIL.save(imgName.split('.')[0]+'_d.jpg')
    return newImage

def merge4(seriesName, image1, image2, image3, image4):
    print('Assemblage')
    box1 = (95, 95, 1363, 1363) #include centering (172/2=86)
    box2 = (1437, 95, 2705, 1363)
    box3 = (95, 1437, 1363, 2705)
    box4 = (1437, 1437, 2705, 2705)
    image1PIL = Image.fromarray(image1.astype('uint8'), 'RGB').resize((1400, 1400)).crop((66,66,1400-66,1400-66))
    image2PIL = Image.fromarray(image2.astype('uint8'), 'RGB').resize((1400, 1400)).crop((66,66,1400-66,1400-66))
    image3PIL = Image.fromarray(image3.astype('uint8'), 'RGB').resize((1400, 1400)).crop((66,66,1400-66,1400-66))
    image4PIL = Image.fromarray(image4.astype('uint8'), 'RGB').resize((1400, 1400)).crop((66,66,1400-66,1400-66))
    newImage = np.ones((2800, 2800, 3))*255
    newImagePIL = Image.fromarray(newImage.astype('uint8'), 'RGB')
    
    signaturePIL = Image.open('./signature/signature.jpg').resize((75, 600))
    boxs = (2800-115-50-50, 2800-115-600-10, 2800-115-25, 2800-115-10)

    newImagePIL.paste(image1PIL, box1)
    newImagePIL.paste(image2PIL, box2)
    newImagePIL.paste(image3PIL, box3)
    newImagePIL.paste(image4PIL, box4)
    newImagePIL.paste(signaturePIL, boxs)
    newImagePIL.save(seriesName+'_d.jpg')


instaPrep(seriesName)