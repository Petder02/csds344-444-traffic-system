import time
import pygame
import threading


class TrafficLight():
    """
    A class representing a traffic light and its current state

    """

    def __init__(self, is_green: bool, is_yellow: bool, is_red: bool, delay: float):
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

    def get_nort_south_time_remaining(self, time: float):
        """
        Get the time remaining for the north/south light
        """
        if self.north_south.get_green():
            return self.green_time # / time
        elif self.north_south.get_yellow():
            return self.yellow_time # / time
        else:
            return self.red_time # / time


    def get_east_west_time_remaining(self, time: float):
        """
        Get the time remaining for the east/west light
        """
        if self.east_west.get_green():
            return self.green_time # % time
        elif self.east_west.get_yellow():
            return self.yellow_time # % time
        else:
            return self.red_time # % time



def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Traffic System")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Initialize the traffic lights
        north_south = TrafficLight(False, False, True, 10.0)  # Start with North/South red
        east_west = TrafficLight(True, False, False, 10.0)    # Start with East/West green
        traffic_system = TrafficSystem(north_south, east_west, 10.0, 10.0, 2.0)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw roads
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 250, 600, 100))  # Horizontal road
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 0, 100, 600))  # Vertical road

        # Update the traffic lights based on elapsed time
        elapsed_time = pygame.time.get_ticks() / 1000  # convert milliseconds to seconds
        if elapsed_time % (traffic_system.red_time + traffic_system.green_time + traffic_system.yellow_time) < traffic_system.red_time:
            north_south.set_red()
            east_west.set_green()
        elif elapsed_time % (traffic_system.red_time + traffic_system.green_time + traffic_system.yellow_time) < traffic_system.red_time + traffic_system.green_time:
            north_south.set_green()
            east_west.set_red()
        else:
            north_south.set_yellow()
            east_west.set_red()

        # Draw traffic lights
        north_south_light_color = (255, 0, 0) if north_south.get_red() else (255, 255, 0) if north_south.get_yellow() else (0, 255, 0)
        east_west_light_color = (255, 0, 0) if east_west.get_red() else (255, 255, 0) if east_west.get_yellow() else (0, 255, 0)
        pygame.draw.circle(screen, north_south_light_color, (300, 200), 20)  # North/South traffic light
        pygame.draw.circle(screen, east_west_light_color, (250, 300), 20)  # East/West traffic light

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()