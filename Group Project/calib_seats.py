import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
import json
from picamera2 import Picamera2

def draw_roi(event, x, y, flags, state):
    if event == cv2.EVENT_LBUTTONDOWN:
        state["drawing"] = True
        state["ix"], state["iy"] = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if state["drawing"] and state["current_frame"] is not None:
            state["temp_frame"] = state["current_frame"].copy()
            cv2.rectangle(state["temp_frame"], (state["ix"], state["iy"]), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        state["drawing"] = False
        if state["current_frame"] is None:
            return

        x1, x2 = sorted([state["ix"], x])
        y1, y2 = sorted([state["iy"], y])

        cv2.rectangle(state["current_frame"], (x1, y1), (x2, y2), (0, 255, 0), 2)

        seat_id = state["seat_counter"]
        label = f"Seat {seat_id}"

        cv2.putText(
            state["current_frame"],
            label,
            (x1, max(0, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

        state["seats"].append({"id": seat_id, "label": label, "coords": [x1, y1, x2, y2]})
        print(f"Added: {label}")

        state["seat_counter"] += 1
        state["temp_frame"] = state["current_frame"].copy()

def main():
    state = {
        "drawing": False,
        "ix": -1,
        "iy": -1,
        "current_frame": None,
        "temp_frame": None,
        "seats": [],
        "seat_counter": 1
    }

    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (1280, 720)})
    picam2.configure(config)
    picam2.start()

    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
    print("Step 1: Adjust camera angle. Press SPACE to freeze frame and start calibration.")

    while True:
        frame = picam2.capture_array()
        cv2.imshow("Preview", frame)
        k = cv2.waitKey(1) & 0xFF

        if k == 32:
            state["current_frame"] = frame.copy()
            state["temp_frame"] = frame.copy()
            break
        if k == ord("q"):
            picam2.stop()
            cv2.destroyAllWindows()
            return

    cv2.destroyWindow("Preview")

    cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Calibration", draw_roi, state)

    print("Step 2: Draw seat regions with mouse. Press 's' to save, 'q' to quit.")

    while True:
        display = state["temp_frame"] if state["temp_frame"] is not None else state["current_frame"]
        cv2.imshow("Calibration", display)
        k = cv2.waitKey(1) & 0xFF

        if k == ord("s"):
            with open("seats.json", "w", encoding="utf-8") as f:
                json.dump(state["seats"], f, indent=4)
            print(f"Saved successfully. Total seats: {len(state['seats'])}")
            break

        if k == ord("q"):
            break

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
