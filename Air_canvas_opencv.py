import numpy as np
import cv2
import imutils
from collections import deque

red_lower_bound = np.array([0, 100, 100])     # HSV format
red_upper_bound = np.array([20, 255, 255])

lower_bound = red_lower_bound
upper_bound = red_upper_bound

# BGR format

#                 Blue         Red         Green        Yellow           White             
color_list = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 255, 255), (255, 255, 255)]       

#                         Blue         Red
color_palette_list = [(255, 0, 0), (0, 0, 255)]

# index for the colors in our palette
idx = 0


trace_blue = [deque(maxlen=1500)]
trace_red = [deque(maxlen=1500)]

# indexes
idx_blue = 0
idx_red = 0

camera = cv2.VideoCapture(0)

while True:
    (cam_rec, cam_frame) = camera.read()
    cam_frame = cv2.flip(cam_frame, 1)
    cam_frame = imutils.resize(cam_frame, width=1000)
    feed = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2HSV)


    mask = cv2.inRange(feed, lower_bound, upper_bound)                                       
   
    (contours, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = None


#    mask = cv2.inRange(feed, lower_bound, upper_bound) 

#    (_, contours, _) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
      
#    center = None



    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    t = 2

    cam_frame = cv2.rectangle(cam_frame, (125,60), (275,120), (90,0,100), -1)
    cv2.putText(cam_frame, "CLEAR", (170, 95), font, font_scale, color_list[4], t, cv2.LINE_AA)

    cam_frame = cv2.rectangle(cam_frame, (425,60), (575,120), color_palette_list[0], -1)
    cv2.putText(cam_frame, "BLUE", (480, 95), font, font_scale, color_list[4], t, cv2.LINE_AA)

    cam_frame = cv2.rectangle(cam_frame, (725,60), (875,120), color_palette_list[1], -1)
    cv2.putText(cam_frame, "RED", (785, 95), font, font_scale, color_list[4], t, cv2.LINE_AA)




    if len(contours) > 0:

        cont = sorted(contours, key = cv2.contourArea, reverse = True)[0]

        ((x, y), radius) = cv2.minEnclosingCircle(cont)

        cv2.circle(cam_frame, (int(x), int(y)), int(radius), color_list[2], 2)

        M = cv2.moments(cont)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))



        if center[1] <= 120:
            if 125 <= center[0] <= 275: 
                trace_blue = [deque(maxlen=1500)]
                trace_red = [deque(maxlen=1500)]

                idx_blue = 0
                idx_red = 0

            elif 425 <= center[0] <= 575:
                    idx = 0 

            elif 725 <= center[0] <= 875:
                    idx = 1 
      
        else :
            if idx == 0:
                trace_blue[idx_blue].appendleft(center)
            elif idx == 1:
                trace_red[idx_red].appendleft(center)




    else:
        trace_blue.append(deque(maxlen=1500))
        idx_blue += 1
        trace_red.append(deque(maxlen=1500))
        idx_red += 1



    traced = [trace_blue, trace_red]
    
    for p in range(len(traced)):
        for m in range(len(traced[p])):
            for n in range(1, len(traced[p][m])):
                if traced[p][m][n] is None:
                    continue
                
                cv2.line(cam_frame, traced[p][m][n - 1], traced[p][m][n], color_palette_list[p], 2)
                
    cv2.imshow("Canvas Drawing", cam_frame)
    
    if cv2.waitKey(1) & 0xFF == ord("w"):
        break


camera.release()
cv2.destroyAllWindows()




