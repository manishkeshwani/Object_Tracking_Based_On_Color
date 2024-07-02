import cv2
import imutils

lowerBlue = (26,48,74)
higherBlue = (130,255,255)

cam = cv2.VideoCapture(0)

while True:
    (_,img) = cam.read()
    img = imutils.resize(img,width=800)
    blurred = cv2.GaussianBlur(img,(11,11),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv,lowerBlue,higherBlue)
    mask = cv2.erode(mask,None,iterations=2)
    mask = cv2.dilate(mask,None,iterations=2)

    center = None

    cnts = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts)>0:
        c = max(cnts,key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))

        if radius>10:
            cv2.circle(img,(int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(img,center,5,(0,255,255),-1)
            print("Center: ",center," Radius: ",radius)

            if radius>200:
                print("Object is Too Close! Stop")
            else:
                if center[0]<150:
                    print("Approching Left")
                elif center[0]>700:
                    print("Approching Right")
                elif radius<200:
                    print("Object is in Front")
                else:
                    print("Object is Too Close! Stop")
    cv2.imshow("CAMERA",img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
        
