import numpy as np
import cv2
import imutils
from collections import deque
import time

# Define the HSV range for the green color
greenLower = (10, 120, 100)
greenUpper = (40, 255, 255)

# Open the video stream
#cap = cv2.VideoCapture("two_balls.MOV")
cap = cv2.VideoCapture("one_ball.MOV")
time.sleep(2.0)

# Initialize variables for bounce counting and motion direction for the first ball
bounce_count1 = 0
direction1 = None
pts1 = deque(maxlen=10)

# Initialize variables for bounce counting and motion direction for the second ball
bounce_count2 = 0
direction2 = None
pts2 = deque(maxlen=10)

# Minimum distance between ball centers
min_distance = 120

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if frame is None:
        break

    # Resize the frame for better processing speed
    frame = imutils.resize(frame, width=600)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Create a mask to extract green color
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center1, center2 = None, None

    # Process each contour
    for c in cnts:
        # Find the contour with the minimum enclosing circle
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        # Calculate the centroid of the ball
        ball_center = (int(x), int(y))
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (255, 0, 255), -1)

        # Check if center1 is None or if the current ball is close enough to center1
        if center1 is None or np.linalg.norm(np.array(center1) - np.array(ball_center)) < min_distance:
            center1 = ball_center
            pts1.appendleft(center1)

        # Check if center2 is None, and the current ball is not too close to center1
        elif center2 is None and np.linalg.norm(np.array(center1) - np.array(ball_center)) >= min_distance:
            center2 = ball_center
            pts2.appendleft(center2)

    # Draw circles and trails for the first ball
    for i in range(1, len(pts1)):
        if pts1[i - 1] is None or pts1[i] is None:
            continue
        thickness = int(np.sqrt(10 / float(i + 1)) * 2.5)
        cv2.line(frame, pts1[i - 1], pts1[i], (0, 0, 255), thickness)

    # Draw circles and trails for the second ball
    for i in range(1, len(pts2)):
        if pts2[i - 1] is None or pts2[i] is None:
            continue
        thickness = int(np.sqrt(10 / float(i + 1)) * 2.5)
        cv2.line(frame, pts2[i - 1], pts2[i], (0, 255, 0), thickness)

    # Check for bounce by detecting a change in motion direction for the first ball
    if len(pts1) >= 2:
        dy = pts1[0][1] - pts1[1][1]  # Change in y-coordinate
        if dy > 20:
            direction1 = 'up'
        elif dy < 20 and direction1 == 'up':
            bounce_count1 += 1
            print(f"Bounce detected! Count for ball 1: {bounce_count1}")
            direction1 = 'down'

    # Check for bounce by detecting a change in motion direction for the second ball
    if len(pts2) >= 2:
        dy = pts2[0][1] - pts2[1][1]  # Change in y-coordinate
        if dy > 20:
            direction2 = 'up'
        elif dy < 20 and direction2 == 'up':
            bounce_count2 += 1
            print(f"Bounce detected! Count for ball 2: {bounce_count2}")
            direction2 = 'down'

    # Display bounce count on the frame for each ball
    cv2.putText(frame, f'Bounces: {bounce_count1}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Bounces: {bounce_count2}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release resources
cv2.destroyAllWindows()
cap.release()
