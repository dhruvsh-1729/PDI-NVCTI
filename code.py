import cv2

path = "images/stop.jpeg"

img= cv2.imread(path)

cv2.imshow('Image',img)

cv2.waitKey(0)

cv2.destroyAllWindows()

