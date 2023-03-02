import cv2
import mediapipe as mp

# Initialize the MediaPipe Hand Tracking module
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

# Set the size and position of the square
square_size = 50
square_x = 0
square_y = 0


img = cv2.imread("./data/carParkImg.png")

# Create a VideoCapture object for the camera
cap = cv2.VideoCapture(0)

# Set the camera resolution and frame rate
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height =cap.get(cv2.CAP_PROP_FRAME_HEIGHT)



img = cv2.imread("./data/carParkImg.png")
img_resized = cv2.resize(img,(int(frame_width/3),int(frame_height/3)))
img_height, img_width, _ = img_resized.shape

# image initial position
x = 50
y = 50

while True:
    # Capture a frame from the camera
    success, frame = cap.read()

    if not success:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Process the frame with the MediaPipe Hand Tracking module
    results = hands.process(frame)

    # Extract the hand landmarks from the results
    if results.multi_hand_landmarks:
        for index,hand_landmarks in enumerate(results.multi_hand_landmarks):
            #print(f"index {index}")
            mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hand_label = results.multi_handedness[index].classification[0].label

            if hand_label == "Left":
                print("left")
            # right hand
            elif hand_label == "Right":
                print("right")
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            else:
                print("unknown hand")


            # Get the coordinates of the index finger and thumb
            # index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            #print(f"index_finger, {index_finger}")
            #print(f"thumb, {thumb}")

            # Convert the coordinates from normalized values to pixel values
            image_height, image_width, _ = frame.shape

            # actual position in the image
            index_finger_x = int(index_finger.x * image_width)
            index_finger_y = int(index_finger.y * image_height)
            thumb_x = int(thumb.x * image_width)
            thumb_y = int(thumb.y * image_height)

            # Check if the index finger and thumb are close together
            if (thumb_x - index_finger_x) ** 2 + (thumb_y - index_finger_y) ** 2 < 500:
                #print("distance ",(thumb_x - index_finger_x) ** 2 + (thumb_y - index_finger_y) ** 2)

                rule_x = square_x < index_finger_x < square_x+square_size
                rule_y = square_y < index_finger_y < square_y+square_size

                img_rule_x = x < index_finger_x < x + img_width
                img_rule_y = y < index_finger_y < y + img_height

                if img_rule_x and img_rule_y:
                    x = index_finger_x - img_width // 2
                    y = index_finger_y - img_height // 2

                if rule_x and rule_y:
                    # Move the square to the position of the index finger
                    square_x = index_finger_x - square_size // 2
                    square_y = index_finger_y - square_size // 2

    # Draw the square on the frame
    cv2.rectangle(
        frame,
        (square_x, square_y),
        (square_x + square_size, square_y + square_size),
        (0, 255, 0),
        thickness=2,
    )

    # add the image over the video capture frame
    frame[y:y+img_height,x:x+img_width] = img_resized

    # Display the frame with the square
    cv2.imshow('Hand Tracking', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()