import cv2
import time
import math
from cvzone.PoseModule import PoseDetector
import urllib.request

def angle_between_points(p1, p2, p3):
    angle = math.degrees(math.atan2(p3[1] - p2[1], p3[0] - p2[0]) - math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
    angle = angle % 360
    if p1[0] < p3[0]:
        angle = 360 - angle if angle != 0 else angle
    return angle % 360

def process_frame(img, pd, start_time, counter, peak):
    img = cv2.resize(img, (1000, 500))
    img = pd.findPose(img)
    lmList, _ = pd.findPosition(img, draw=False)
    if lmList:
        shoulder, hip, knee = (lmList[12][:2], lmList[24][:2], lmList[26][:2]) if lmList[11][0] < lmList[25][0] else (lmList[11][:2], lmList[23][:2], lmList[25][:2])
        angle = abs(angle_between_points(shoulder, hip, knee))
        angle_threshold_up = 230
        angle_threshold_down = 270
        if angle > angle_threshold_down and not peak:
            if start_time is None:
                start_time = time.time()
            peak = True
        elif angle < angle_threshold_up and peak:
            if (time.time() - start_time) <= 30:  # Count only for 30 seconds
                counter += 1
                peak = False
    return img, start_time, counter, peak

def count_situps(video_url):
    video_file, _ = urllib.request.urlretrieve(video_url)
    cap = cv2.VideoCapture(video_file)
    pd = PoseDetector(trackCon=0.70, detectionCon=0.70)
    counter = 0
    peak = False
    start_time = None

    while True:
        success, img = cap.read()
        if not success:
            break

        img, start_time, counter, peak = process_frame(img, pd, start_time, counter, peak)
    
    cap.release()
    return counter