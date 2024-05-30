import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import space_pressed,r_pressed,t_pressed,a_pressed,d_pressed,w_pressed
import time

detector=HandDetector(detectionCon=0.8, maxHands=1)

space_key_pressed=space_pressed
r_key_pressed = r_pressed
t_key_pressed = t_pressed
a_key_pressed = a_pressed
d_key_pressed = d_pressed
w_key_pressed = w_pressed
 
time.sleep(2.0)

current_key_pressed = set()

video=cv2.VideoCapture(0)

while True:
    ret,frame=video.read()
    
    keyPressed = False
    
    spacePressed=False
    r_Pressed = False
    t_Pressed = False
    a_Pressed = False
    d_Pressed = False
    
    
    key_count=0
    key_pressed=0  
     
    hands,img=detector.findHands(frame)
    
    cv2.rectangle(img, (0, 480), (300, 425),(50, 50, 255), -2)
    cv2.rectangle(img, (640, 480), (400, 425),(50, 50, 255), -2)
    
    if hands:
        lmList=hands[0]
        fingerUp=detector.fingersUp(lmList)
        #print(fingerUp)
        if fingerUp==[0,0,0,0,0]:
            cv2.putText(frame, 'Finger Count: 0', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'idle', (440,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            
            '''PressKey(space_key_pressed)
            spacePressed=True
            current_key_pressed.add(space_key_pressed)
            key_pressed=space_key_pressed
            keyPressed = True
            key_count=key_count+1
            '''
        if fingerUp==[0,1,0,0,0]:
            cv2.putText(frame, 'Finger Count: 1', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Attack-1', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            
            PressKey(r_key_pressed)
            r_Pressed=True
            current_key_pressed.add(r_key_pressed)
            key_pressed=r_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if fingerUp==[0,1,1,0,0]:
            cv2.putText(frame, 'Finger Count: 2', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Right Move', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(d_key_pressed)
            d_Pressed=True
            current_key_pressed.add(d_key_pressed)
            key_pressed=d_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if fingerUp==[0,1,1,1,0]:
            cv2.putText(frame, 'Finger Count: 3', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Left Move', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            #PressKey(a_key_pressed)
            '''a_Pressed=True
            current_key_pressed.add(a_key_pressed)
            key_pressed=a_key_pressed
            keyPressed = True
            key_count=key_count+1'''
            
        if fingerUp==[0,1,1,1,1]:
            cv2.putText(frame, 'Finger Count: 4', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Jumping', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(w_key_pressed)
            w_Pressed=True
            current_key_pressed.add(w_key_pressed)
            key_pressed=w_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if fingerUp==[1,1,1,1,1]:
            cv2.putText(frame, 'Finger Count: 5', (20,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'Attack-2', (420,460), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
            PressKey(t_key_pressed)
            t_Pressed=True
            current_key_pressed.add(t_key_pressed)
            key_pressed=t_key_pressed
            keyPressed = True
            key_count=key_count+1
            
        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
        elif key_count==1 and len(current_key_pressed)==2:    
            for key in current_key_pressed:             
                if key_pressed!=key:
                    ReleaseKey(key)
            current_key_pressed = set()
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
            
    cv2.imshow("Frame",frame)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break

video.release()
cv2.destroyAllWindows()
