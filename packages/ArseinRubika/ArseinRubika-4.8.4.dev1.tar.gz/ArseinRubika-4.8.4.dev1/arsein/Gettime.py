import cv2
import datetime

def Td(file):
	data = cv2.VideoCapture(file)
	frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
	fps = data.get(cv2.CAP_PROP_FPS)
	seconds = round((int(frames) / int(fps)) * 1000)
	return seconds

