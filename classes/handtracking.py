import cv2
import numpy as np
import mediapipe as mp
import time

# create own function
class handDetector():
    # from Hand  method from mediapipe
    def __init__(self,mode=False,maxHands=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=False):
        self.result=self.hands.process(img)
        return img

    def findPosition(self,img,handNomber=0,draw=False):
        lmList=[]
        if self.result.multi_hand_landmarks:
            hand=self.result.multi_hand_landmarks[handNomber]
            for id, lm in enumerate(hand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),8,(255,0,255),cv2.FILLED)
        return lmList

def main():
    cap=cv2.VideoCapture(0)
    cTime=0
    pTime=0
    detector=handDetector()
    while True:
        success,frame=cap.read()
        img=detector.findHands(frame)
        list=detector.findPosition(img)
        if len(list)!=0:
            print(list[0])
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(frame,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
        cv2.imshow("Frame",frame)
        if cv2.waitKey(5) & 0xFF == 27:
          break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
