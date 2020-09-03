#   moyenne des traits du bord, min et max, noircir le trait à fond
#   gérer 2,3 images
#   Mettre les images de to_process dans le dossier
# verbose mode GUI selectable
# comments
# save steps GUI selectable
# propose choices
#ne pas tout retransformer en jpg si ça l'est déjà

# load images with Pillow
from PIL import Image
import numpy as np
from imageTools import sharpenImage, post_process
from skimage import transform as tf
from square_edge_detection import left_low_edge, left_top_edge, right_low_edge, right_top_edge, intersection_right

# to load the list of files
from os import listdir, mkdir, getcwd, rename
from os.path import isfile, join

# Get the name of the series

from gui import graphical_user_interface
seriesName = ''
possibility = listdir('./to_process/')[0].split('_')[0]
while seriesName == '':
    seriesName = graphical_user_interface(possibility)


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


def instaPrep(seriesName: str):
    # Load list of files
    file_list = [f for f in listdir('./to_process/')]
    print(file_list)
    file_list = [f for f in file_list if f.split('.')[1].lower() == 'jpg' and f.split('_')[0] == seriesName and f.split(
        '_')[-1].split('.')[0] != 'd' and (f.split('.')[0]+'_d.'+f.split('.')[1] not in file_list)]
    file_list = list(map(lambda x: x.split('.')[0], file_list))
    file_list.sort()
    nb = len(file_list)

    src_path = './to_process/'
    out_path = './processed/'+seriesName+'/'
    try:
        mkdir(out_path)
    except OSError:
        print("Creation of the directory %s failed" % out_path)
    else:
        print("Successfully created the directory %s " % out_path)

    if nb == 0:
        print('Aucune photo trouvée. Fin du processus.')

    if nb == 1:
        print('1 photo à traiter')
        digitalizeImage(seriesName, seriesName+'_1.jpg')

    if nb == 2:
        print('2 photos à traiter')
        # digitalize separately
        for i in range(1, 3):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            digitalizeImage(seriesName, seriesName+'_'+str(i)+'.jpg')

    if nb == 3:
        print('3 photos à traiter')
        # déterminer laquelle est le rectangle
        # digitalize separately
        for i in range(1, 4):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            digitalizeImage(seriesName, seriesName+'_'+str(i)+'.jpg')

    if nb == 4:
        print('4 photos à traiter')
        images = []
        # digitalize separately
        for i in range(1, 5):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            images.append(
                digitalizeImage(seriesName, seriesName+'_'+str(i)+'.jpg', True))
        # Merge
        merge4(seriesName, images[0], images[1], images[2], images[3])
    for i in range(nb):
        rename(src_path+seriesName+'_'+str(i+1)+'.jpg',
               out_path+seriesName+'_'+str(i+1)+'.jpg')


