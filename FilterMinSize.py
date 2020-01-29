import numpy as np
import math
import cv2

class FilterMinSize:
    def __init__(self, path):
        self.baseUrl = ""
        self.fileNameResult = "result_min.jpg"
        self.originalImage = "original_image.jpg"
        self.im1_path = ''
        self.im_result_path = ''
        self.im_upload_path = ''

    def set_im1_path(self, fileName):
        self.im1_path = fileName
    def get_im1_path(self):
        return self.im1_path   

    def min_filter(self,data, filter_size):
        self.baseUrl = "smoothing-gpc-with-interface/"
        img_out = data.copy()
        height = data.shape[0]
        width = data.shape[1]

        for i in np.arange(3, height-3):
            for j in np.arange(3, width-3):
                min = 255
                for k in np.arange(-3, 4):
                    for l in np.arange(-3, 4):
                        a = data.item(i+k, j+l)
                        if a < min:
                            min = a
                b = min
                img_out.itemset((i,j), b)

        return img_out

    def psnr(self, img1, img2):
        mse = np.mean( (img1 - img2) ** 2 )
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 10 * np.log10((PIXEL_MAX)**2 / (mse))
    def psnrResult(self):
        #open result
        img_result_path = 'imageresults/'+self.fileNameResult
        img_result = cv2.imread(img_result_path)
        print('link:',img_result_path)
        #open upload
        im_upload_path = 'imageuploads/'+self.originalImage
        img_upload = cv2.imread(im_upload_path)

        psnr_scratch = self.psnr(img_upload, img_result)
        return psnr_scratch

    def main(self, filterSize = 3):
        im1_path = 'imagenoise/test_noise_added.jpg'
        img1 = cv2.imread(im1_path, 0)

        #run filter
        # filter_size = 3
        removed_noise = self.min_filter(img1, filterSize)

        #save image
        im_result_path = 'imageresults/'+self.fileNameResult
        
        cv2.imwrite(im_result_path,removed_noise)