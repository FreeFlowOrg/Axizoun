# USAGE
# python sliding_window.py --image images/adrian_florida.jpg

# import the necessary packages

from helpers import *
import argparse
import time
import cv2

def extract_chars():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="Path to the image")
	args = vars(ap.parse_args())

	# load the image and define the window width and height
	image = cv2.imread(args["image"])
	(winW, winH) = (192, 192)

	# loop over the image pyramid
	for resized in pyramid(image, scale=1.5):
		# loop over the sliding window for each layer of the pyramid
		for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
			# if the window does not meet our desired window size, ignore it
			if window.shape[0] != winH or window.shape[1] != winW:
				continue

			import pytesseract
			#print(pytesseract.image_to_string(window))

			with open('extracted_info.txt', 'a') as info_file:
				info_file.write(str(pytesseract.image_to_string(window).encode('utf-8')) + '\n')
				info_file.write('#\n')

			clone = resized.copy()
			cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
			cv2.imshow("Window", clone)
			cv2.waitKey(1)
			time.sleep(0.025)

def extract_information():
	with open('extracted_info.txt', 'r') as info_file:
		content = info_file.read()

	for line in content.split('#'):
		print(line)

if __name__ == '__main__':
	extract_chars()
	extract_information()
