import numpy as np
import cv2, os
import paho.mqtt.client as mqtt

# Import Image for analysis
frame = cv2.imread('9.jpg')
lol = cv2.imread('2.png')
if frame is not None:
    hight, width, c = frame.shape 
    print hight/2, width/2
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # For filtering of dead leaf colour
    lower_brown = np.array([0,0,0])
    higher_brown = np.array([30,255,255])
    mask = cv2.inRange(hsv , lower_brown , higher_brown)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    # For getting the area
    contours,hierarchy = cv2.findContours(mask, 1, 2)
    area = 0
    temp = 0
    i = 0
    j = 0 
    for cnt in contours:
 	area_t = cv2.contourArea(cnt)
        area = area + area_t
	M = cv2.moments(cnt)
	if (temp < area_t):
		temp = area_t
		j = i
		print j
        i = i + 1
    cnt = contours[j]
    M = cv2.moments(cnt)
    cY = int(M['m10']/M['m00'])
    cX = int(M['m01']/M['m00'])
    print cX, cY
    # For blacking that area
    ball = lol[20:40, 20:40]
    res[cX-10:cX+10, cY-10:cY+10] = ball
    # For filtering of total leaf colour
    lower_fore = np.array([0,0,100])
    higher_fore = np.array([50,150,255])
    mask1 = cv2.inRange(hsv , lower_fore , higher_fore)
    res1 = cv2.bitwise_and(frame, frame, mask = mask1)
    # for getting the total leaf area
    contours,hierarchy = cv2.findContours(mask1, 1, 2)
    area1 = 0
    for cnt in contours:
        area1 = area1 + cv2.contourArea(cnt)

    # Printing % of leaf which is in dead colour
    results = area*100/area1
    print results
    # Showing Different parts
    cv2.namedWindow('frame1',cv2.WINDOW_NORMAL)
    cv2.imshow('frame1',res1)
    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    cv2.imshow('frame',res)
    #os.remove("output.jpg")
    cv2.waitKey(0) & 0xFF == ord('q')
    cv2.destroyAllWindows()

    # For sending the results back to master
    def on_publish(mosq, userdata, mid):
        mosq.disconnect()
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.on_publish = on_publish
    client.publish("image",results,0)
    client.loop_forever()
else:
    print 'lol'
