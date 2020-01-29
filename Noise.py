import cv2
import numpy as np
from skimage.util import random_noise


class Noise:

    def addNoise(self, fileType):
        img = cv2.imread('imageuploads/original_image.'+fileType, 0)

        img_noise = random_noise(img, mode='s&p',amount=0.3)
        img_noise = np.array(255*img_noise, dtype = 'uint8')

        img_noise_path = 'imagenoise/test_noise_added.'+"jpg"
        cv2.imwrite(img_noise_path,img_noise)