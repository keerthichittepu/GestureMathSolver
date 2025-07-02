import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import pandas as pd
import os
import pyttsx3
import matplotlib.pyplot as plt
import threading
from datetime import datetime

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables
last_update_time = 0
digit_buffer = ""
digit_buffer_time = 0
expression = ""
res = ""
delay = 1.25
digit_timeout = 3

# Euclidean distance
def euclidean_distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# Count fingers
def count_fingers(hand_landmarks, label):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []
    if label == "Left":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i]-2].y else 0)
    return fingers.count(1)

# Gesture detection
def detectGesture(hand1_data, hand2_data):
    (hand1, label1), (hand2, label2) = hand1_data, hand2_data
    f1 = count_fingers(hand1, label1)
    f2 = count_fingers(hand2, label2)
    dist = euclidean_distance(hand1.landmark[8], hand2.landmark[8])
    if f1 == 1 and f2 == 1:
        if dist < 0.06:
            return "exit"
        return "+"
    elif (f1 == 1 and f2 == 2) or (f1 == 2 and f2 == 1):
        return "-"
    elif (f1 == 1 and f2 == 3) or (f1 == 3 and f2 == 1):
        return "*"
    elif (f1 == 1 and f2 == 4) or (f1 == 4 and f2 == 1):
        return "/"
    elif f1 == 2 and f2 == 2:
        return "del"
    elif (f1 == 1 and f2 == 5) or (f1 == 5 and f2 == 1):
        return "6"
    elif (f1 == 2 and f2 == 5) or (f1 == 5 and f2 == 2):
        return "7"
    elif (f1 == 3 and f2 == 5) or (f1 == 5 and f2 == 3):
        return "8"
    elif (f1 == 4 and f2 == 5) or (f1 == 5 and f2 == 4):
        return "9"
    elif f1 == 0 and f2 == 0:
        return "="
    elif f1 == 5 and f2 == 5:
        return "clear"
    return None

# Save to CSV
def log_expression(expression, result):
    log_file = "math_logs.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[timestamp, expression, result]], columns=["Time", "Expression", "Result"])
    if os.path.exists(log_file):
        existing = pd.read_csv(log_file)
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry
    updated.to_csv(log_file, index=False)

# Show live graph
def show_graph_background():
    try:
        df = pd.read_csv("math_logs.csv")
        df["Time"] = pd.to_datetime(df["Time"])
        df["Date"] = df["Time"].dt.date
        expr_per_day = df.groupby("Date").size()
        plt.figure(figsize=(6, 4))
        expr_per_day.plot(kind="bar", color="orange")
        plt.title("Expressions Solved Per Day")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Graph Error:", e)

# Webcam setup
cap = cv.VideoCapture(0)

while True:
    success, image = cap.read()
    if not success:
        continue
    image = cv.flip(image, 1)
    img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    current_time = time.time()
    hand_data = []

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = hand_handedness.classification[0].label
            hand_data.append((hand_landmarks, label))
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Single hand input
        if len(hand_data) == 1:
            hand_landmarks, label = hand_data[0]
            fingers_up = count_fingers(hand_landmarks, label)
            if fingers_up in [0, 1, 2, 3, 4, 5] and current_time - last_update_time > delay:
                digit_buffer += str(fingers_up)
                digit_buffer_time = current_time
                last_update_time = current_time

        # Two-hand gesture
        if len(hand_data) == 2:
            gesture = detectGesture(hand_data[0], hand_data[1])
            if gesture == "exit":
                break
            elif gesture == "clear":
                expression = ""
                res = ""
                digit_buffer = ""
                last_update_time = current_time
            elif gesture == "del" and current_time - last_update_time > delay:
                expression = expression[:-1]
                last_update_time = current_time
            elif gesture == "=" and current_time - last_update_time > delay:
                if digit_buffer:
                    expression += digit_buffer
                    digit_buffer = ""
                try:
                    res = str(eval(expression))
                    log_expression(expression, res)
                    engine.say(f"The result is {res}")
                    engine.runAndWait()
                    threading.Thread(target=show_graph_background, daemon=True).start()
                except:
                    res = "Error"
                    log_expression(expression, res)
                    engine.say("There was an error in calculation")
                    engine.runAndWait()
                last_update_time = current_time
            elif gesture and current_time - last_update_time > delay:
                if digit_buffer:
                    expression += digit_buffer
                    digit_buffer = ""
                expression += gesture
                last_update_time = current_time

    # Auto-finalize digit buffer
    if digit_buffer and current_time - digit_buffer_time > digit_timeout:
        expression += digit_buffer
        digit_buffer = ""

    # Display
    cv.putText(image, f'Expr: {expression + digit_buffer}', (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv.putText(image, f'Result: {res}', (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
    cv.imshow("Gesture Math Solver", image)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break
    elif key == ord('c'):
        expression = ""
        res = ""
        digit_buffer = ""

# Cleanup
cap.release()
cv.destroyAllWindows()
