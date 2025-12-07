import cv2
import numpy as np

canvas = np.zeros((512, 512, 3), dtype=np.uint8)
canvas.fill(255)

cv2.line(canvas, (50, 50), (450, 50), (255, 0, 0), 3)

cv2.circle(canvas, (256, 256), 100, (0, 255, 0), -1)

cv2.ellipse(canvas, (256, 400), (150, 75), 45, 0, 360, (0, 0, 255), 3)

pts = np.array([[100, 200], [200, 300], [300, 200], [200, 100]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(canvas, [pts], isClosed=True, color=(0, 255, 255), thickness=2)

cv2.imshow("Shapes", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
