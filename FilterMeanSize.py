import numpy as np
import math
from cv2 import cv2

class FilterMeanSize:
    def __init__(self, path):
        self.baseUrl = "/home/codelabs/ngulik/python/smoothing-gpc-with-interface/"
        # self.fileNameResult = "result_median.jpg"
        # self.originalImage = "original_image.jpg"

    def mean_filter(self, data, filter_size):
        img_out = data.copy()

        height = data.shape[0]
        width = data.shape[1]
        for i in np.arange(3, height-3):
            for j in np.arange(3, width-3):        
                sum = 0
                for k in np.arange(-3, 4):
                    for l in np.arange(-3, 4):
                        a = data.item(i+k, j+l)
                        sum = sum + a
                b = int(sum / 49.0)
                img_out.itemset((i,j), b)
        return img_out

    def psnr(self, img1, img2):
        mse = np.mean( (img1 - img2) ** 2 )
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * np.log10((PIXEL_MAX) / math.sqrt(mse))

    def psnrResult(self):
        # open result
        img_result_path = self.baseUrl +'imageresults/result_mean.jpg'
        img_result = cv2.imread(img_result_path)
        #open upload
        im_upload_path = self.baseUrl +'imageuploads/original_image.jpg'
        img_upload = cv2.imread(im_upload_path)

        psnr_scratch = self.psnr(img_upload, img_result)
        return psnr_scratch

    def main(self, filterSize = 3):
        im1_path = self.baseUrl +'imagenoise/test_noise_added.jpg'
        img1 = cv2.imread(im1_path, 0)

        #run filter
        # filter_size = 3
        removed_noise = self.mean_filter(img1, filterSize)

        #save image
        im_result_path = self.baseUrl +'imageresults/result_mean.jpg'
        cv2.imwrite(im_result_path,removed_noise)
