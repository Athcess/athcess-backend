import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import time
import math
import urllib.request

def calculate_speed(video_url, height):
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

        def stop(self):
            if self.running:
                end_time = time.time()
                self.elapsed_time = end_time - self.start_time
                self.running = False
                print(f"Stopwatch stopped. Total time: {self.elapsed_time:.2f} seconds.")

    stopwatch = Stopwatch()
    ratio = 0
    t1 = 0
    pd = PoseDetector(trackCon=0.70, detectionCon=0.70)

    def modeling(lmlist, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, height):
        nonlocal stopwatch, ratio, t1

        if len(lmlist) != 0:
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

            x0, y0 = point0[0:-1]
            x3, y3 = point3[0:-1]
            x6, y6 = point6[0:-1]

            if point0[0] in range(900, 925):
                feet_midpoint = [(x3 + x6) / 2, (y3 + y6) / 2]
                ratio = height / math.dist([x0, y0], feet_midpoint)

            if len(point0) == 0 or (
                    point0[0] not in range(75, 925) or (point3[1] not in range(0, 500)) or (
                    point6[1] not in range(0, 500))):
                if stopwatch.running:
                    stopwatch.stop()
                    t1 = stopwatch.elapsed_time

            else:
                if not stopwatch.running:
                    stopwatch.start()

    video_file, _ = urllib.request.urlretrieve(video_url)
    cap = cv2.VideoCapture(video_file)
    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (1000, 500))
        pd.findPose(img, draw=0)
        lmlist, bbox = pd.findPosition(img, draw=0, bboxWithHands=0)
        modeling(lmlist, 23, 25, 27, 24, 26, 28, 11, 13, 15, 12, 14, 16, height)

    speed = ((ratio * 850) / 100) / t1 if t1 != 0 else 0
    cap.release()
    return round(speed, 2)