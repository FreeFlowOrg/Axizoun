import cv2

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		shape = "unknown"
		perimeter = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

		if len(approx) == 3:
			shape = "triangle"

		elif len(approx) == 4:
			(x, y, w, h) = cv2.boundingRect(approx)
			AR = w / float(h) 	# AR - aspect ratio

			# square has aspect ratio close to 1
			shape = "square" if AR >= 0.95 and AR <= 1.05 else "rectangle"

		elif len(approx) == 5:
			shape = "pentagon"

		else:
			shape = "circle"

		return shape