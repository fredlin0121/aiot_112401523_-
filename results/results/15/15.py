from picamera2 import Picamera2
import time

picam2 = Picamera2()

picam2.start()

time.sleep(3)

picam2.capture_file("image.jpeg")

picam2.stop()
