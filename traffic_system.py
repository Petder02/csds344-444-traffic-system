# Starter file for the project basically

class TrafficLight():
    """
    A class representing a traffic light and its current state

    """

    def __init__(self, green_time: int, yellow_time: int, red_time: int):
        """
        Initialize a traffic light

        state: The state of the traffic light
        time: The time the traffic light has been in its current state
        """
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.red_time = red_time

    def get_state(self, time: int) -> str:
        pass

    def __str__(self):
        return f"Green: {self.green_time}, Yellow: {self.yellow_time}, Red: {self.red_time}"
