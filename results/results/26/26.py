import cv2
import numpy as np

src = cv2.imread('cup.jpg', -1)
src = cv2.resize(src, (403, 302))

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    1,
    20,
    None,
    10,
    75,
    3,
    75
)

circles = circles.astype(int)
if len(circles) > 0:
    out = src.copy()
    for x, y, r in circles[0]:
        cv2.circle(out, (x, y), r, (0, 0, 255), 3)
        cv2.circle(out, (x, y), 2, (0, 255, 0), 3)
    src = cv2.hconcat([src, out])

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image', src)
cv2.waitKey(0)
cv2.destroyAllWindows()
