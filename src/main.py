#   gérer 2,3 images
# comments
# ne pas tout retransformer en jpg si ça l'est déjà

# load images with Pillow
from gui import graphical_user_interface
from PIL import Image
import numpy as np
from imageTools import sharpenImage, post_process
from skimage import transform as tf

from square_edge_detection import upper_threshold, lower_threshold, left_threshold, right_threshold
from square_edge_detection import left_low_edge, left_top_edge, right_low_edge, right_top_edge

# to load the list of files
from os import listdir, mkdir, getcwd, rename
from os.path import isfile, join

# Get the name of the series


def isBlack(arr):
    var = int(arr[0])+int(arr[1])+int(arr[2])
    return (var < 320) and arr[0] < 120 and arr[1] < 120 and arr[2] < 120


def isWhite(arr):
    var = int(arr[0])+int(arr[1])+int(arr[2])
    return (var > 400)


def instaPrep(series_name: str, apple_correction=True, perspective_correction=True, verbose=False, steps=False):
    """
    Function which prepares the different cartoons according to the situation.
    """

    # Load list of files
    file_list = [f for f in listdir('./to_process/')]
    file_list = [f for f in file_list if f.split('.')[1].lower() == 'jpg' and f.split('_')[0] == series_name and f.split(
        '_')[-1].split('.')[0] != 'd' and (f.split('.')[0]+'_d.'+f.split('.')[1] not in file_list)]
    file_list = list(map(lambda x: x.split('.')[0], file_list))
    file_list.sort()
    nb = len(file_list)

    src_path = './to_process/'
    out_path = './processed/'+series_name+'/'
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
        digitalizeImage(series_name, series_name+'_1.jpg',
                        apple_correction, perspective_correction, verbose, steps)

    if nb == 2:
        print('2 photos à traiter')
        # digitalize separately
        for i in range(1, 3):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            digitalizeImage(series_name, series_name+'_'+str(i)+'.jpg',
                            apple_correction, perspective_correction, verbose, steps)

    if nb == 3:
        print('3 photos à traiter')
        # déterminer laquelle est le rectangle
        # digitalize separately
        for i in range(1, 4):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            digitalizeImage(series_name, series_name+'_'+str(i)+'.jpg',
                            apple_correction, perspective_correction, verbose, steps)

    if nb == 4:
        print('4 photos à traiter')
        images = []
        # digitalize separately
        for i in range(1, 5):
            print('Photo '+str(i)+' en traitement. Veuillez patienter.')
            images.append(
                digitalizeImage(series_name, series_name+'_'+str(i)+'.jpg',  apple_correction, perspective_correction, verbose, steps))
        # Merge
        merge4(series_name, images[0], images[1], images[2], images[3])
    """for i in range(nb):
        rename(src_path+series_name+'_'+str(i+1)+'.jpg',
               out_path+series_name+'_'+str(i+1)+'.jpg')"""


