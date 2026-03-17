import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
activation = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(activation, POINTER(IAudioEndpointVolume))
min_vol, max_vol = volume.GetVolumeRange()[0], volume.GetVolumeRange()[1]

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    h, w, _ = img.shape

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        x1, y1 = int(hand.landmark[4].x * w), int(hand.landmark[4].y * h)
        x2, y2 = int(hand.landmark[8].x * w), int(hand.landmark[8].y * h)

        cv2.circle(img, (x1, y1), 12, (255, 0, 255), -1)
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), -1)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        dist = math.hypot(x2 - x1, y2 - y1)
        volume.SetMasterVolumeLevelScalar(np.interp(dist, [20, 200], [0.02, 1.0]), None)
        vol_perc = int(np.interp(dist, [20, 200], [2, 100]))
        vol_bar = int(np.interp(dist, [20, 200], [400, 150]))

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
        cv2.rectangle(img, (50, vol_bar), (85, 400), (0, 255, 0), -1)
        cv2.putText(img, str(vol_perc) + "%", (40, 430),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
