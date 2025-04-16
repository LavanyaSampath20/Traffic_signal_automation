import time

class AdaptiveSignalControl:
    def __init__(self, min_time=10, max_time=60):
        self.min_time = min_time
        self.max_time = max_time
        self.current_signal = None
        self.last_change_time = time.time()

    def calculate_green_time(self, traffic_density):
        return max(self.min_time, min(self.max_time, self.min_time + (self.max_time - self.min_time) * traffic_density))

    def update_signal(self, lane_densities):
        """
        Updates the traffic signal dynamically based on congestion.
        """
        most_congested_lane = max(lane_densities, key=lane_densities.get)
        green_time = self.calculate_green_time(lane_densities[most_congested_lane])

        # Auto-switch every 10s if no congestion detected
        if self.current_signal is None or time.time() - self.last_change_time >= green_time:
            self.current_signal = most_congested_lane
            self.last_change_time = time.time()

        # Ensure fairness, force switch every 10s
        if time.time() - self.last_change_time >= 10:
            self.current_signal = None
        
        return self.current_signal, green_time
