import numpy as np
import cv2
import math

class FilterMedianSize:


    def __init__(self, path):
        self.baseUrl = "E:/[1]OfflineTugas/GPC/smoothing-gpc-with-interface/"
        self.fileNameResult = "result_median.jpg"
        self.originalImage = "original_image.jpg"
        self.im1_path = ''
        self.im_result_path = ''
        self.im_upload_path = ''

    def set_im1_path(self, fileName):
        self.im1_path = fileName
    def get_im1_path(self):
        return self.im1_path   

    def median_filter(self, data, filter_size):
        temp = []
        indexer = filter_size // 2
        data_final = []
        data_final = np.zeros((len(data),len(data[0])))
        for i in range(len(data)):

            for j in range(len(data[0])):

                for z in range(filter_size):
                    if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                        for c in range(filter_size):
                            temp.append(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                            temp.append(0)
                        else:
                            for k in range(filter_size):
                                temp.append(data[i + z - indexer][j + k - indexer])

                temp.sort()
                data_final[i][j] = temp[len(temp) // 2]
                temp = []
        return data_final

    def psnr(self, img1, img2):
        mse = np.mean( (img1 - img2) ** 2 )
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 10 * np.log10((PIXEL_MAX)**2 / (mse))

    def psnrResult(self):
        #open result
        img_result_path = self.baseUrl+'imageresults/'+self.fileNameResult
        img_result = cv2.imread(img_result_path, 0)
        # #open upload
        im_upload_path = self.baseUrl+'imageuploads/'+self.originalImage
        img_upload = cv2.imread(im_upload_path, 0)

        psnr_scratch = self.psnr(img_upload, img_result)
        return psnr_scratch

    def main(self,filterSize = 3):
        im1_path = self.baseUrl+'imagenoise/test_noise_added.jpg'
        self.set_im1_path(im1_path)
        img1 = cv2.imread(im1_path, 0)
        
        #run filter
        # filter_size = 3
        removed_noise = self.median_filter(img1, int(filterSize))

        #save image
        im_result_path = self.baseUrl+'imageresults/'+self.fileNameResult
        cv2.imwrite(im_result_path,removed_noise)


# main()