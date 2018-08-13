# import req libraries
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

# aprsing the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# preprocessing the image
# resizing the image for better approximation
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# converting to gray scale
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
threshold = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# finding the contour
contour = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, 
	cv2.CHAIN_APPROX_SIMPLE)
contour = contour[0] if imutils.is_cv2() else contour[1]

SD = ShapeDetector()

# looping over the contours
for c in contour:
	M = cv2.moments(c)
	cX = int((M['m10'] / M['m00']) * ratio)
	cY = int((M['m01'] / M['m00']) * ratio)
	shape = SD.detect(c)

	# changing back to original size
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	# identifying the shapes and naming them
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 
		0.5, (0, 0, 0), 2)

	# showing the image
	print(shape)
	cv2.imshow("Image", image)
	cv2.waitKey(0)