import cv2
import RPi.GPIO as GPIO
import time

# BUZZER SETUP

BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)


# CAMERA SETUP
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Camera not accessible")
    GPIO.cleanup()
    exit()

# Read first two frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()

print("Motion detection started. Press 'q' to exit")

buzzer_on = False

while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    motion = False

    for contour in contours:
        if cv2.contourArea(contour) < 1500:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        motion = True

    
    # BUZZER LOGIC
   
    if motion:
        cv2.putText(frame1, "MOTION DETECTED",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        buzzer_on = True
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        buzzer_on = False

    cv2.imshow("Motion Detection", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()
    if not ret:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# CLEANUP

cap.release()
cv2.destroyAllWindows()
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.cleanup()
