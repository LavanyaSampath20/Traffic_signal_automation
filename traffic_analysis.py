import cv2
import numpy as np

def compute_traffic_density(frame):
    mog2 = cv2.createBackgroundSubtractorMOG2()
    fg_mask = mog2.apply(frame)
    
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = frame.shape[0] * frame.shape[1]
    moving_area = sum(cv2.contourArea(cnt) for cnt in contours if cv2.contourArea(cnt) > 500)
    
    density = (moving_area / total_area) * 100
    return density
