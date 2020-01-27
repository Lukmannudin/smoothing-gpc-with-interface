import numpy as np
import cv2
import math

class FilterMedian:

    def __init__(self):
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
        return 20 * np.log10((PIXEL_MAX) / math.sqrt(mse))

    def psnrResult(self):
        #open result
        img_result_path = 'imageresults/result_median.jpg'
        img_result = cv2.imread(img_result_path)
        #open upload
        im_upload_path = 'imageuploads/original_image.jpg'
        img_upload = cv2.imread(im_upload_path)

        psnr_scratch = self.psnr(img_upload, img_result)
        return psnr_scratch

    def main(self,filterSize):
        im1_path = 'imagenoise/test_noise_added.jpg'
        self.set_im1_path(im1_path)
        img1 = cv2.imread(im1_path, 0)
        
        #run filter
        print("ini: "+filterSize+ 'end')
        filter_size = 3
        removed_noise = self.median_filter(img1, int(filter_size))

        #save image
        im_result_path = 'imageresults/result_median.jpg'
        cv2.imwrite(im_result_path,removed_noise)

        
        

# main()