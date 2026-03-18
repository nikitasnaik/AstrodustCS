import cv2

image = cv2.imread("input.jpg")

#converting to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#saved
cv2.imwrite("output_gray.jpg", gray_image)

#display image
cv2.imshow("Grayscale Image", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
