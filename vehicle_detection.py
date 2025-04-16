import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model (fine-tuned for top-view is ideal)
model = YOLO("yolov8n.pt")

def detect_cars(frame, prev_positions):
    """
    Detects only cars and classifies movement.
    - Green = Moving
    - Red = Stopped
    """
    results = model(frame)
    current_positions = {}

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            label = int(box.cls[0])  # Class ID
            confidence = float(box.conf[0])  # Confidence Score

            # COCO Class 2 = "Car"
            if label == 2 and confidence > 0.3:
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                current_positions[(cx, cy)] = (x1, y1, x2, y2)

                # Determine movement (Threshold: 10 pixels)
                moving = any(np.linalg.norm(np.array([cx, cy]) - np.array(prev)) > 10 for prev in prev_positions)

                # Assign color (Green = Moving, Red = Stopped)
                color = (0, 255, 0) if moving else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    return frame, current_positions
