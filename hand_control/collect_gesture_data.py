import cv2
import mediapipe as mp
import pandas as pd
import os

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Gesture key-to-label mapping
gesture_map = {
    'i': 'idle',
    's': 'stop',
    'f': 'forward',
    'b': 'backward',
    'l': 'left',
    'r': 'right'
}

# CSV file setup
csv_file = "hand_gestures.csv"
if not os.path.exists(csv_file):
    columns = [f"{axis}{i}" for i in range(21) for axis in ['x','y','z']] + ['label']
    pd.DataFrame(columns=columns).to_csv(csv_file, index=False)

# Start camera
cap = cv2.VideoCapture(0)  # Change to 0 if needed

if not cap.isOpened():
    print("❌ Could not open camera.")
    exit()

print("📷 Hand Gesture Data Collection Started")
print("👉 Press i/s/f/b/l/r to label a gesture (idle/stop/forward/backward/left/right)")
print("❌ Press q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                print("👋 Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                hands.close()
                exit()

            elif chr(key) in gesture_map:
                # Extract landmarks
                row = []
                for lm in hand_landmarks.landmark:
                    row.extend([lm.x, lm.y, lm.z])
                row.append(gesture_map[chr(key)])

                # Save to CSV
                pd.DataFrame([row]).to_csv(csv_file, mode='a', header=False, index=False)
                print(f"Saved: {gesture_map[chr(key)]}")

    cv2.imshow("Hand Gesture Collector", frame)