def digitalizeImage(seriesName, imgName, ROTATION=True):
    if ROTATION:
        print('Tentative de rotation')
    # Open the image form working directory
    imagePIL = Image.open('./to_process/'+imgName)
    imageGPIL = imagePIL.convert('L')

    # get the size of the image
    width = imagePIL.size[0]
    height = imagePIL.size[1]

    # matrixize and sharpen the image
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

    # find the square
    # on commence par le haut au milieu, on cherche le premier pixel noir
    found = False
    mid = width//2
    maxI = 0
    i = 100
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

    upperThreshold = maxI - 172

    found = False
    maxI = 0
    i = height - 101
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
    lowerThreshold = maxI + 172

    found = False
    mid = height//2
    maxJ = 0
    j = 100
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
    leftThreshold = maxJ - 172

    found = False
    maxJ = 0
    j = width-101
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
    rightThreshold = maxJ + 172

    # Find the edges
    leftTopEdge = left_top_edge(image, upperThreshold, width)
    rightTopEdge = right_top_edge(image, upperThreshold, width)
    rightLowerEdge = right_low_edge(image, lowerThreshold, width)
    leftLowerEdge = left_low_edge(image, lowerThreshold, width)

    upper_length = ((leftTopEdge[0]-rightTopEdge[0])
                    ** 2+(leftTopEdge[1]-rightTopEdge[1])**2)**(1/2)
    lower_length = ((leftLowerEdge[0]-rightLowerEdge[0])
                    ** 2+(leftLowerEdge[1]-rightLowerEdge[1])**2)**(1/2)
    left_length = ((leftTopEdge[0]-leftLowerEdge[0])
                   ** 2+(leftTopEdge[1]-leftLowerEdge[1])**2)**(1/2)
    right_length = ((rightLowerEdge[0]-rightTopEdge[0])
                    ** 2+(rightLowerEdge[1]-rightTopEdge[1])**2)**(1/2)

    # print('longueur côté haut : '+str(upper_length)+' pixels')
    # print('longueur côté bas : '+str(lower_length)+' pixels')
    # print('longueur côté gauche : '+str(left_length)+' pixels')
    # print('longueur côté droit : '+str(right_length)+' pixels')

    # Rotation
    # On considère la droite passant par les deux coins droits et on cherche son intersection avec l'horizontale passant par le coin en bas à gauche
    if ROTATION:
        # Right Lower Edge Angle
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
        b = is_D-jp_D*a

        right_intersection = [i_A, j_A-b/a]
        rightLowEdge_dist = ((right_intersection[0]-rightLowerEdge[0])**2 + (
            right_intersection[1]-rightLowerEdge[1])**2)**(1/2)
        #print(i_A, i_D)
        angleRLE = np.arctan(rightLowEdge_dist/lower_length)*180/np.pi
        if i_A < i_D:  # negative angle
            angleRLE *= -1

        #print('Lower angle: ' + str(angleRLE))

        # Left Top Edge Angle

        i_A = rightTopEdge[0]

        i_C = leftLowerEdge[0]
        i_D = leftTopEdge[0]
        j_A = rightTopEdge[1]
        j_C = leftLowerEdge[1]
        j_D = leftTopEdge[1]
        ip_C = i_C - i_A
        ip_D = i_D - i_A
        jp_C = -j_C + j_A
        jp_D = -j_D + j_A

        a = (ip_C-ip_D)/(jp_C-jp_D)
        b = ip_D-jp_D*a

        left_intersection = [i_A, j_A+b/a]
        # print(left_intersection)
        leftTopEdge_dist = ((left_intersection[0]-leftTopEdge[0])**2 + (
            left_intersection[1]-leftTopEdge[1])**2)**(1/2)

        angleLTE = np.arctan(leftTopEdge_dist/upper_length)*180/np.pi
        if i_A > i_D:  # negative angle
            angleLTE *= -1

        #print('upper angle: '+str(angleLTE))

        # Left Lower Edge Angle
        i_A = leftTopEdge[0]
        i_C = rightLowerEdge[0]
        i_D = leftLowerEdge[0]
        j_A = leftTopEdge[1]
        j_C = rightLowerEdge[1]
        j_D = leftLowerEdge[1]
        ip_C = j_C - j_A
        ip_D = j_D - j_A
        jp_C = i_C - i_A
        jp_D = i_D - i_A

        a = (ip_C-ip_D)/(jp_C-jp_D)
        b = ip_D-jp_D*a

        left_intersection = [i_A-b/a, j_A]
        # print(left_intersection)
        leftTopEdge_dist = ((left_intersection[0]-leftLowerEdge[0])**2 + (
            left_intersection[1]-leftLowerEdge[1])**2)**(1/2)
        angleLLE = np.arctan(leftTopEdge_dist/left_length)*180/np.pi
        if j_A > j_D:  # negative angle
            angleLLE *= -1

        #print('left angle: '+str(angleLLE))

        # Right Lower Edge Angle
        i_A = rightLowerEdge[0]
        i_C = leftTopEdge[0]
        i_D = rightTopEdge[0]
        j_A = rightLowerEdge[1]
        j_C = leftTopEdge[1]
        j_D = rightTopEdge[1]
        ip_C = -j_C + j_A
        ip_D = -j_D + j_A
        jp_C = -i_C + i_A
        jp_D = -i_D + i_A

        a = (ip_C-ip_D)/(jp_C-jp_D)
        b = ip_D-jp_D*a

        right_intersection = [i_A+b/a, j_A]
        # print(right_intersection)
        rightLowerEdge_dist = ((right_intersection[0]-rightTopEdge[0])**2 + (
            right_intersection[1]-rightTopEdge[1])**2)**(1/2)
        angleRTE = np.arctan(rightLowerEdge_dist/right_length)*180/np.pi
        if j_A < j_D:  # negative angle
            angleRTE *= -1

        #print('right angle: '+str(angleRTE))

    else:
        angleRLE = 0
        angleLTE = 0
        angleLLE = 0
        angleRTE = 0

    # Looking for absurd values

    angles = [angleLLE, angleLTE, angleRLE, angleRTE]
    rotation_angle = 0
    meanLLE = angleLTE/3 + angleRLE/3 + angleRTE/3
    meanLTE = angleLLE/3 + angleRLE/3 + angleRTE/3
    meanRLE = angleLLE/3 + angleLTE/3 + angleRTE/3
    meanRTE = angleLLE/3 + angleLTE/3 + angleRLE/3

    if (abs(abs(angleLLE)) > 2*abs(meanLLE)) or (abs(angleLLE) < 1/2*abs(meanLLE)):
        angles.pop(0)
    if (abs(abs(angleLTE)) > 2*abs(meanLTE)) or (abs(angleLTE) < 1/2*abs(meanLTE)):
        angles.pop(1)
    if (abs(abs(angleRLE)) > 2*abs(meanRLE)) or (abs(angleRLE) < 1/2*abs(meanRLE)):
        angles.pop(-2)
    if (abs(abs(angleRTE)) > 2*abs(meanRTE)) or (abs(angleRTE) < 1/2*abs(meanRTE)):
        angles.pop(-1)

    if (angleLLE > 0 and angleLTE > 0 and angleRLE > 0 and angleRTE > 0) or (angleLLE < 0 and angleLTE < 0 and angleRLE < 0 and angleRTE < 0):
        rotation_angle = - sum(angles)/len(angles)

    # Crop and sharpen the image
    leftBorder = min(leftLowerEdge[1], leftTopEdge[1], leftThreshold+172)-172
    rightBorder = max(rightLowerEdge[1],
                      rightTopEdge[1], rightThreshold-172)+172
    upperBorder = min(rightTopEdge[0], leftTopEdge[0], upperThreshold+172)-172
    lowerBorder = max(leftLowerEdge[0],
                      rightLowerEdge[0], lowerThreshold-172)+172

    box = (leftBorder, upperBorder, rightBorder,
           lowerBorder)  # left upper right lower
    white = (255, 255, 255)
    imagePIL = imagePIL.rotate(rotation_angle,
                               fillcolor=white).crop(box).resize((2800, 2800))
    imageGPIL = imagePIL.convert('L')
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

    width = 2800
    height = 2800

