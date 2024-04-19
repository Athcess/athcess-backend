import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math
import urllib.request

def count_push_ups(video_url):
    video_file, _ = urllib.request.urlretrieve(video_url)
    cap = cv2.VideoCapture(video_file)
    pd = PoseDetector(trackCon=0.70, detectionCon=0.70)
    counter = 0
    direction = 0

    def angles(lmlist, p1, p2, p3, p4, p5, p6, drawpoints):
        nonlocal counter
        nonlocal direction

        if len(lmlist) != 0:
            point1 = lmlist[p1]
            point2 = lmlist[p2]
            point3 = lmlist[p3]
            point4 = lmlist[p4]
            point5 = lmlist[p5]
            point6 = lmlist[p6]

            x1, y1 = point1[0:-1]
            x2, y2 = point2[0:-1]
            x3, y3 = point3[0:-1]
            x4, y4 = point4[0:-1]
            x5, y5 = point5[0:-1]
            x6, y6 = point6[0:-1]

            lefthandangle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                         math.atan2(y1 - y2, x1 - x2))

            righthandangle = math.degrees(math.atan2(y6 - y5, x6 - x5) -
                                          math.atan2(y4 - y5, x4 - x5))

            leftHandAngle = int(np.interp(lefthandangle, [-30, 180], [100, 0]))
            rightHandAngle = int(np.interp(righthandangle, [34, 173], [100, 0]))

            left, right = leftHandAngle, rightHandAngle

            if left >= 70 and right >= 70:
                if direction == 0:
                    counter += 0.5
                    direction = 1
            if left <= 70 and right <= 70:
                if direction == 1:
                    counter += 0.5
                    direction = 0

    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (1000, 500))
        pd.findPose(img, draw=0)
        lmlist, bbox = pd.findPosition(img, draw=0, bboxWithHands=0)

        angles(lmlist, 11, 13, 15, 12, 14, 16, drawpoints=0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return counter