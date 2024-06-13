import cv2
import mediapipe as mp
import time
import fingerCountingProject as cnt

time.sleep(2.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []
        if results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

        fingers = []

        if len(lmList) != 0:
            # Detection for number 5
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Detection for number 6
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1] and lmList[tipIds[1]][1] > lmList[tipIds[1] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Detection for number 7
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1] and lmList[tipIds[2]][1] > lmList[tipIds[2] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Detection for number 8
            # Thumb touches the tip of the middle finger
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1] and lmList[tipIds[3]][1] > lmList[tipIds[3] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Detection for number 9
            # Thumb touches the tip of the ring finger
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1] and lmList[tipIds[4]][1] > lmList[tipIds[4] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Detection for number 10
            # Thumb touches the tip of the index finger
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1] and lmList[tipIds[1]][1] > lmList[tipIds[1] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Check for other fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        total = fingers.count(1)
        cnt.led(total)

        if total == 0:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "0 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 1:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "1 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 2:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "2 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 3:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "3 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 4:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "4 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 5:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "5 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 6:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "6 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 7:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "7 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 8:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "8 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 9:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "9 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        elif total == 10:
            cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, "10 LED", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        else:
            # Handle other cases (if needed)
            pass

        cv2.imshow("Frame", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()