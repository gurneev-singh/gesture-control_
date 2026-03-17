import cv2
import numpy as np
import time
from PROCESS.hand_tracker import HandTracker
from PROCESS.volume_control import VolumeController
from PROCESS.media_control import MediaController
from PROCESS.brightness_control import BrightnessController
from PROCESS.voice_control import VoiceController
from PROCESS.utils import get_distance, draw_volume_bar, draw_brightness_bar, draw_finger_line

tracker = HandTracker()
controller = VolumeController()
media = MediaController()
brightness = BrightnessController()
voice = VoiceController()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

last_mute_time = 0
last_playpause_time = 0
COOLDOWN = 1.5
mode = "volume"

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = tracker.find_hands(img)
    p1, p2 = tracker.get_finger_positions(img)
    current_time = time.time()

    # check voice commands
    cmd = voice.get_command()
    if cmd == "volume":
        mode = "volume"
    elif cmd == "brightness":
        mode = "brightness"
    elif cmd == "mute":
        if controller.is_muted():
            controller.unmute()
        else:
            controller.mute()
    elif cmd == "playpause":
        media.play_pause()

    # Fist = mute/unmute
    if tracker.is_fist(img):
        if current_time - last_mute_time > COOLDOWN:
            if controller.is_muted():
                controller.unmute()
            else:
                controller.mute()
            last_mute_time = current_time

    # Peace sign = play/pause
    elif tracker.is_peace(img):
        if current_time - last_playpause_time > COOLDOWN:
            media.play_pause()
            last_playpause_time = current_time

    # show mute status
    if controller.is_muted():
        cv2.putText(img, "MUTED", (250, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    # show current mode
    cv2.putText(img, f"MODE: {mode.upper()}", (400, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # show last voice command
    if cmd:
        cv2.putText(img, f"Voice: {cmd}", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # pinch controls volume or brightness
    if p1 and p2 and not controller.is_muted():
        if mode == "volume":
            draw_finger_line(img, p1, p2)
            dist = tracker.smooth_distance(get_distance(p1, p2))
            vol_level = np.interp(dist, [20, 200], [0.02, 1.0])
            vol_perc = int(np.interp(dist, [20, 200], [2, 100]))
            controller.set_volume(vol_level)
            draw_volume_bar(img, vol_perc)

        elif mode == "brightness":
            bp1, bp2 = tracker.get_brightness_positions(img)
            if bp1 and bp2:
                draw_finger_line(img, bp1, bp2)
                dist2 = tracker.smooth_distance(get_distance(bp1, bp2))
                bright_perc = int(np.interp(dist2, [20, 200], [2, 100]))
                brightness.set_brightness(bright_perc)
                draw_brightness_bar(img, bright_perc)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()