def digitalizeImage(series_name, imgName,  apple_correction=True, perspective_correction=True, verbose=False, steps=False):
    """
    Function which prepares a cartoon doing the following steps:
        - finding the borders and edges and cropping with a 172pix padding
        - finding if the image is rotated and to which angle, and rotating it back
        - correcting the perspective effects
        - applying a "digitalizing" filter to the image

    Input:
        - series_name: (str) name of the cartoon series
        - imgName: (str) number of the image in the series
        - perpective_correction: (bool) 
        - verbose: (bool) 
        - steps: (bool)

    Output: 
        - image: (np.array((2800, 2800))) "digitalized" image    

    """

    # Open the image form working directory
    imagePIL = Image.open('./to_process/'+imgName)
    imageGPIL = imagePIL.convert('L')

    # get the size of the image
    width = imagePIL.size[0]
    height = imagePIL.size[1]

    # matrixize and sharpen the image
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

    if not perspective_correction:
        upperThreshold = upper_threshold(image, height, width)
        lowerThreshold = lower_threshold(image, upperThreshold, height, width)
        leftThreshold = left_threshold(image, height, width)
        rightThreshold = right_threshold(image, leftThreshold, height, width)

        if steps:
            Image.fromarray(image.astype('uint8'), 'RGB').save('./processed/'+series_name+'/' +
                                                               imgName.split('.')[0].split('_')[1]+'_bc.jpg')

        if verbose:
            print('upper limit: ' + str(upperThreshold+172))
            print('lower limit: ' + str(lowerThreshold-172))
            print('left limit: ' + str(leftThreshold+172))
            print('right limit: ' + str(rightThreshold-172))

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

        if verbose:
            print('longueur côté haut : '+str(upper_length)+' pixels')
            print('longueur côté bas : '+str(lower_length)+' pixels')
            print('longueur côté gauche : '+str(left_length)+' pixels')
            print('longueur côté droit : '+str(right_length)+' pixels')

        # Crop and sharpen the image #A CHANGER
        leftBorder = min(leftLowerEdge[1], leftTopEdge[1], leftThreshold+172)-8
        rightBorder = max(rightLowerEdge[1],
                          rightTopEdge[1], rightThreshold-172)+8
        upperBorder = min(
            rightTopEdge[0], leftTopEdge[0], upperThreshold+172)-8
        lowerBorder = max(leftLowerEdge[0],
                          rightLowerEdge[0], lowerThreshold-172)+8

        box = (leftBorder, upperBorder, rightBorder,
               lowerBorder)  # left upper right lower

        imagePIL = imagePIL.crop(box).resize((2472, 2472))

        background = np.ones((2800, 2800, 3))*255
        backgroundPIL = Image.fromarray(background.astype('uint8'), 'RGB')
        box = (164, 164, 2636, 2636)
        backgroundPIL.paste(imagePIL, box)

        imagePIL = backgroundPIL
        if steps:
            imagePIL.save('./processed/'+series_name+'/' +
                          imgName.split('.')[0].split('_')[1]+'_c.jpg')

        imageGPIL = imagePIL.convert('L')
        image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

        width = 2800
        height = 2800

    if perspective_correction:
        height = 2800
        width = 2800
        imagePIL = Image.open(
            './to_process/'+imgName).resize((2800, 2800), Image.LANCZOS)
        imageGPIL = imagePIL.convert('L')

        if apple_correction:
            if verbose:
                print('Correction de la rotation apple')
            imagePIL = imagePIL.rotate(90).rotate(180)
            if steps:
                imagePIL.save('./processed/'+series_name+'/' +
                              imgName.split('.')[0].split('_')[1]+'_r.jpg')
        imageGPIL = imagePIL.convert('L')
        image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)
        if steps:
            imagePIL = Image.fromarray(np.uint8(image)).convert('RGB')
            imagePIL.save('./processed/'+series_name+'/' +
                          imgName.split('.')[0].split('_')[1]+'_rs.jpg')
        # find the square
        # on commence par le haut au milieu, on cherche le premier pixel noir
        upperThreshold = upper_threshold(image, height, width)
        lowerThreshold = lower_threshold(image, upperThreshold, height, width)
        #left_upper_threshold = left_threshold(image, height, width, -15)
        #left_lower_threshold = left_threshold(image, height, width, 15)
        #right_upper_threshold = right_threshold(image, leftThreshold, height, width, -15)
        #right_lower_threshold = right_threshold(image, leftThreshold, height, width, 15)
        if verbose:
            print('upper limit: ' + str(upperThreshold+172))
            print('lower limit: ' + str(lowerThreshold-172))
            #print('left lower limit: ' + str(leftThreshold+172))
            #print('left upper limit: ' + str(leftThreshold+172))
            #print('right lower limit: ' + str(rightThreshold-172))
            #print('right upper limit: ' + str(rightThreshold-172))

        leftTopEdge = left_top_edge(image, upperThreshold, 2800)
        rightTopEdge = right_top_edge(image, upperThreshold, 2800)
        rightLowerEdge = right_low_edge(image, lowerThreshold, 2800)
        leftLowerEdge = left_low_edge(image, lowerThreshold, 2800)

        # Correcting the perspective
        image = np.array(imagePIL)
        dst = np.array([leftTopEdge[::-1], rightTopEdge[::-1],
                        rightLowerEdge[::-1], leftLowerEdge[::-1]])
        src = np.array([[170, 170][::-1], [170, 2630][::-1],
                        [2630, 2630][::-1], [2630, 170][::-1]])

        if verbose:
            print('Points réels:\n' + str(dst))
            print('Points théoriques:\n' + str(src))

        tform = tf.ProjectiveTransform()
        tform.estimate(src, dst)
        image = tf.warp(image/255, tform,
                        output_shape=(2800, 2800), cval=1, order=3)*255

    imagePIL = Image.fromarray(np.uint8(image)).convert('RGB')

    if steps:
        print('Saving after transform.')
        # save the image after the homographic transform
        imagePIL.save('./processed/'+series_name+'/' +
                      imgName.split('.')[0].split('_')[1]+'_t.jpg')

    imageGPIL = imagePIL.convert('L')

    width = imagePIL.size[0]
    height = imagePIL.size[1]
    image = sharpenImage(imagePIL, imageGPIL, 0.75, 15)

    # Extract red part of the image
    red_image = np.zeros((2800, 2800, 3))
    red_image = np.copy(image)
    red_image[red_image[:, :, 0] < 40 +
              (red_image[:, :, 1]+red_image[:, :, 2])/2] = [0, 0, 0]
    image[image[:, :, 0] > 40 +
          (image[:, :, 1]+image[:, :, 2])/2] = [0, 0, 0]
    if steps:
        # Save the red part image
        red_imagePIL = Image.fromarray(red_image.astype('uint8'), 'RGB')
        red_imagePIL.save('./processed/'+series_name+'/' +
                          imgName.split('.')[0].split('_')[1]+'_rt.jpg')

    # Build the new image adding the red part
    image = post_process(image)
    image = image + red_image

    numImagePIL = Image.fromarray(image.astype('uint8'), 'RGB')
    image = np.array(numImagePIL)

    signaturePIL = Image.open(
        './src/signature/signature.jpg').resize((75, 505))
    box = (2800-172-50-60, 2800-172-50-505, 2800-172-35, 2800-172-50)
    numImagePIL.paste(signaturePIL, box)
    numImagePIL.save('./processed/'+series_name+'/' +
                     imgName.split('.')[0].split('_')[1]+'.jpg')
    return image


def merge4(series_name, image1, image2, image3, image4):
    if verbose:
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

    signaturePIL = Image.open(
        './src/signature/signature.jpg').resize((75, 505))
    boxs = (2800-115-50-50, 2800-115-505-10, 2800-115-25, 2800-115-10)

    newImagePIL.paste(image1PIL, box1)
    newImagePIL.paste(image2PIL, box2)
    newImagePIL.paste(image3PIL, box3)
    newImagePIL.paste(image4PIL, box4)
    newImagePIL.paste(signaturePIL, boxs)
    newImagePIL.save('./processed/'+series_name+'/'+series_name+'.jpg')


series_name = ''
file_names = listdir('./to_process/')
file_names = list(set(map(lambda x: x.split('_')[0], file_names)))

if len(file_names) >= 1:
    while series_name == '':
        series_name, apple_correction, perspective_correction, verbose, steps = graphical_user_interface(
            file_names)
    instaPrep(series_name, apple_correction,
              perspective_correction, verbose, steps)
else:
    print("Aucune image trouvée.\nVeuillez ajouter des images dans le dossier './to_process'")
