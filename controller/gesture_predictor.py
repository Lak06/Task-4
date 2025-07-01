import cv2
import torch
import numpy as np
import mediapipe as mp

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from gesture_utils import GestureNet  # Assuming GestureNet class is in model.py
import os

class GestureControlNode(Node):
    def __init__(self):
        super().__init__('gesture_control')
        self.publisher = self.create_publisher(Twist, '/robot1/cmd_vel', 10)

    def send_command(self, gesture):
        msg = Twist()

        if gesture == 'forward':
            msg.linear.x = 0.5
        elif gesture == 'backward':
            msg.linear.x = -0.5
        elif gesture == 'left':
            msg.angular.z = 0.5
        elif gesture == 'right':
            msg.angular.z = -0.5
        elif gesture == 'stop':
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        else:
            return  # Ignore unknown gestures

        self.publisher.publish(msg)
        self.get_logger().info(f"Sent command for gesture: {gesture}")

def main():
    # Initialize ROS
    rclpy.init()
    node = GestureControlNode()
# Load the gesture labels

    label_path = os.path.join(os.path.dirname(__file__), "gesture_labels.npy")
    label_names = np.load(label_path, allow_pickle=True)


# Load the trained model
    input_size = 63  # 21 landmarks × 3 (x, y, z)
    num_classes = len(label_names)
    model = GestureNet(input_size, num_classes)
    model_path = os.path.join(os.path.dirname(__file__), "gesture_model.pt")
    model.load_state_dict(torch.load(model_path))
    model.eval()

# Setup MediaPipe for hand detection
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1)

# Open the webcam
    cap = cv2.VideoCapture(0)

    print("Starting live gesture prediction...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on screen
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract 63 landmark values (x, y, z for 21 points)
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])

            # Convert to tensor and predict
                input_tensor = torch.tensor(landmarks).unsqueeze(0).float()
                with torch.no_grad():
                    output = model(input_tensor)
                    pred_class = torch.argmax(output, dim=1).item()
                    gesture = label_names[pred_class]
                    print("Predicted Gesture:", gesture)
                    node.send_command(gesture)

            # Display prediction on screen
                cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            print("No hand detected")

    # Show webcam output
        cv2.imshow("Gesture Prediction", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
    cap.release()
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
