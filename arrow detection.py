import cv2
import numpy as np
def find_arrow_direction(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, bin_img = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    cnts, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    msg = "no arrow"
    for c in cnts:
        if cv2.contourArea(c) < 1000:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        left = bin_img[y:y+h, x:x + w//2]
        right = bin_img[y:y+h, x + w//2:x+w]

        left_cnt = cv2.countNonZero(left)
        right_cnt = cv2.countNonZero(right)

        if left_cnt < right_cnt:
            msg = "Left"
        else:
            msg = "Right"
        cv2.putText(img, "Arrow: " + msg, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 2)
        break
    return img, msg
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("camera is not working")
    exit()
while True:
    ok, frame = cam.read()
    if not ok:
        break
    result, text = find_arrow_direction(frame)
    cv2.imshow("Direction detection", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
