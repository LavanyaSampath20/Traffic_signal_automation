import time

class AdaptiveTrafficControl:
    def __init__(self):
        self.green_time = 10  # Default green light duration
        self.last_update_time = time.time()

    def update_signal(self, traffic_density):
        """
        Adjusts signal timing dynamically based on vehicle density.
        - More congestion → More green time (max 30 sec)
        - Less congestion → Minimum green time (10 sec)
        """
        max_green_time = 30
        min_green_time = 10

        self.green_time = min(max(min_green_time + (traffic_density // 5), min_green_time), max_green_time)
        self.last_update_time = time.time()

    def get_signal_status(self):
        """
        Returns 'Green' if within green time, otherwise 'Red'.
        """
        elapsed_time = time.time() - self.last_update_time
        if elapsed_time < self.green_time:
            return "Green"
        else:
            return "Red"
