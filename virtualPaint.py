import cv2 as cv
import mediapipe as mp
import time
import numpy as np

class handDetector():
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        self.results = self.hands.process(frame)

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLm.landmark):
                    if draw:    
                        self.mpDraw.draw_landmarks(frame, handLm, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNum = 0, draw=True):
        lmlist = []
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]

            for id, lm in enumerate(myHand.landmark):
                h,w,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw and id == 8:
                    cv.circle(frame, (cx,cy), 10, (255,0,255), cv.FILLED)

        return lmlist
    
def main():
    capture = cv.VideoCapture(1)
    cTime, pTime = 0,0
    detector = handDetector()
    canvas = None
    prevx, prevy = 0,0
    color_rotation = ([255,0,0], [0,255,0], [0,0,255])
    rotation = 0
    current_color = [255,0,0]
    while True:
        success, frame = capture.read()
        frame = cv.flip(frame, 1)
        frame = detector.findHands(frame)
        lmlist = detector.findPosition(frame)

        if canvas is None:
            canvas = np.zeros_like(frame)
        if len(lmlist) != 0:
            cv.line(frame, (lmlist[4][1], lmlist[4][2]), (lmlist[8][1], lmlist[8][2]), color=(0,255,0), thickness=2, lineType=cv.LINE_AA)
            distance = np.sqrt((pow(lmlist[8][1] - lmlist[4][1], 2)) + (pow(lmlist[4][2] - lmlist[8][2],2)))

            if distance <= 70:
                current_color = color_rotation[rotation]
                rotation+=1
                if rotation == 3:
                    rotation = 0
                
            if lmlist[8][2] < lmlist[6][2]:
                pt2 = (int(lmlist[8][1]), int(lmlist[8][2]))
                if prevx == 0 and prevy == 0:
                    prevx, prevy = pt2
                cv.line(canvas, (prevx, prevy), pt2, current_color, thickness=3, lineType=cv.LINE_AA)
                prevx, prevy = pt2
            else:
                prevx, prevy = 0,0
            

        else:
            prevx, prevy = 0,0
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        frame = cv.add(frame, canvas)
        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
        cv.imshow('vpaint', frame)

        key = cv.waitKey(1)
        if key == ord('c'):
            canvas = np.zeros_like(frame)
        elif key == ord('q'):
            break
        

main()