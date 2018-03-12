import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import sys
from time import time

def check_usage(script_name):
  if len(sys.argv) != 2:
    print ("Usage: python %s.py <filename>" % script_name)
    exit(1)

def read_image():
  filename = sys.argv[1]
  if not os.path.isfile(filename):
    print ("No such file:", filename)
    exit(1)

  img = cv2.imread(filename)
  gray = np.float32(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY))
  return img, gray




def generate_gradient_matrix(src, blockSize, ksize, k, score):  # ksize sobel size to find gradient

  size_y, size_x = src.shape

  # Return value of the method
  scored_image_gradient = np.zeros(src.shape)
  gradient_x = cv2.Sobel(src, cv2.CV_32F, 1, 0, ksize=ksize) ### 1(derivate order in x)  
  gradient_y = cv2.Sobel(src, cv2.CV_32F, 0, 1, ksize=ksize) 

  gradient_xx = np.square(gradient_x)
  gradient_yy = np.square(gradient_y)
  gradient_xy = np.multiply(gradient_x, gradient_y)
  for y in range(size_y): 
    oy = time()
    for x in range(size_x):
      M = np.zeros((2, 2))


      ymin = max(0, y - blockSize / 2)
      ymax = min(size_y, y + blockSize / 2)
      xmin = max(0, x - blockSize / 2)
      xmax = min(size_x, x + blockSize / 2)

      

      for v in range(int(ymin), int(ymax)):
        for u in range(int(xmin), int(xmax)):
          M[0, 0] += gradient_xx[v,u]
          M[0, 1] += gradient_xy[v,u]
          M[1, 1] += gradient_yy[v,u]
      M[1, 0] = M[0, 1]


      scored_image_gradient[y, x] = score(M)


  return scored_image_gradient


