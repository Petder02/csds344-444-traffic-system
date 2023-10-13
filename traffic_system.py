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

class PedestrianLight():
    def __init__(self, walk: bool, stop: bool):
        self.walk = walk
        self.stop = stop

    def set_walk(self):
        self.walk = True
        self.stop = False

    def set_stop(self):
        self.walk = False
        self.stop = True

    def get_walk(self):
        return self.walk

    def get_stop(self):
        return self.stop


class TrafficSystem():
    def __init__(self, north_light: TrafficLight, south_light: TrafficLight, east_light: TrafficLight, west_light: TrafficLight,
                 north_cross: PedestrianLight, south_cross: PedestrianLight, east_cross: PedestrianLight, west_cross: PedestrianLight,
                 red_time: float, green_time: float, yellow_time: float):
        self.north_light = north_light
        self.south_light = south_light
        self.east_light = east_light
        self.west_light = west_light
        self.north_cross = north_cross
        self.south_cross = south_cross
        self.east_cross = east_cross
        self.west_cross = west_cross
        self.red_time = red_time
        self.green_time = green_time
        self.yellow_time = yellow_time

    def get_north_south_time_remaining(self, time: float):
        if self.north_light.get_green():
            return self.green_time
        elif self.north_light.get_yellow():
            return self.yellow_time
        else:
            return self.red_time

    def get_east_west_time_remaining(self, time: float):
        if self.east_light.get_green():
            return self.green_time
        elif self.east_light.get_yellow():
            return self.yellow_time
        else:
            return self.red_time


def initialize_traffic_system():
    # Initialize the traffic lights
    north_light = TrafficLight(False, False, True, 10.0)  # Start with North red
    south_light = TrafficLight(False, False, True, 10.0)  # Start with South red
    east_light = TrafficLight(True, False, False, 10.0)  # Start with East green
    west_light = TrafficLight(True, False, False, 10.0)  # Start with West green
    north_cross = PedestrianLight(False, True)  # Start with North cross stop
    south_cross = PedestrianLight(False, True)  # Start with South cross stop
    east_cross = PedestrianLight(True, False)  # Start with East cross stop
    west_cross = PedestrianLight(True, False)  # Start with West cross stop

    traffic_system = TrafficSystem(north_light, south_light, east_light, west_light, north_cross, south_cross,
                                   east_cross, west_cross, 5.0, 10.0, 5.0)

    return traffic_system

def update_traffic_lights(cycle_time: float, traffic_system: TrafficSystem):
    if cycle_time < traffic_system.red_time:
        traffic_system.north_light.set_red()
        traffic_system.south_light.set_red()
        traffic_system.north_cross.set_stop()
        traffic_system.south_cross.set_stop()
        traffic_system.east_light.set_green()
        traffic_system.west_light.set_green()
        traffic_system.east_cross.set_walk()
        traffic_system.west_cross.set_walk()
    elif cycle_time < traffic_system.red_time + traffic_system.yellow_time:
        traffic_system.east_light.set_yellow()
        traffic_system.west_light.set_yellow()
    elif cycle_time < traffic_system.red_time + traffic_system.yellow_time + traffic_system.green_time:
        traffic_system.north_light.set_green()
        traffic_system.south_light.set_green()
        traffic_system.north_cross.set_walk()
        traffic_system.south_cross.set_walk()
        traffic_system.east_light.set_red()
        traffic_system.west_light.set_red()
        traffic_system.east_cross.set_stop()
        traffic_system.west_cross.set_stop()
    elif cycle_time < traffic_system.red_time + traffic_system.yellow_time + traffic_system.green_time + traffic_system.yellow_time:
        traffic_system.north_light.set_yellow()
        traffic_system.south_light.set_yellow()


def draw_traffic_lights(screen: pygame.Surface, traffic_system: TrafficSystem):
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    north_light_color = RED if traffic_system.north_light.get_red() else YELLOW if traffic_system.north_light.get_yellow() else GREEN
    south_light_color = RED if traffic_system.south_light.get_red() else YELLOW if traffic_system.south_light.get_yellow() else GREEN
    east_light_color = RED if traffic_system.east_light.get_red() else YELLOW if traffic_system.east_light.get_yellow() else GREEN
    west_light_color = RED if traffic_system.west_light.get_red() else YELLOW if traffic_system.west_light.get_yellow() else GREEN

    # Draw traffic lights
    pygame.draw.circle(screen, north_light_color, (300, 100), 20)  # North traffic light
    pygame.draw.circle(screen, south_light_color, (300, 500), 20)  # South traffic light
    pygame.draw.circle(screen, east_light_color, (100, 300), 20)  # East traffic light
    pygame.draw.circle(screen, west_light_color, (500, 300), 20)  # West traffic light

