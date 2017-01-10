import zmq
import cv2
import sys
from scorer import Scorer

cnt=0
print("Waiting Start...")

###
### Scorer Python SDK Test for Web
###

my_dict =  {"data":"hogehoge", "comment":"this is a comment"}
my_str  = "logstring-test"
my_list  = [100,200,300]

img_list = []

scorer=Scorer("Task")

while True:

    if scorer.poll() == False:
        continue

    frame = scorer.get_frame()
    if frame == None:
       continue

    bgr = frame.get_bgr()
    gray = frame.get_gray()
    scorer.web_show(gray, 1)
    scorer.web_show(bgr, 3)

    for i in range(scorer.get_roi_circle_len()):
        x,y,radius = scorer.get_roi_circle_by_index(i)
        bgr = cv2.circle(bgr, (x,y), radius, (0,0,255), 5)
    scorer.web_show(bgr, 4)

    for i in range(scorer.get_roi_line_len()):
        x1,y1,x2,y2 = scorer.get_roi_line_by_index(i)
        bgr = cv2.line(bgr, (x1,y1),(x2,y2), (255,0,0), 5)

    for i in range(scorer.get_roi_rect_len()):
        x1,y1,x2,y2 = scorer.get_roi_rect_by_index(i)
        bgr = cv2.rectangle(bgr, (x1,y1),(x2,y2), (0,255,0), 5)

    scorer.web_show(bgr, 2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#    if cnt % 20  == 0:
#        img_list.append(bgr)
#
#    cnt = cnt + 1
#    if cnt % 50  == 0:
#        if scorer.upload(log_str = my_str, images= img_list) == False:
#            sys.exit()
#        del img_list[:]
