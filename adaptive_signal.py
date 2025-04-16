import time

class AdaptiveSignal:
    def __init__(self):
        self.signal_status = "RED"
        self.last_switch_time = time.time()
        self.countdown = 10  # Initial countdown set to 10 seconds

        # Stop time counters
        self.red_stop_time = 0
        self.green_stop_time = 0
        self.last_update_time = time.time()

    def update_signal(self, moving_cars, total_cars):
        """
        Updates the traffic signal and maintains a countdown timer.
        - Green if congestion is high or if 10 sec have passed.
        - Countdown decreases every second.
        - Tracks total stop time for RED & GREEN.
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_switch_time
        time_since_last_update = current_time - self.last_update_time

        congestion_ratio = (total_cars - moving_cars) / total_cars if total_cars > 0 else 0

        if self.signal_status == "RED":
            if elapsed_time >= 10 or congestion_ratio > 0.5:
                self.signal_status = "GREEN"
                self.last_switch_time = current_time
                self.countdown = 10
                self.red_stop_time = 0  # Reset RED stop time
            else:
                self.countdown = max(0, 10 - int(elapsed_time))
                self.red_stop_time += time_since_last_update

        elif self.signal_status == "GREEN":
            if elapsed_time >= 10 and congestion_ratio < 0.3:
                self.signal_status = "RED"
                self.last_switch_time = current_time
                self.countdown = 10
                self.green_stop_time = 0  # Reset GREEN stop time
            else:
                self.countdown = max(0, 10 - int(elapsed_time))
                self.green_stop_time += time_since_last_update

        self.last_update_time = current_time  # Update last time

        return self.signal_status, self.countdown, int(self.red_stop_time), int(self.green_stop_time)
