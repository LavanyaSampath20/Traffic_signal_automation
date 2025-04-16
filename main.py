import cv2
import time
from vehicle_detection import detect_vehicles
from traffic_analysis import compute_traffic_density
from signal_control import AdaptiveSignalControl

def main():
    cap = cv2.VideoCapture("traffic_video.mp4") 
    mog2_bg = cv2.createBackgroundSubtractorMOG2()
    
    traffic_system = AdaptiveSignalControl()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Simulating multiple lanes (split frame into 3 parts)
        h, w, _ = frame.shape
        lanes = {
            "Left": frame[:, :w//3],
            "Center": frame[:, w//3:2*w//3],
            "Right": frame[:, 2*w//3:]
        }

        lane_densities = {}

        for lane_name, lane_frame in lanes.items():
            vehicles = detect_vehicles(lane_frame, mog2_bg)
            density = compute_traffic_density(vehicles, lane_frame.shape)
            lane_densities[lane_name] = density

        # Adaptive signal control with automatic 10-sec switching
        traffic_system.control_traffic(lane_densities)

        # Display lanes with bounding boxes
        for lane_name, lane_frame in lanes.items():
            for (x, y, w, h) in detect_vehicles(lane_frame, mog2_bg):
                cv2.rectangle(lane_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Traffic Monitoring", frame)
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