# find the square
    # on commence par le haut au milieu, on cherche le premier pixel noir
    found = False
    mid = width//2
    maxI = 0
    i = 150
    while not found and i < height - 150:
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

    upperThreshold = maxI-172

    found = False
    maxI = 0
    i = height - 150
    while not found and i > upperThreshold + 150:
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
    lowerThreshold = maxI + 172

    found = False
    mid = height//2
    maxJ = 0
    j = 150
    while not found and j < width-150:
        if isBlack(image[mid][j]):
            #print(mid, j)
            i = -round(height/40)
            stop = False
            while not stop and i < round(height/40):
                foundI = False
                varJ = -round(width/50)
                while not foundI and varJ < round(width/50):
                    foundI = isBlack(image[mid+i][j+varJ])
                    #print(i+mid,j+varJ,foundI, image[mid+i][j+varJ])
                    varJ += 1
                # si on a pas trouvé de noir dans le rectangle, c'est pas un trait du carré
                stop = not foundI
                # print(stop)
                if foundI:
                    maxJ = j
                i += 1
            if not stop:
                found = True
        j += 1
    leftThreshold = maxJ - 172

    found = False
    maxJ = 0
    j = width-101
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
                if foundI:
                    maxJ = j
                i += 1
            if not stop:
                found = True
        j -= 1
    rightThreshold = maxJ + 172

    # imagePIL.save('./processed/'+seriesName+'/' +
    #              imgName.split('.')[0].split('_')[1]+'_bt.jpg')

    # print(leftThreshold)
    # print(rightThreshold)
    # print(upperThreshold)
    # print(lowerThreshold)

    leftTopEdge = left_top_edge(image, upperThreshold, 2800)
    rightTopEdge = right_top_edge(image, upperThreshold, 2800)
    rightLowerEdge = right_low_edge(image, lowerThreshold, 2800)
    leftLowerEdge = left_low_edge(image, lowerThreshold, 2800)

    # print(leftTopEdge)
    # print(rightTopEdge)
    # print(rightLowerEdge)
    # print(leftLowerEdge)

    image = np.array(imagePIL)
    dst = np.array([leftTopEdge[::-1], rightTopEdge[::-1],
                    rightLowerEdge[::-1], leftLowerEdge[::-1]])
    src = np.array([[170, 170][::-1], [170, 2630][::-1],
                    [2630, 2630][::-1], [2630, 170][::-1]])
    # print(src)
    # print(dst)
    tform = tf.ProjectiveTransform()
    tform.estimate(src, dst)
    image = tf.warp(image/255, tform, output_shape=(2800, 2800), cval=1)*255

    imagePIL = Image.fromarray(np.uint8(image)).convert('RGB')
    # imagePIL.save('./processed/'+seriesName+'/' +
    #              imgName.split('.')[0].split('_')[1]+'_t.jpg')
    imageGPIL = imagePIL.convert('L')

    width = imagePIL.size[0]
    height = imagePIL.size[1]
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

    #newImage = np.ones((2800, 2800, 3))*255

    # Build the new image

    image[image[:,:,0]+image[:,:,1]+image[:,:,2]>500] = [255, 255, 255]
    image = post_process(image)

    numImagePIL = Image.fromarray(image.astype('uint8'), 'RGB')

    signaturePIL = Image.open('./signature/signature.jpg').resize((75, 505))
    box = (2800-172-50-60, 2800-172-50-505, 2800-172-35, 2800-172-50)
    numImagePIL.paste(signaturePIL, box)
    numImagePIL.save('./processed/'+seriesName+'/' +
                     imgName.split('.')[0].split('_')[1]+'.jpg')
    return image