def draw_pedestrian_signs(screen: pygame.Surface, traffic_system: TrafficSystem):
    # North
    font = pygame.font.Font(None, 36)
    border_width = 10
    square_x = 150
    square_y = 150
    square_size = 75
    pygame.draw.rect(screen, (0, 0, 0), (
        square_x - border_width, square_y - border_width, square_size + 2 * border_width,
        square_size + 2 * border_width))
    pygame.draw.rect(screen, (0, 0, 0),
                     (square_x, square_y, square_size, square_size))  # Draw the filled square inside the border
    sign_text = "WALK" if traffic_system.north_cross.get_walk() else "STOP"
    sign_color = (255, 255, 255) if traffic_system.north_cross.get_walk() else (255, 0, 0)
    screen.blit(font.render('north', True, (255, 255, 255)), (square_x + 5, square_y + 5))
    screen.blit(font.render(sign_text, True, sign_color), (square_x + 5, square_y + 40))

    # east
    square_x = 375
    square_y = 150
    pygame.draw.rect(screen, (0, 0, 0), (
        square_x - border_width, square_y - border_width, square_size + 2 * border_width,
        square_size + 2 * border_width))
    pygame.draw.rect(screen, (0, 0, 0),
                     (square_x, square_y, square_size, square_size))  # Draw the filled square inside the border
    sign_text = "WALK" if traffic_system.east_cross.get_walk() else "STOP"
    sign_color = (255, 255, 255) if traffic_system.east_cross.get_walk() else (255, 0, 0)
    screen.blit(font.render('east', True, (255, 255, 255)), (square_x + 5, square_y + 5))
    screen.blit(font.render(sign_text, True, sign_color), (square_x + 5, square_y + 40))

    # west
    font = pygame.font.Font(None, 36)
    square_x = 150
    square_y = 375
    pygame.draw.rect(screen, (0, 0, 0), (
        square_x - border_width, square_y - border_width, square_size + 2 * border_width,
        square_size + 2 * border_width))
    pygame.draw.rect(screen, (0, 0, 0),
                     (square_x, square_y, square_size, square_size))  # Draw the filled square inside the border
    sign_text = "WALK" if traffic_system.west_cross.get_walk() else "STOP"
    sign_color = (255, 255, 255) if traffic_system.west_cross.get_walk() else (255, 0, 0)
    screen.blit(font.render('west', True, (255, 255, 255)), (square_x + 5, square_y + 5))
    screen.blit(font.render(sign_text, True, sign_color), (square_x + 5, square_y + 40))

    # south
    font = pygame.font.Font(None, 36)
    square_x = 375
    square_y = 375
    pygame.draw.rect(screen, (0, 0, 0), (
        square_x - border_width, square_y - border_width, square_size + 2 * border_width,
        square_size + 2 * border_width))
    pygame.draw.rect(screen, (0, 0, 0),
                     (square_x, square_y, square_size, square_size))  # Draw the filled square inside the border
    sign_text = "WALK" if traffic_system.south_cross.get_walk() else "STOP"
    sign_color = (255, 255, 255) if traffic_system.south_cross.get_walk() else (255, 0, 0)
    screen.blit(font.render('south', True, (255, 255, 255)), (square_x + 5, square_y + 5))
    screen.blit(font.render(sign_text, True, sign_color), (square_x + 5, square_y + 40))


def main():
    pygame.init()

    screenWidth = 600
    screenHeight = 600
    screenSize = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Traffic System")
    clock = pygame.time.Clock()

    traffic_system = initialize_traffic_system()

    screen.fill((255, 255, 255))  # Clear the screen

    # Draw roads
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 250, 600, 100))  # Horizontal road
    pygame.draw.rect(screen, (255, 255, 204), pygame.Rect(0, 295, 600, 10))  # Horizontal road line
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 0, 100, 600))  # Vertical road
    pygame.draw.rect(screen, (255, 255, 204), pygame.Rect(295, 0, 10, 600))  # Vertical road line

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the traffic lights based on elapsed time
        elapsed_time = pygame.time.get_ticks() / 1000  # convert milliseconds to seconds
        cycle_time = elapsed_time % (traffic_system.red_time + traffic_system.yellow_time + traffic_system.green_time + traffic_system.yellow_time)
        update_traffic_lights(cycle_time, traffic_system)

        # Draw traffic lights
        draw_traffic_lights(screen, traffic_system)

        # Draw pedestrian crossing signs
        draw_pedestrian_signs(screen, traffic_system)

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
