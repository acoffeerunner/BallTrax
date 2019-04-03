import cv2
import argparse
import numpy as np
#import time
 
def callback(value):
    pass
   
def main(): 
    camera = cv2.VideoCapture(0)

    st = time.time()
    d = 0
    dsp = 0
    i = 1
    centsx = [None] * 100000000
    centsy = [None] * 100000000
    while True:
        ret, image = camera.read()
  
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 
        v1_min = 70
        v2_min = 126
        v3_min = 156
        v1_max = 255
        v2_max = 255 
        v3_max = 255
 
        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
 
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
 
        # find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        centsx[i] = center[0]
        centsy[i] = center[1]
        # draw the circle and centroid on the frame
        cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
        cv2.circle(image, center, 3, (0, 0, 255), -1)
        cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
        cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 255, 0),1)
        if i > 1:
            d += ((centsx[i]-centsx[i-1])**2+(centsy[i]-centsy[i-1])**2)**0.5
            dsp = ((centsx[i]-centsx[1])**2+(centsy[i]-centsy[1])**2)**0.5  
        cv2.putText(image, "distance: "+str(d)+" pixels in "+str(et)+"in "+str(i)+"frames", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),1)
        cv2.putText(image, "displacement: "+str(dsp)+" pixels in "+str(et)+"in "+str(i)+"frames", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),1)
        s=d/i
        v=dsp/i
        cv2.putText(image, "speed: "+str(s)+" pixels per frame", (0, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),1)
        cv2.putText(image, "velocity: "+str(v)+" pixels per frame", (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),1)
        s=d/et

        cv2.imshow("Original", image)
        cv2.imshow("Mask", mask)
        i+=1
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break
 
 
if __name__ == '__main__':
    main()
