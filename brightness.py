import serial
import cv2
import math
from cvzone.HandTrackingModule import HandDetector

# Initialize serial communication
serialcomm = serial.Serial('COM3', 9600)
serialcomm.timeout = 1

# Initialize camera capture and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Read frame from camera
    success, img = cap.read()
    if not success:
        print("Failed to read frame from camera.")
        break

    # Resize frame
    img = cv2.resize(img, (500, 500))

    # Find hands and get landmarks
    img, hands = detector.findHands(img)

    # Process each detected hand
    if hands is not None:  
        for hand in hands:
            if 'lmList' in hand and len(hand['lmList']) >= 9:
                # Get specific landmarks (e.g., index finger tip and middle finger tip)
                index_tip = hand['lmList'][8]
                middle_tip = hand['lmList'][12]

                # Draw circles at the landmarks
                cv2.circle(img, tuple(index_tip), 7, (0, 255, 255), 1)
                cv2.circle(img, tuple(middle_tip), 7, (0, 255, 255), 1)

                # Draw line between the landmarks
                cv2.line(img, tuple(index_tip), tuple(middle_tip), (0, 255, 0), 2)

                # Calculate distance between landmarks
                distance = int(math.sqrt((middle_tip[0] - index_tip[0]) ** 2 + (middle_tip[1] - index_tip[1]) ** 2))

                # Map distance to range 0-255 (for serial communication)
                distance = int((distance / 110) * 255)

                # Send distance over serial
                serialcomm.write(str(distance).encode())
                serialcomm.write(b'\n')

                # Display distance on the image
                cv2.putText(img, str(distance), (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)

    # Display the processed frame
    cv2.imshow('Image', img)

    # Exit loop if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
