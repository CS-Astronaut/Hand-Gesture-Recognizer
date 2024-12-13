import cv2
import mediapipe as mp
import sqlite3
import time
import pyautogui
import subprocess
from datetime import datetime

DB_FILE = "gestures.db"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

last_gesture = None
last_trigger_time = 0
DEBOUNCE_DELAY = 0.5

# List to store debugging logs
debug_logs = []

def execute_action(action, gesture_name):
    """Execute the corresponding action for a detected gesture."""
    global debug_logs
    try:
        if action.startswith("/usr/bin/"):
            subprocess.Popen(action)
        elif action == "Volume Up":
            pyautogui.press("volumeup")
        elif action == "Volume Down":
            pyautogui.press("volumedown")
        elif action == "Zoom In":
            pyautogui.hotkey('ctrl', '+')
        elif action == "Zoom Out":
            pyautogui.hotkey('ctrl', '-')
        elif action == "Scroll Up":
            pyautogui.scroll(100)
        elif action == "Scroll Down":
            pyautogui.scroll(-100)
        else:
            print(f"Unhandled action: {action}")
        
        # Log the triggered action
        log_message = f"{datetime.now()} - Gesture Triggered - {gesture_name} - function {action}"
        debug_logs.append(log_message)
        print(log_message)  # Optionally, print to the console as well
    except Exception as e:
        print(f"Action execution error: {e}")

def load_gestures_from_db():
    """Load gestures and their actions from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT gesture_name, action FROM gestures")
        gestures = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return gestures
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}

def detect_gesture(landmarks):
    """Detect gestures based on hand landmarks."""
    def is_finger_up(finger_indices):
        return all(landmarks[tip].y < landmarks[base].y for tip, base in finger_indices)

    def is_finger_down(finger_indices):
        return all(landmarks[tip].y > landmarks[base].y for tip, base in finger_indices)

    index_tip, index_base = 8, 6
    middle_tip, middle_base = 12, 10
    ring_tip, ring_base = 16, 14
    pinky_tip, pinky_base = 20, 18
    thumb_tip, thumb_base = 4, 3

    # One finger up
    if (landmarks[index_tip].y < landmarks[index_base].y and 
        all(landmarks[tip].y > landmarks[base].y for tip, base in [(middle_tip, middle_base), (ring_tip, ring_base), (pinky_tip, pinky_base)])):
        return "one_finger_up"

    # One finger down
    if (landmarks[index_tip].y > landmarks[index_base].y and 
        all(landmarks[tip].y < landmarks[base].y for tip, base in [(middle_tip, middle_base), (ring_tip, ring_base), (pinky_tip, pinky_base)])):
        return "one_finger_down"

    # Fist closed
    if all(landmarks[tip].y > landmarks[0].y for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
        return "fist_closed"

    # Fist opened
    if all(landmarks[tip].y < landmarks[0].y for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
        return "fist_opened"

    return None

def render_debug_logs(frame):
    """Render debug logs on the frame."""
    y_offset = 20
    for log in debug_logs[-5:]:  # Display the last 10 logs
        cv2.putText(frame, log, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        y_offset += 20

def process_frame(frame, gestures):
    """Process the frame to detect gestures and execute actions."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    detected_gesture = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            current_gesture = detect_gesture(hand_landmarks.landmark)
            
            if current_gesture and current_gesture in gestures:
                detected_gesture = current_gesture
                break

    return frame, detected_gesture

def main():
    global last_gesture, last_trigger_time
    gestures = load_gestures_from_db()

    if not gestures:
        print("No gestures found in the database. Exiting.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    print("Starting gesture recognition. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to fetch frame from camera.")
            break

        frame, gesture = process_frame(frame, gestures)

        current_time = time.time()
        if gesture and (gesture != last_gesture or current_time - last_trigger_time > DEBOUNCE_DELAY):
            action = gestures[gesture]
            execute_action(action, gesture)
            last_gesture = gesture
            last_trigger_time = current_time

        # Render debug logs on the frame
        render_debug_logs(frame)

        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
