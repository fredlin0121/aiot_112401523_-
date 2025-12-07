from ultralytics import YOLO
import os
import cv2
import matplotlib.pyplot as plt

save_dir = 'results/'
os.makedirs(save_dir, exist_ok=True)

model = YOLO('yolov8n.pt')

image_path = 'image.jpeg'
results = model(image_path)

annotated_image = results[0].plot()

plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

cv2.imwrite(os.path.join(save_dir, 'detected_image.jpeg'), annotated_image)
print(f"Saved detection result to {os.path.join(save_dir, 'detected_image.jpeg')}")

detected_classes = set()
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    class_name = model.names[cls_id]
    detected_classes.add(class_name)

print("Detected Classes:")
for cls in detected_classes:
    print(f"- {cls}")
