from util import *


def shi(src, blockSize, ksize, k,Q): # Q-question
  def harris_score(M):
    if(Q==1):
     l1,l2=np.linalg.eig(M)[0]
     return min(l1,l2)
  return generate_gradient_matrix(src, blockSize, ksize, k, harris_score)


def write_image_with_corners_and_show(name, image, corners):

  result = cv2.dilate(corners, None) ##  morphological dilation


  image[result > 0.2 * result.max()] = [0, 255, 0]  #BGR

  cv2.imwrite("%s.jpg" % name, image)
  cv2.imshow(name, image)


img, gray = read_image()

gray1=gray

img1=img

cv2.imshow("input", img)
ini_time = time()  # starting timer 
print (" Running  shi detector :")
shi_out = shi(gray1, 2, 3, 0.04,1)
cv2.imshow("shi_out",shi_out)
cv2.waitKey(10)
write_image_with_corners_and_show("shi_out", img1, shi_out)


