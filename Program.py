import cv2
import numpy as np

frameWidth = 480
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def empty(img):
    pass


cv2.namedWindow("TrackBar")     # trackbar for setting upper and lower limit of the threshold image
cv2.resizeWindow("TrackBar", 600, 300)
cv2.createTrackbar("hue_min", "TrackBar", 0, 179, empty)
cv2.createTrackbar("hue_max", "TrackBar", 179, 179, empty)
cv2.createTrackbar("sat_min", "TrackBar", 144, 255, empty)
cv2.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
cv2.createTrackbar("val_min", "TrackBar", 122, 255, empty)
cv2.createTrackbar("val_max", "TrackBar", 255, 255, empty)

cv2.namedWindow("T1")       # Switches of shape tracker
cv2.resizeWindow("T1", 300, 300)
cv2.createTrackbar("Switch", "T1", 0, 1, empty)     # switch of shape tracker
cv2.createTrackbar("Square", "T1", 0, 1, empty)
cv2.createTrackbar("Triangle", "T1", 0, 1, empty)
cv2.createTrackbar("circle", "T1", 0, 1, empty)
cv2.createTrackbar("pentagon", "T1", 0, 1, empty)

cv2.namedWindow("T2")       # Switches of Color tracker
cv2.resizeWindow("T2", 300, 300)
cv2.createTrackbar("Sw", "T2", 0, 1, empty)     # switch of Particular color object tracker
cv2.createTrackbar("Yellow", "T2", 0, 1, empty)
cv2.createTrackbar("Red", "T2", 0, 1, empty)
cv2.createTrackbar("Green", "T2", 0, 1, empty)
cv2.createTrackbar("Blue", "T2", 0, 1, empty)

while True:
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    Sw = cv2.getTrackbarPos("Sw", "T2")
    a1 = cv2.getTrackbarPos("Yellow", "T2")
    a2 = cv2.getTrackbarPos("Red", "T2")
    a3 = cv2.getTrackbarPos("Green", "T2")
    a4 = cv2.getTrackbarPos("Blue", "T2")

    lower = np.array([0, 0, 0])
    upper = np.array([255, 255, 255])
    if Sw == 1:
        if a4 == 1:
            lower = np.array([100, 50, 50])
            upper = np.array([140, 255, 255])
        elif a1 == 1:
            lower = np.array([20, 100, 100])
            upper = np.array([30, 255, 255])
        elif a2 == 1:
            lower = np.array([155, 25, 0])
            upper = np.array([179, 255, 255])
        elif a3 == 1:
            lower = np.array([40, 40, 40])
            upper = np.array([70, 255, 255])

    else:
        hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
        hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
        sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
        sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
        val_min = cv2.getTrackbarPos("val_min", "TrackBar")
        val_max = cv2.getTrackbarPos("val_max", "TrackBar")
        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])

    Switch = cv2.getTrackbarPos("Switch", "T1")
    s1 = cv2.getTrackbarPos("Square", "T1")
    s2 = cv2.getTrackbarPos("Triangle", "T1")
    s3 = cv2.getTrackbarPos("circle", "T1")
    s4 = cv2.getTrackbarPos("pentagon", "T1")

    mask = cv2.inRange(hsv, lower, upper)
    cnts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 300:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(c)

            if Switch == 1:
                if s1 == 1:
                    if len(approx) == 4:
                        cv2.putText(img, "Rectangle", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if s2 == 1:
                    if len(approx) == 3:
                        cv2.putText(img, "Triangle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if s3 == 1:
                    if 9 < len(approx) > 5:
                        cv2.putText(img, "Circle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if s4 == 1:
                    if len(approx) == 5:
                        cv2.putText(img, "Pentagon", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if len(approx) == 4:
                    cv2.putText(img, "Rectangle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                                2)
                elif len(approx) == 3:
                    cv2.putText(img, "Triangle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                (0, 255, 0), 2)
                elif len(approx) == 5:
                    cv2.putText(img, "Pentagon", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                (0, 255, 0), 2)
                elif len(approx) > 9:
                    cv2.putText(img, "Random shape", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                (0, 255, 0), 2)
                else:
                    cv2.putText(img, "Circle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                (0, 255, 0), 2)
    cv2.imshow("Result", img)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
