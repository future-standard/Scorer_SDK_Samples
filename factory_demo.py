import zmq
import cv2
import sys
import numpy as np
#import Scorer
import scorer_sdk.Scorer


cnt=0
print("Waiting Start...")

scorer=scorer_sdk.Scorer.Scorer("Task")
args = sys.argv

if len(args) > 1:
	thresh = int(args[1])
else:
	thresh = 50

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
	width = int(x2-x1)
	height = int(y2-y1)
	ret ,binary_img = cv2.threshold(bgr, thresh, 255, cv2.THRESH_BINARY)
	crop_img = binary_img[y1:y2, x1:x2]
	m = int(np.count_nonzero(crop_img))
	m = int((width*height*3-m)*100/(width*height*3))
	bgr = cv2.rectangle(bgr, (x1,y1), (x2,y2), (0,0,255), 3)
	cv2.imshow("bgr", bgr)
	cv2.imshow("crop_img", crop_img)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	cnt = cnt + 1
	if cnt % 1 == 0:
		print(str(m)+"%")

