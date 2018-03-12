import numpy
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from scipy import misc
from scipy import ndimage
import math
import cv2
def scaleSpectrum(A):
   return numpy.real(numpy.log10(numpy.absolute(A) + numpy.ones(A.shape)))


# sample values from a spherical gaussian function from the center of the image
def makeGaussianFilter(numRows, numCols, sigma, highPass):
   centerI = int(numRows/2) + 1 if numRows % 2 == 1 else int(numRows/2)
   centerJ = int(numCols/2) + 1 if numCols % 2 == 1 else int(numCols/2)

   def gaussian(i,j):
      coefficient = math.exp(-1.0 * ((i - centerI)**2 + (j - centerJ)**2) / (2 * sigma**2))
      return 1 - coefficient if highPass else coefficient

   return numpy.array([[gaussian(i,j) for j in range(numCols)] for i in range(numRows)])


def filterDFT(imageMatrix, filterMatrix):
   shiftedDFT = fftshift(fft2(imageMatrix))
   misc.imsave("dft.png", scaleSpectrum(shiftedDFT))

   filteredDFT = shiftedDFT * filterMatrix
   misc.imsave("filtered-dft.png", scaleSpectrum(filteredDFT))
   #return ifft2(ifftshift(filteredDFT))
   return (ifftshift(filteredDFT))


def lowPass(imageMatrix, sigma):
   n,m = imageMatrix.shape
   return filterDFT(imageMatrix, makeGaussianFilter(n, m, sigma, highPass=False))


def highPass(imageMatrix, sigma):
   n,m = imageMatrix.shape
   return filterDFT(imageMatrix, makeGaussianFilter(n, m, sigma, highPass=True))
def extra(Img1,Img2,Img3,sigma1,sigma2,sigma3,flag):
	if(flag==1):
		highPassed=highPass(Img1,sigma1)
		highPassed1=highPass(Img2,sigma2)
		lowPassed=lowPass(Img3,sigma3)
		result=numpy.array(abs(ifft2(highPassed + highPassed1+ lowPassed))).astype(numpy.uint8)
	if(flag==2):
		lowPassed=lowPass(Img1,sigma1)
		lowPassed1=lowPass(Img2,sigma2)
		highPassed=highPass(Img3,sigma3)
		result=numpy.array(abs(ifft2(lowPassed + lowPassed1+ highPassed))).astype(numpy.uint8)
	return cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)
def hybridImage(highFreqImg, lowFreqImg, sigmaHigh, sigmaLow):
   highPassed = highPass(highFreqImg, sigmaHigh)
   lowPassed = lowPass(lowFreqImg, sigmaLow)

   result=numpy.array(abs(ifft2(highPassed + lowPassed))).astype(numpy.uint8)
   return cv2.cvtColor(result,cv2.COLOR_GRAY2RGB)

if __name__ == "__main__":
   print("main_hybrid_image")
   print("available_images")
   L=["Afghan_girl_after.jpg","Afghan_girl_before.jpg","bicycle.bmp","bird.bmp","cat.bmp","dog.bmp","einstein.bmp","fish.bmp","makeup_after.jpg","makeup_before.jpg","marilyn.bmp","motorcycle.bmp","plane.bmp","submarine.bmp"]
   for num,value in enumerate(L):
   	print(num,value)
   print("Select num from above available_images as highpass_image")
   j=input()
   Image_H = ndimage.imread("HW1_Data/HW1_Q1/"+L[int(j)], flatten=True)
   print("Select num from above available_images as lowpass_image")
   j=input()
   Image_L = ndimage.imread("HW1_Data/HW1_Q1/"+L[int(j)], flatten=True)
   #Image_H1 = ndimage.imread("HW1_Data/HW1_Q1/bicycle.bmp", flatten=True)
   ### resizing images
   width_,height_=Image_H.shape
   Image_L = cv2.resize(Image_L, (height_, width_)) 
   print("Enter αlpha(high pass cutoff) :")
   alpha=input()
   print("Enter βeta(low pass cutoff) :")
   beta=input()
   hybrid = hybridImage(Image_H, Image_L, int(alpha), int(beta))
   misc.imsave("Hybrid_Image1.png",numpy.real(hybrid))
   cv2.imshow("Hybrid",numpy.real(hybrid))
   cv2.waitKey(10)
   print("extra_credit")
   print("part_a")
   print("Select num from above available_images as highpass_image1")
   j=input()
   Image_H1 = ndimage.imread("HW1_Data/HW1_Q1/"+L[int(j)], flatten=True)
   print("Select num from above available_images as highpass_image2")
   j=input()
   Image_H2 = ndimage.imread("HW1_Data/HW1_Q1/"+L[int(j)], flatten=True)
   print("Select num from above available_images as lowpass_image")
   j=input()
   Image_L = ndimage.imread("HW1_Data/HW1_Q1/"+L[int(j)], flatten=True)
   width_,height_=Image_H1.shape
   Image_L = cv2.resize(Image_L, (height_, width_))
   Image_H2 = cv2.resize(Image_H2, (height_, width_))
   for i in range(1,4):
   	d=30
   	hybrid1 = extra(Image_H1,Image_H2,Image_L,d,d+(10*i),20,1)
   	cv2.imshow("Hybrid"+str(i),numpy.real(hybrid1))
   	cv2.waitKey(10)
   	misc.imsave("Hybrid_a"+str(i)+'.png',numpy.real(hybrid1))
   print("part_b executing....")
   for i in range(1,4):
   	d=12
   	hybrid2 = extra(Image_H1,Image_H2,Image_L,d,(d+4*i),60,2)
   	cv2.imshow("Hybrid_part:b"+str(i),numpy.real(hybrid2))
   	cv2.waitKey(10)
   	misc.imsave("Hybrid_b"+str(i)+'.png',numpy.real(hybrid2))
