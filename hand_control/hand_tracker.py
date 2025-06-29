import cv2 
import mediapipe as mp

mp_hands = mp.solutions.hands #shorter alias
hands = mp_hands.Hands(max_num_hands=1) #internally uses 21 landmarks per hand, limited to detect only 1 hand
mp_draw = mp.solutions.drawing_utils #build in drawing function to overlay landmarks and connections

print("Capturing video...")
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read() #captures frame, ret is boolean(success/failure), frame captures actual frame
    frame = cv2.flip(frame, 1) #flips image horizontally to create a mirror effect - natural fo ruser experience
    if not ret:
        print("Failed to grab frame")
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts frame from BGR (OpenCV default) tp RGB(MediaPipe default)
    result = hands.process(rgb_frame) #Passes the RGB frame to the MediaPipe hand detector, returns results


    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) #draws 21 landmark points and the lines(connections) between them.


    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    

