import cv2
import mediapipe as mp
import math
import socket


def bot_command(move: str, pwm: int) -> None:
    msg4robot = ','.join([move,f'{pwm},{pwm},0,0'])
    print(msg4robot)
    bytesToSend         = str.encode(msg4robot)
    bufferSize          = 1024
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(bytesToSend, robotAddressPort)


robotAddressPort = ("192.168.41.243", 8080)
threshold = 250
pwm = 100
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize VideoCapture
cap = cv2.VideoCapture(0)  # Change the parameter if you have multiple cameras
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set height

# Set the desired window size
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.resizeWindow('Hand Tracking', 1280, 720)  # Set the window size to 1280x720


while cap.isOpened():
    global turn
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally (mirror image)
    frame = cv2.flip(frame, 1)
    
    # Convert the image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image with MediaPipe Hands
    results = hands.process(image)
    
    # If hands are detected, annotate the image and label them
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x:
                # Draw hand landmarks on the frame
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Get the hand landmarks
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    x, y, _ = image.shape
                    landmarks.append((int(landmark.x * y), int(landmark.y * x)))
                
                # Calculate the distances between fingers
                wrist_tip = landmarks[0]    # Wrist landmark
                thumb_tip = landmarks[4]  # Thumb tip landmark
                index_tip = landmarks[8]  # Index finger tip landmark
                middle_tip = landmarks[12]  # Middle finger tip landmark
                ring_tip = landmarks[16]    # Ring finger tip landmark
                pinky_tip = landmarks[20]  # Pinky finger tip landmark

                # Calculate the distances between thumb and index finger, and thumb and middle finger
                distance_thumb_index = int(math.sqrt((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2))
                distance_thumb_middle = int(math.sqrt((thumb_tip[0] - middle_tip[0])**2 + (thumb_tip[1] - middle_tip[1])**2))
                distance_index_middle = int(math.sqrt((index_tip[0] - index_tip[0])**2 + (index_tip[1] - middle_tip[1])**2))

                distance_thumb_wrist = int(math.sqrt((thumb_tip[0] - wrist_tip[0])**2 + (thumb_tip[1] - wrist_tip[1])**2))
                distance_index_wrist = int(math.sqrt((index_tip[0] - wrist_tip[0])**2 + (index_tip[1] - wrist_tip[1])**2))
                distance_middle_wrist = int(math.sqrt((middle_tip[0] - wrist_tip[0])**2 + (middle_tip[1] - wrist_tip[1])**2))
                distance_ring_wrist = int(math.sqrt((ring_tip[0] - wrist_tip[0])**2 + (ring_tip[1] - wrist_tip[1])**2))
                distance_pinky_wrist = int(math.sqrt((pinky_tip[0] - wrist_tip[0])**2 + (pinky_tip[1] - wrist_tip[1])**2))

                # Check if the index and middle fingers are close together
                    # Check if the pinky and ring fingers are closed
                if  (distance_index_middle < 30) and (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist > threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist > threshold):
                    # Combine the distances for pinch zoom control
                    pinch_distance = int((distance_thumb_index + distance_thumb_middle)/2)
                    print(pinch_distance) # map this to PWM vaule of enable pin

                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist > threshold):
                    print('Right')
                    bot_command("RT",pwm)

                if (distance_pinky_wrist > threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    print('Left')
                    bot_command("LT", pwm)

                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist < threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist < threshold):
                    print('Stop')
                    bot_command("STP", 0)
                
                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist > threshold) and (distance_index_wrist > threshold) and (distance_thumb_wrist < threshold):
                    print('Forward')
                    bot_command("FWD", pwm)
                
                if (distance_pinky_wrist < threshold) and (distance_ring_wrist < threshold) and (distance_middle_wrist > threshold) and (distance_index_wrist < threshold) and (distance_thumb_wrist < threshold):
                    print('F#*k You Too')
                    # Implement panic mode

    # Display the output
    cv2.imshow('Hand Tracking', frame)
    
    # Check for key press events
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('w'):  # Forward movement
        if key == ord('a'):  # Forward left (aw)
            pass
            # bot_command('FLT')
        elif key == ord('d'):  # Backward right (sd)
            # bot_command('FRT')
            pass
        else:
            bot_command('FWD', pwm)
    elif key == ord('s'):  # Backward movement
        if key == ord('a'):  # Backward left (as)
            # bot_command('BLT')
            pass
        elif key == ord('d'):  # Backward right (sd)
            # bot_command('BRT')
            pass
        else:
            bot_command('BWD', pwm)
    elif key == ord('a'):
        bot_command('LT', pwm)
    elif key == ord('d'):
        bot_command('RT', pwm)
    elif key == ord(' '):  # Stop movement if spacebar is pressed
        bot_command('STP', 0)

# Release resources
cap.release()
cv2.destroyAllWindows()
