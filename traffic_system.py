import time
import pygame
import threading

class TrafficLight():
    def __init__(self, is_green: bool, is_yellow: bool, is_red: bool, delay: float):
        self.is_green = is_green
        self.is_yellow = is_yellow
        self.is_red = is_red
        self.delay = delay

    def set_green(self):
        self.is_green = True
        self.is_yellow = False
        self.is_red = False

    def set_yellow(self):
        self.is_green = False
        self.is_yellow = True
        self.is_red = False

    def set_red(self):
        self.is_green = False
        self.is_yellow = False
        self.is_red = True

    def get_green(self):
        return self.is_green

    def get_yellow(self):
        return self.is_yellow

    def get_red(self):
        return self.is_red

    def get_delay(self):
        return self.delay

class TrafficSystem():
    def __init__(self, north: TrafficLight, south: TrafficLight, east: TrafficLight, west: TrafficLight, red_time: float, green_time: float, yellow_time: float):
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.red_time = red_time
        self.green_time = green_time
        self.yellow_time = yellow_time

    def get_nort_south_time_remaining(self, time: float):
        if self.north.get_green():
            return self.green_time
        elif self.north.get_yellow():
            return self.yellow_time
        else:
            return self.red_time

    def get_east_west_time_remaining(self, time: float):
        if self.east.get_green():
            return self.green_time
        elif self.east.get_yellow():
            return self.yellow_time
        else:
            return self.red_time

def main():
    pygame.init()

    screenWidth = 600
    screenHeight = 600
    screenSize = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Traffic System")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Initialize the traffic lights
        north = TrafficLight(False, False, True, 10.0)  # Start with North red
        south = TrafficLight(False, False, True, 10.0)  # Start with South red
        east = TrafficLight(True, False, False, 10.0)   # Start with East green
        west = TrafficLight(True, False, False, 10.0)   # Start with West green
        traffic_system = TrafficSystem(north, south, east, west, 10.0, 10.0, 2.0)

        screen.fill((255, 255, 255))  # Clear the screen

        # Draw roads
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 250, 600, 100))  # Horizontal road
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 0, 100, 600))  # Vertical road

        # Update the traffic lights based on elapsed time
        elapsed_time = pygame.time.get_ticks() / 1000  # convert milliseconds to seconds
        if elapsed_time % (traffic_system.red_time + traffic_system.green_time + traffic_system.yellow_time) < traffic_system.red_time:
            north.set_red()
            south.set_red()
            east.set_green()
            west.set_green()
        elif elapsed_time % (traffic_system.red_time + traffic_system.green_time + traffic_system.yellow_time) < traffic_system.red_time + traffic_system.green_time:
            north.set_green()
            south.set_green()
            east.set_red()
            west.set_red()
        else:
            north.set_yellow()
            south.set_yellow()
            east.set_red()
            west.set_red()

        # Draw traffic lights
        north_light_color = (255, 0, 0) if north.get_red() else (255, 255, 0) if north.get_yellow() else (0, 255, 0)
        south_light_color = (255, 0, 0) if south.get_red() else (255, 255, 0) if south.get_yellow() else (0, 255, 0)
        east_light_color = (255, 0, 0) if east.get_red() else (255, 255, 0) if east.get_yellow() else (0, 255, 0)
        west_light_color = (255, 0, 0) if west.get_red() else (255, 255, 0) if west.get_yellow() else (0, 255, 0)
        pygame.draw.circle(screen, north_light_color, (300, 100), 20)  # North traffic light
        pygame.draw.circle(screen, south_light_color, (300, 500), 20)  # South traffic light
        pygame.draw.circle(screen, east_light_color, (100, 300), 20)  # East traffic light
        pygame.draw.circle(screen, west_light_color, (500, 300), 20)  # West traffic light

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
