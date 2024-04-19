import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import time
import math

def calculate_speed(video_url):
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return None
    
    pd = PoseDetector(trackCon=0.70, detectionCon=0.70)

    class Stopwatch:
        def __init__(self):
            self.start_time = None
            self.elapsed_time = 0
            self.running = False

        def start(self):
            if not self.running:
                self.start_time = time.time()
                self.running = True
                print("Stopwatch started.")
            else:
                print("Stopwatch is already running.")

        def stop(self):
            if self.running:
                end_time = time.time()
                self.elapsed_time = end_time - self.start_time
                self.running = False
                print(f"Stopwatch stopped. Total time: {self.elapsed_time:.2f} seconds.")
            else:
                print("Stopwatch is not running.")

    global stopwatch_called
    global stopwatch
    global ratio
    global t1

    def modeling(lmlist,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,drawpoints):
        global stopwatch_called
        global stopwatch
        global ratio
        global t1

        if len(lmlist)!= 0:
            point0 = lmlist[0]
            point1 = lmlist[p1]
            point2 = lmlist[p2]
            point3 = lmlist[p3]
            point4 = lmlist[p4]
            point5 = lmlist[p5]
            point6 = lmlist[p6]
            point7 = lmlist[p7]
            point8 = lmlist[p8]
            point9 = lmlist[p9]
            point10 = lmlist[p10]
            point11 = lmlist[p11]
            point12 = lmlist[p12]

            x0,y0 = point0[0:-1]
            x1,y1 = point1[0:-1]
            x2, y2 = point2[0:-1]
            x3, y3 = point3[0:-1]
            x4, y4 = point4[0:-1]
            x5, y5 = point5[0:-1]
            x6, y6 = point6[0:-1]
            x7,y7 = point7[0:-1]
            x8, y8 = point8[0:-1]
            x9, y9 = point9[0:-1]
            x10, y10 = point10[0:-1]
            x11, y11 = point11[0:-1]
            x12, y12 = point12[0:-1]
            print(point0,point3,point6)
            if point0[0] in range(900,925):
                feet_midpoint = [(x3+x6)/2, (y3+y6)/2]
                ratio = 173 / math.dist([x0,y0],feet_midpoint)
        
            print(ratio)
            if point0[1] < 50 or len(point0) == 0  or (point0[0] not in range(75,925) or (point3[1] not in range(0,500)) or (point6[1] not in range(0,500))):
                 cv2.rectangle(img,(950,0),(1000,50),(0,0,255),-1)
                 if stopwatch_called:
                    stopwatch.stop()
                    t1 = stopwatch.elapsed_time
                     
            else:
                cv2.rectangle(img,(950,0),(1000,50),(0,255,0),-1)
                if not stopwatch_called:
                     stopwatch.start()
                     stopwatch_called = True
                

            if drawpoints == True:
                cv2.circle(img,(x0,y0),10,(255,0,255),3)
                cv2.circle(img, (x0, y0), 15, (0,255, 0),3)
                cv2.circle(img,(x1,y1),10,(255,0,255),3)
                cv2.circle(img, (x1, y1), 15, (0,255, 0),3)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), 3)
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), 3)
                cv2.circle(img, (x3, y3), 10, (255, 0, 255), 3)
                cv2.circle(img, (x3, y3), 15, (0, 255, 0), 3)
                cv2.circle(img, (x4, y4), 10, (255, 0, 255), 3)
                cv2.circle(img, (x4, y4), 15, (0, 255, 0), 3)
                cv2.circle(img, (x5, y5), 10, (255, 0, 255), 3)
                cv2.circle(img, (x5, y5), 15, (0, 255, 0), 3)
                cv2.circle(img, (x6, y6), 10, (255, 0, 255), 3)
                cv2.circle(img, (x6, y6), 15, (0, 255, 0), 3)

                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),6)
                cv2.line(img, (x2,y2), (x3, y3), (0, 0, 255), 4)
                cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 4)
                cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 4)
                cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 4)

                cv2.circle(img,(x7,y7),10,(255,0,255),3)
                cv2.circle(img, (x7, y7), 15, (0,255, 0),3)
                cv2.circle(img, (x8, y8), 10, (255, 0, 255), 3)
                cv2.circle(img, (x8, y8), 15, (0, 255, 0), 3)
                cv2.circle(img, (x9, y9), 10, (255, 0, 255), 3)
                cv2.circle(img, (x9, y9), 15, (0, 255, 0), 3)
                cv2.circle(img, (x10, y10), 10, (255, 0, 255), 3)
                cv2.circle(img, (x10, y10), 15, (0, 255, 0), 3)
                cv2.circle(img, (x11, y11), 10, (255, 0, 255), 3)
                cv2.circle(img, (x11, y11), 15, (0, 255, 0), 3)
                cv2.circle(img, (x12, y12), 10, (255, 0, 255), 3)
                cv2.circle(img, (x12, y12), 15, (0, 255, 0), 3)

                cv2.line(img,(x7,y7),(x8,y8),(0,0,255),4)
                cv2.line(img, (x8,y8), (x9, y9), (0, 0, 255), 4)
                cv2.line(img, (x10, y10), (x11, y11), (0, 0, 255), 4)
                cv2.line(img, (x11, y11), (x12, y12), (0, 0, 255), 4)
                cv2.line(img, (x7, y7), (x10, y10), (0, 0, 255), 4)

    def process_video():
        while True:
            ret, img = cap.read()
            if not ret:
                break

            img = cv2.resize(img, (1000, 500))
            cvzone.putTextRect(img, 'Please stay inside the rectangle', [150, 30], thickness=2, border=2, scale=2.5, colorB=(0, 0, 0))
            cv2.rectangle(img, (75, 50), (925, 500), (0, 255, 0), 3)
            pd.findPose(img, draw=0)
            lmlist, bbox = pd.findPosition(img, draw=0, bboxWithHands=0)
            
            if lmlist:
                modeling(lmlist, 23, 25, 27, 24, 26, 28, 11, 13, 15, 12, 14, 16, drawpoints=1)

            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Calculate and return speed
        speed = ((ratio * 850) / 100) / t1
        return round(speed, 2)

    # Start processing the video
    stopwatch_called = False
    stopwatch = Stopwatch()
    ratio = 0
    t1 = 0
    speed = process_video()

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    return speed