# à commenter
from scipy.ndimage import gaussian_filter
# load and show an image with Pillow
from PIL import Image
import numpy as np
# Open the image form working directory


def relu(x):
    """
    linear function between 90/255 and 1
    """
    return 255/165*x-90/165


def sharpenImage(imagePIL, imageGPIL, amount=0.75, sigma=15):
    """
    Enhance and sharpen the image before further processing.
    Input:
    - imagePIL: PIL.Image 
    - imageGPIL: PIL.Image Grayscale image
    - amount: (float)
    - sigma: (int) 
    Output:
    - image: List(List(int)) modified (whitened) image
    """
    imageG = np.array(imageGPIL)/255
    image = np.array(imagePIL)/255
    blurredGImage = gaussian_filter(imageG, sigma)
    sub = imageG - blurredGImage
    sub3 = np.stack([sub, sub, sub], axis=2)*amount
    image = (image + sub3)*255
    image[image > 255] = 255
    image[image < 0] = 0
    return image.astype(int)


def post_process(image):
    """
    Detect white pixels and avoid overlapping.
    Input:
    - image: List(List(int))
    Output:
    - image: List(List(int)) modified (whitened) image
    """
    image[image[:, :, 0]+image[:, :, 1] +
                  image[:, :, 2] > 400] = [255, 255, 255]
    image = relu(image/255)*255
    image[image > 255] = 255
    image[image < 90] = 0
    return image
