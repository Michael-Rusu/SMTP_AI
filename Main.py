import cv2
import mediapipe
import time
import numpy as np
import pyautogui
import os

#CHECK SPAM AS EMAIL MIGHT BE THERE

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


reSWidth = 1500
reSHeight = 900

ctime=0
ptime=0

cap=cv2.VideoCapture(0)

 
medhands=mediapipe.solutions.hands
hands=medhands.Hands(max_num_hands=1,min_detection_confidence=0.7)
draw=mediapipe.solutions.drawing_utils

while True:
    success, img=cap.read()
    img = cv2.flip(img,1)
    #resizes the canvas
    #img = cv2.resize(img, (reSWidth, reSHeight))
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    res = hands.process(imgrgb)
    
    lmlist=[]
    tipids=[4,8,12,16,20] #list of all landmarks of the tips of fingers
    
    cv2.rectangle(img,(20,350),(90,440),(0,255,204),cv2.FILLED)
    cv2.rectangle(img,(20,350),(90,440),(0,0,0),5)
    
    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                
                h,w,c= img.shape
                cx,cy=int(lm.x * w) , int(lm.y * h)
                lmlist.append([id,cx,cy])
                if len(lmlist) != 0 and len(lmlist)==21:
                    fingerlist=[]
                    
                    #thumb and dealing with flipping of hands
                    if lmlist[12][1] > lmlist[20][1]:
                        if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    else:
                        if lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    
                    #others
                    for id in range (1,5):
                        if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                    
                    if len(fingerlist)!=0:
                        fingercount=fingerlist.count(1)
                        if fingercount == 2:
                            img = pyautogui.screenshot('ELHS.png')
                            print("2 Fingers Detected")


                            fromaddr = "elhstudentfair@gmail.com"
                            toaddr = "mickirusu@gmail.com"


                            msg = MIMEMultipart()

                            msg['From'] = fromaddr

                            msg['To'] = toaddr
                            msg['Subject'] = "High School Fair Photo"

                            body = """
                                Hi, Thank you for being interested ELHS for your High School next year. Please enjoy the amazing photo you took with our amazing students and staff.

                                Michael

                                """


                            msg.attach(MIMEText(body, 'plain'))


                            filename = "High School Fair Photo with ELHS"
                            attachment = open("/Users/michael/Desktop/SendPhotoUsingHandTracking/ELHS.png", "rb")


                            p = MIMEBase('application', 'octet-stream')


                            p.set_payload((attachment).read())


                            encoders.encode_base64(p)

                            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)


                            msg.attach(p)


                            s = smtplib.SMTP('smtp.gmail.com', 587)
                            s.starttls()


                            s.login(fromaddr, "ELHSisBestandNothingCanBeatit107")  
                            # dydgur-buhsiq-rugCo6


                            text = msg.as_string()
                            s.sendmail(fromaddr, toaddr, text)
                            s.quit()

                            os.remove("ELHS.png")

                            

                    
                    #cv2.putText(img,str(fingercount),(25,430),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),5)
                    
                #change color of points and lines
                draw.draw_landmarks(img,handlms,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))
    
    #fps counter
    ctime = time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    #fps display
    cv2.putText(img,f'FPS:{str(int(fps))}',(0,12),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
          
    cv2.imshow("AI Photo",img)
    
    
    #press esc to quit
    if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()

#crea
