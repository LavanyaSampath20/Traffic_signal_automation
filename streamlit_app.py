import streamlit as st
import cv2
import time
import numpy as np
from vehicle_detection import detect_cars
from adaptive_signal import AdaptiveSignal

# Initialize Traffic Signal System
signal_controller = AdaptiveSignal()

# Streamlit UI
st.title("🚦 Adaptive Traffic Signal System with Countdown Timer & Stop Time Tracking")

# Traffic Light Widget with Countdown Color
def traffic_light_widget(status, countdown):
    """Displays traffic light status with countdown color."""
    if status == "GREEN":
        return f"🟩 Countdown: {countdown} sec"
    else:
        return f"🟥 Countdown: {countdown} sec"

# Upload video
video_file = st.file_uploader("Upload a traffic video", type=["mp4", "avi", "mov"])

if video_file:
    # Save uploaded file as temp video
    tfile = "temp_video.mp4"
    with open(tfile, "wb") as f:
        f.write(video_file.read())

    cap = cv2.VideoCapture(tfile)

    # Placeholders for Streamlit display
    video_placeholder = st.empty()
    signal_placeholder = st.empty()
    light_placeholder = st.empty()
    stop_time_placeholder = st.empty()

    prev_positions = {}  # Store previous frame positions

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect only cars and classify movement
        processed_frame, current_positions = detect_cars(frame, prev_positions)
        prev_positions = current_positions  # Update for next frame

        # Count moving and total cars
        total_cars = len(current_positions)
        moving_cars = sum(
            np.linalg.norm(np.array(curr) - np.array(prev)) > 10
            for curr in current_positions.keys()
            for prev in prev_positions.keys()
        )

        # Get stable signal update, countdown timer, and stop time
        signal_status, countdown, red_stop_time, green_stop_time = signal_controller.update_signal(
            moving_cars, total_cars
        )

        # Convert OpenCV image to RGB for Streamlit
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

        # Display results in Streamlit
        video_placeholder.image(processed_frame, channels="RGB")
        signal_placeholder.subheader(f"🚦 Signal: {signal_status} (Stable)")
        light_placeholder.markdown(f"### {traffic_light_widget(signal_status, countdown)}")
        
        # Show stop time count for RED & GREEN
        stop_time_placeholder.markdown(
            f"""
            ### ⏳ Total Stop Time:
            🔴 Red: **{red_stop_time} sec**  
            🟩 Green: **{green_stop_time} sec**  
            """
        )

        # Pause for real-time effect
        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()
