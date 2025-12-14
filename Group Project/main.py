import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
import json
import datetime
import csv
from picamera2 import Picamera2
from ultralytics import YOLO

MODEL_PATH = "yolov8n.pt"
SEATS_FILE = "seats.json"
LOG_FILE = "attendance_log.csv"
CONF_THRESHOLD = 0.5

def load_seats():
    try:
        with open(SEATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {SEATS_FILE} not found. Please run calib_seats.py first.")
        return []

def save_to_local_csv(total, present, absent_list):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Date", "Time", "Total Seats", "Present Count", "Absent List"])

        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        absent_str = ", ".join(absent_list) if absent_list else "None"

        writer.writerow([date_str, time_str, total, present, absent_str])
        print(f"Attendance record saved to {LOG_FILE}")

def check_attendance(frame, model, seats):
    results = model(frame, classes=[0], conf=CONF_THRESHOLD, verbose=False)

    person_centers = []
    for box in results[0].boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        person_centers.append((cx, cy))

    status = {}
    output_frame = frame.copy()

    for seat in seats:
        sx1, sy1, sx2, sy2 = seat["coords"]
        label = seat["label"]
        is_occupied = False

        for px, py in person_centers:
            if sx1 < px < sx2 and sy1 < py < sy2:
                is_occupied = True
                break

        status[label] = is_occupied

        color = (0, 255, 0) if is_occupied else (0, 0, 255)
        cv2.rectangle(output_frame, (sx1, sy1), (sx2, sy2), color, 2)
        cv2.putText(output_frame, label, (sx1, sy1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return output_frame, status

def main():
    print("Loading YOLO model...")
    model = YOLO(MODEL_PATH)

    print("Loading seat configuration...")
    seats = load_seats()
    if not seats:
        return

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)})
    picam2.configure(config)
    picam2.start()

    cv2.namedWindow("SmartSeat Monitor", cv2.WINDOW_NORMAL)

    print("\nSystem ready. Controls:")
    print(" [SPACE]  Capture and take attendance")
    print(" [q]      Quit program")

    try:
        while True:
            frame = picam2.capture_array()

            cv2.imshow("SmartSeat Monitor", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 32:
                print("\n--- Attendance Check Started ---")

                result_img, status = check_attendance(frame, model, seats)

                absent_list = [name for name, present in status.items() if not present]
                total = len(seats)
                present_count = total - len(absent_list)

                print(f"Attendance: {present_count}/{total}")
                print(f"Absent: {absent_list}")

                save_to_local_csv(total, present_count, absent_list)

                cv2.imshow("Attendance Result", result_img)
                print("Press any key to return to monitoring...")
                cv2.waitKey(0)
                cv2.destroyWindow("Attendance Result")

            elif key == ord("q"):
                break

    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
