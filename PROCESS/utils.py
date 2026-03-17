import cv2
import math
import numpy as np

def get_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def draw_volume_bar(img, vol_perc):
    vol_bar = int(np.interp(vol_perc, [0, 100], [400, 150]))
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
    cv2.rectangle(img, (50, vol_bar), (85, 400), (0, 255, 0), -1)
    cv2.putText(img, str(vol_perc) + "%", (40, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def draw_brightness_bar(img, bright_perc):
    bright_bar = int(np.interp(bright_perc, [0, 100], [400, 150]))
    cv2.rectangle(img, (550, 150), (585, 400), (0, 255, 255), 2)
    cv2.rectangle(img, (550, bright_bar), (585, 400), (0, 255, 255), -1)
    cv2.putText(img, str(bright_perc) + "%", (540, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

def draw_finger_line(img, p1, p2):
    cv2.circle(img, p1, 12, (255, 0, 255), -1)
    cv2.circle(img, p2, 12, (255, 0, 255), -1)
    cv2.line(img, p1, p2, (255, 0, 255), 3)