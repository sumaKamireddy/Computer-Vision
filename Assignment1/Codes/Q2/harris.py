from util import *


def harris(src, blockSize, ksize, k,Q): # Q-question
  def harris_score(M):
    if(Q==1):
     return np.linalg.det(M) - k * (np.trace(M) )  
    if(Q==2):
     l1,l2=np.linalg.eig(M)[0]
     return l1*l2-k*(l1+l2)
  return generate_gradient_matrix(src, blockSize, ksize, k, harris_score)


def write_image_with_corners_and_show(name, image, corners):
  #print(corners)
  result = cv2.dilate(corners, None) ##  morphological dilation
  #print(result) 
  # Threshold for an optimal value, it may vary depending on the image.
  image[result > 0.2 * result.max()] = [0, 255, 0]  #BGR
  #image[result > 500] = [0, 255, 0]  #BGR

  cv2.imwrite("%s.png" % name, image)
  cv2.imshow(name, image)

check_usage("harris")  ### input format checking
img, gray = read_image()

ini_time = time()  # starting timer 
print (" Running  Harris corner detector :")
partb_out = harris(gray, 2, 3, 0.04,1)
print ("SUCCESS (%.3f secs): Running Harris corner detector" % (time() - ini_time))
ini2_time=time()
partc_out = harris(gray, 2, 3, 0.04,2)
print ("SUCCESS (%.3f secs): Running Harris lamda detector" % (time() - ini2_time))
l=[]
# opencv = cv2.cornerHarris(gray,2,3,0.04)
for i in range(4,10):
	alpha_var = harris(gray, 2, 3, float(i)/100,1)
	write_image_with_corners_and_show("alpha_var"+str(i), img, alpha_var)

write_image_with_corners_and_show("partb_out", img, partb_out)
write_image_with_corners_and_show("partc_out", img, partc_out)
cv2.destroyAllWindows()
