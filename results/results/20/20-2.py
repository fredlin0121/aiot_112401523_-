from picamera2 import Picamera2, Preview
import cv2
import numpy as np

model = cv2.face.LBPHFaceRecognizer_create()
model.read('faces.data')
print('Loaded training data successfully')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

names = ['ckk']

try:
    while True:
        frame = picam2.capture_array()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (600, 336))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (400, 400))
            val = model.predict(face_img)
            print('label:{}, conf:{:.1f}'.format(val[0], val[1]))
            if val[1] < 50:
                cv2.putText(
                    frame, names[val[0]], (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3
                )
        cv2.imshow('video', frame)
        if cv2.waitKey(1) == 27:
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    picam2.stop()
    cv2.destroyAllWindows()
