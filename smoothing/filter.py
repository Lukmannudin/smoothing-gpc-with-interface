# © Copyright lexmanuel.com :: Alexander M S 


#import and get image data
import matplotlib.pyplot  as plt
import matplotlib.image as img
import numpy as np
import cv2 #for comparing manual and using cv2 library

image_path = 'test.jpg'
# image_path = '/content/Lenna_(test_image).png'
image = img.imread(image_path)

# #print(image)
# plt.imshow(image)

#Convolution without library
def conv(image, kernel):

  image_h = image.shape[0]
  image_w = image.shape[1]

  kernel_h = kernel.shape[0]
  kernel_w = kernel.shape[1]

  h = kernel_h//2
  w = kernel_w//2

  image_conv = np.zeros(image.shape)

  for i in range(h, image_h-h):
    for j in range(w, image_w-w):
      sum = 0

      for m in range(kernel_h):
        for n in range(kernel_w):
          sum = sum + kernel[m][n]*image[i-h+m][j-w+n]
      image_conv[i][j] = sum

  plt.subplot(1,2,1)
  plt.imshow(image)
  plt.title('Original Image')

  plt.subplot(1,2,2)
  plt.imshow(image_conv)
  plt.title('Filtered Image')
  plt.show()

#List of Matrices
sharpen = np.array([ [0,-1,0],
                    [-1,5,-1],
                    [0,-1,0]], np.float32)

gaus_blur = 1/9 * np.array([[1,1,1],
                            [1,1,1],
                            [1,1,1]], np.float32)

edge_detection = np.array([[-1,-1,-1],
                            [-1,-8,-1],
                            [-1,-1,-1]], np.float32)



def convolve_np(X, F):
    X_height = X.shape[0]
    X_width = X.shape[1]

    F_height = F.shape[0]
    F_width = F.shape[1]
    
    H = int((F_height - 1) / 2)
    W = int((F_width - 1) / 2)
    
    out = np.zeros((X_height, X_width))
    
    for i in np.arange(H, X_height-H):
        for j in np.arange(W, X_width-W):
            sum = 0
            for k in np.arange(-H, H+1):
                for l in np.arange(-W, W+1):
                    x = i+k
                    y = j+l
                    a = X.getpixel((int(y), int(x)))
                    w = F[H+k, W+l]
                    sum += (w * a)
            out[i,j] = sum
    
    return out

#Convolution without library
convolve_np(image,gaus_blur)

#using library

img_library = cv2.filter2D(image, -1, gaus_blur)
plt.subplot(1,2,1)
plt.imshow(image)
plt.title('Original Image')
  
plt.subplot(1,2,2)
plt.imshow(img_library)
plt.title('Filtered Image')
plt.show()