def merge4(seriesName, image1, image2, image3, image4):
    print('Assemblage')
    box1 = (95, 95, 1363, 1363)  # include centering (172/2=86)
    box2 = (1437, 95, 2705, 1363)
    box3 = (95, 1437, 1363, 2705)
    box4 = (1437, 1437, 2705, 2705)
    image1PIL = Image.fromarray(image1.astype('uint8'), 'RGB').resize(
        (1400, 1400)).crop((66, 66, 1400-66, 1400-66))
    image2PIL = Image.fromarray(image2.astype('uint8'), 'RGB').resize(
        (1400, 1400)).crop((66, 66, 1400-66, 1400-66))
    image3PIL = Image.fromarray(image3.astype('uint8'), 'RGB').resize(
        (1400, 1400)).crop((66, 66, 1400-66, 1400-66))
    image4PIL = Image.fromarray(image4.astype('uint8'), 'RGB').resize(
        (1400, 1400)).crop((66, 66, 1400-66, 1400-66))
    newImage = np.ones((2800, 2800, 3))*255
    newImagePIL = Image.fromarray(newImage.astype('uint8'), 'RGB')

    signaturePIL = Image.open('./signature/signature.jpg').resize((75, 505))
    boxs = (2800-115-50-50, 2800-115-505-10, 2800-115-25, 2800-115-10)

    newImagePIL.paste(image1PIL, box1)
    newImagePIL.paste(image2PIL, box2)
    newImagePIL.paste(image3PIL, box3)
    newImagePIL.paste(image4PIL, box4)
    newImagePIL.paste(signaturePIL, boxs)
    newImagePIL.save('./processed/'+seriesName+'/'+seriesName+'.jpg')


instaPrep(seriesName)
