import cv2
import numpy as np

images = []
labels = []

fixed_size = (100, 100)

for index in range(100):
    filename = f'images/h0/{index:03d}.pgm'
    print(f'Reading {filename}')
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f'Error: {filename} could not be read!')
        continue

    img_resized = cv2.resize(img, fixed_size)
    images.append(img_resized)
    labels.append(0)

images_array = np.array(images, dtype=np.uint8)
labels_array = np.array(labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()
model.train(images_array, labels_array)
model.save('faces.data')
print('Training done and model saved.')
