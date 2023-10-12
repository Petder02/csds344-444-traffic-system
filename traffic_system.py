# Starter file for the project basically

class TrafficLight():
    """
    A class representing a traffic light and its current state

    """

    def __init__(self, is_green: bool, is_yellow: bool, is_red: bool, delay: float)
        """
        Initialize a traffic light

        is_green: Is the light green?
        is_yellow: Is the light yellow?
        is_red: Is the light red?
        delay: Amount of time between any light changes
        """
        self.is_green = is_green
        self.is_yellow = is_yellow
        self.is_red = is_red
        self.delay = delay


    def set_green(self):
        """
        Set the light to green
        """
        self.is_green = True
        self.is_yellow = False
        self.is_red = False


    def set_yellow(self):
        """
        Set the light to yellow
        """
        self.is_green = False
        self.is_yellow = True
        self.is_red = False


    def set_red(self):
        """
        Set the light to red
        """
        self.is_green = False
        self.is_yellow = False
        self.is_red = True


    def get_green(self):
        """
        Get the green state
        """
        return self.is_green

    def get_yellow(self):
        """
        Get the yellow state
        """
        return self.is_yellow


    def get_red(self):
        """
        Get the red state
        """
        return self.is_red


    def get_delay(self):
        """
        Get the delay
        """
        return self.delay


class TrafficSystem():
    """
    Class representing a full traffic system

    """

    def __init__(self, north_south: TrafficLight, east_west: TrafficLight,
                 red_time: float, green_time: float, yellow_time: float):
        """
        Initialize a traffic system

        north_south: Traffic light for north/south direction
        east_west: Traffic light for east/west direction
        red_time: Time for red light
        green_time: Time for green light
        yellow_time: Time for yellow light
        """
        self.north_south = north_south
        self.east_west = east_west
        self.red_time = red_time
        self.green_time = green_time
        self.yellow_time = yellow_time

    









