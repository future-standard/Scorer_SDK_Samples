import zmq
import cv2
import sys
import numpy as np
import time
from scorer import Scorer


count=0
print("Waiting Start...")

scorer=Scorer("Task")
args = sys.argv

thresh = 120
minarea = 100
maxarea = 10000

if len(args) > 3:
	thresh = int(args[1])
	minarea = int(args[2])
	maxarea = int(args[3])
elif len(args) >1:
	thresh = int(args[1])
	
starttime = time.time()
while True:
	if scorer.poll() == False:
		continue
	frame = scorer.get_frame()
	if frame == None:
		continue
	bgr = frame.get_bgr()
	bgr = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
	bgr = cv2.cvtColor(bgr, cv2.COLOR_GRAY2BGR)
	x1,y1,x2,y2 = scorer.get_roi_rect_by_index(0)
	x1l,y1l,x2l,y2l = scorer.get_roi_line_by_index(0)
	width = int(x2-x1)
	height = int(y2-y1)
	ret ,binary_img = cv2.threshold(bgr, thresh, 255, cv2.THRESH_BINARY)
	crop_img = binary_img[y1:y2, x1:x2]
	binary_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	im2, contours, hierarchy = cv2.findContours(binary_crop_img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	countcnt=0;
	for h, cnt in enumerate(contours):
		if cv2.contourArea(cnt) > maxarea:
			continue
		elif cv2.contourArea(cnt) > minarea:
			countcnt = countcnt + 1	

	cv2.drawContours(crop_img,contours,-1,(0,255,0),1)
	m = int(np.count_nonzero(crop_img))
	m = int((width*height*3-m)*100/(width*height*3))
	bgr = cv2.rectangle(bgr, (x1,y1), (x2,y2), (0,0,255), 3)
	bgr = cv2.line(bgr, (x1l,y1l),(x2l,y2l), (255,0,0), 3)
	scorer.web_show(bgr, 1)
	scorer.web_show(crop_img, 2)	

	endtime = time.time()
	seconds = endtime - starttime
	starttime = time.time()
	fps = int(1/seconds*10)/10
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	count = count + 1
	if count % 15 == 0:
		print(str(m)+"% fps" + str(fps) + " count:" + str(countcnt))

