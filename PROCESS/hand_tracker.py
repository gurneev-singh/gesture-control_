import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.9,
            model_complexity=1
        )
        self.results = None
        self.gesture_history = []
        self.HISTORY_SIZE = 8

    def find_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_finger_positions(self, img):
        h, w, _ = img.shape
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            x1 = int(hand.landmark[4].x * w)
            y1 = int(hand.landmark[4].y * h)
            x2 = int(hand.landmark[8].x * w)
            y2 = int(hand.landmark[8].y * h)
            return (x1, y1), (x2, y2)
        return None, None

    def get_brightness_positions(self, img):
        h, w, _ = img.shape
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            x1 = int(hand.landmark[4].x * w)
            y1 = int(hand.landmark[4].y * h)
            x2 = int(hand.landmark[12].x * w)
            y2 = int(hand.landmark[12].y * h)
            return (x1, y1), (x2, y2)
        return None, None

    def smooth_distance(self, dist):
        self.gesture_history.append(dist)
        if len(self.gesture_history) > self.HISTORY_SIZE:
            self.gesture_history.pop(0)
        smoothed = sum(self.gesture_history) / len(self.gesture_history)
        if len(self.gesture_history) >= 2:
            if abs(smoothed - self.gesture_history[-2]) < 3:
                return self.gesture_history[-2]
        return smoothed

    def is_fist(self, img):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            finger_tips = [8, 12, 16, 20]
            finger_base = [6, 10, 14, 18]
            curled = 0
            for tip, base in zip(finger_tips, finger_base):
                if landmarks[tip].y > landmarks[base].y:
                    curled += 1
            return curled == 4
        return False

    def is_peace(self, img):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            index_up   = landmarks[8].y  < landmarks[6].y
            middle_up  = landmarks[12].y < landmarks[10].y
            ring_down  = landmarks[16].y > landmarks[14].y
            pinky_down = landmarks[20].y > landmarks[18].y
            return index_up and middle_up and ring_down and pinky_down
        return False

    def is_brightness_mode(self, img):
        # 3 fingers up (index + middle + ring), pinky down
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            landmarks = hand.landmark
            index_up   = landmarks[8].y  < landmarks[6].y
            middle_up  = landmarks[12].y < landmarks[10].y
            ring_up    = landmarks[16].y < landmarks[14].y
            pinky_down = landmarks[20].y > landmarks[18].y
            return index_up and middle_up and ring_up and pinky_down
        return False