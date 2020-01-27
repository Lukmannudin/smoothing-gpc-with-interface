import numpy as np
from PIL import Image

class FilterMedian:

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


    # def log10(self,x):
    #     numerator = tf.math.log(x)
    #     denominator = tf.math.log(tf.constant(10, dtype=numerator.dtype))
    #     return numerator / denominator


    def main(self,fileName):
        img = Image.open("/home/codelabs/ngulik/python/microblog/imageuploads/"+fileName).convert("L")
        arr = np.array(img)
        filter_size = 3
        removed_noise = self.median_filter(arr, filter_size) 
        img = Image.fromarray(removed_noise)
        img = img.convert('L')
        img.save('/home/codelabs/ngulik/python/microblog/imageresults/medianresult.png', "png")
        

# main()