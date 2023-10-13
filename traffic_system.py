import argparse
import pygame


class TrafficLight:
    """
    A class representing a traffic light

    """
    def __init__(self, is_green: bool, is_yellow: bool, is_red: bool):
        self.is_green = is_green
        self.is_yellow = is_yellow
        self.is_red = is_red

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


class PedestrianLight:
    """
    A class representing a pedestrian light

    """
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


class TrafficSystem:
    """
    A class representing a traffic system

    """
    def __init__(self, north_light: TrafficLight, south_light: TrafficLight, east_light: TrafficLight,
                 west_light: TrafficLight,
                 north_cross: PedestrianLight, south_cross: PedestrianLight, east_cross: PedestrianLight,
                 west_cross: PedestrianLight,
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


def initialize_traffic_system(red_time: float, green_time: float, yellow_time: float):
    """
    Initializes the traffic system for the GUI

    :param red_time: The time (secs) that the red light is on
    :param green_time: The time (secs) that the green light is on
    :param yellow_time: The time (secs) that the yellow light is on
    """
    # Initialize the traffic lights
    north_light = TrafficLight(False, False, True)  # Start with North red
    south_light = TrafficLight(False, False, True)  # Start with South red
    east_light = TrafficLight(True, False, False)  # Start with East green
    west_light = TrafficLight(True, False, False)  # Start with West green
    north_cross = PedestrianLight(False, True)  # Start with North cross stop
    south_cross = PedestrianLight(False, True)  # Start with South cross stop
    east_cross = PedestrianLight(True, False)  # Start with East cross stop
    west_cross = PedestrianLight(True, False)  # Start with West cross stop

    traffic_system = TrafficSystem(north_light, south_light, east_light, west_light, north_cross, south_cross,
                                   east_cross, west_cross, red_time, green_time, yellow_time)

    return traffic_system


def update_traffic_lights(cycle_time: float, traffic_system: TrafficSystem):
    """
    Updates the traffic lights based on the cycle time

    :param cycle_time: The time (secs) since the start of the cycle
    :param traffic_system: The traffic system
    """
    east_west_green = cycle_time < traffic_system.red_time
    east_west_yellow = cycle_time < traffic_system.red_time + traffic_system.yellow_time
    north_south_green = cycle_time < traffic_system.red_time + traffic_system.yellow_time + traffic_system.green_time
    north_south_yellow = cycle_time < traffic_system.red_time + traffic_system.yellow_time + traffic_system.green_time + traffic_system.yellow_time
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
    """
    Draws traffic lights based on the state of the traffic lights

    :param screen: The pygame screen
    :param traffic_system: The traffic system
    """
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
    """
    Draws pedestrian crossing signs based on the state of the pedestrian crossing lights

    :param screen: The pygame screen
    :param traffic_system: The traffic system
    """
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

    # East
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

    # West
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

    # South
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


def main(red_time: float, green_time: float, yellow_time: float):
    """
    Main function that runs the traffic system

    :param red_time: The time (secs) that the red light is on
    :param green_time: The time (secs) that the green light is on
    :param yellow_time: The time (secs) that the yellow light is on
    """
    pygame.init()

    screenWidth = 600
    screenHeight = 600
    screenSize = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Traffic System")
    clock = pygame.time.Clock()

    traffic_system = initialize_traffic_system(red_time, green_time, yellow_time)

    screen.fill((255, 255, 255))  # Clear the screen

    # Draw roads
    GRAY = (200, 200, 200)
    LIGHT_YELLOW = (255, 255, 204)
    pygame.draw.rect(screen, GRAY, pygame.Rect(0, 250, 600, 100))         # Horizontal road
    pygame.draw.rect(screen, LIGHT_YELLOW, pygame.Rect(0, 295, 600, 10))  # Horizontal road line
    pygame.draw.rect(screen, GRAY, pygame.Rect(250, 0, 100, 600))         # Vertical road
    pygame.draw.rect(screen, LIGHT_YELLOW, pygame.Rect(295, 0, 10, 600))  # Vertical road line

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the traffic lights based on elapsed time
        elapsed_time = pygame.time.get_ticks() / 1000  # convert milliseconds to seconds
        cycle_time = elapsed_time % (
                    traffic_system.red_time + traffic_system.yellow_time + traffic_system.green_time + traffic_system.yellow_time)
        update_traffic_lights(cycle_time, traffic_system)

        # Draw traffic lights
        draw_traffic_lights(screen, traffic_system)

        # Draw pedestrian crossing signs
        draw_pedestrian_signs(screen, traffic_system)

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control the frame rate

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Traffic System',
        description='Simulates a basic traffic system'
    )
    parser.add_argument('--red-time', type=float, default=10.0, help='The time (secs) that the red light is on')
    parser.add_argument('--green-time', type=float, default=10.0, help='The time (secs) that the green light is on')
    parser.add_argument('--yellow-time', type=float, default=5.0, help='The time (secs) that the yellow light is on')

    args = parser.parse_args()
    red_time: float = float(args.red_time)
    green_time: float = float(args.green_time)
    yellow_time: float = float(args.yellow_time)

    main(red_time, green_time, yellow_time)
