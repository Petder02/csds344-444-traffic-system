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
        north_light = TrafficLight(False, False, True, 10.0)  # Start with North red
        south_light = TrafficLight(False, False, True, 10.0)  # Start with South red
        east_light = TrafficLight(True, False, False, 10.0)   # Start with East green
        west_light = TrafficLight(True, False, False, 10.0)   # Start with West green
        north_cross = PedestrianLight(False, True)            # Start with North cross stop
        south_cross = PedestrianLight(False, True)            # Start with South cross stop
        east_cross = PedestrianLight(True, False)             # Start with East cross stop
        west_cross = PedestrianLight(True, False)             # Start with West cross stop

        traffic_system = TrafficSystem(north_light, south_light, east_light, west_light, north_cross, south_cross, east_cross, west_cross, 10.0, 10.0, 2.0)

        screen.fill((255, 255, 255))  # Clear the screen

        # Draw roads
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 250, 600, 100))  # Horizontal road
        pygame.draw.rect(screen, (255, 255, 204), pygame.Rect(0, 295, 600, 10))   # Horizontal road line
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(250, 0, 100, 600))  # Vertical road
        pygame.draw.rect(screen, (255, 255, 204), pygame.Rect(295, 0, 10, 600))   # Vertical road line

        # Update the traffic lights based on elapsed time
        elapsed_time = pygame.time.get_ticks() / 1000  # convert milliseconds to seconds
        if elapsed_time % (traffic_system.red_time + traffic_system.green_time + traffic_system.yellow_time) < traffic_system.red_time:
            north_light.set_red()
            south_light.set_red()
            north_cross.set_stop()
            south_cross.set_stop()
            east_light.set_green()
            west_light.set_green()
            east_cross.set_walk()
            west_cross.set_walk()
        elif elapsed_time % (traffic_system.red_time + traffic_system.green_time + traffic_system.yellow_time) < traffic_system.red_time + traffic_system.green_time:
            north_light.set_green()
            south_light.set_green()
            north_cross.set_walk()
            south_cross.set_walk()
            east_light.set_red()
            west_light.set_red()
            east_cross.set_stop()
            west_cross.set_stop()
        else:
            north_light.set_yellow()
            south_light.set_yellow()
            east_light.set_red()
            west_light.set_red()
            north_cross.set_stop()
            south_cross.set_stop()

        # Draw traffic lights
        north_light_color = (255, 0, 0) if north_light.get_red() else (255, 255, 0) if north_light.get_yellow() else (0, 255, 0)
        south_light_color = (255, 0, 0) if south_light.get_red() else (255, 255, 0) if south_light.get_yellow() else (0, 255, 0)
        east_light_color = (255, 0, 0) if east_light.get_red() else (255, 255, 0) if east_light.get_yellow() else (0, 255, 0)
        west_light_color = (255, 0, 0) if west_light.get_red() else (255, 255, 0) if west_light.get_yellow() else (0, 255, 0)
        pygame.draw.circle(screen, north_light_color, (300, 100), 20)  # North traffic light
        pygame.draw.circle(screen, south_light_color, (300, 500), 20)  # South traffic light
        pygame.draw.circle(screen, east_light_color, (100, 300), 20)  # East traffic light
        pygame.draw.circle(screen, west_light_color, (500, 300), 20)  # West traffic light

        # Draw pedestrian crossing signs
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
        sign_text = "WALK" if north_cross.get_walk() else "STOP"
        sign_color = (255, 255, 255) if north_cross.get_walk() else (255, 0, 0)
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
        sign_text = "WALK" if east_cross.get_walk() else "STOP"
        sign_color = (255, 255, 255) if east_cross.get_walk() else (255, 0, 0)
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
        sign_text = "WALK" if west_cross.get_walk() else "STOP"
        sign_color = (255, 255, 255) if west_cross.get_walk() else (255, 0, 0)
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
        sign_text = "WALK" if south_cross.get_walk() else "STOP"
        sign_color = (255, 255, 255) if south_cross.get_walk() else (255, 0, 0)
        screen.blit(font.render('south', True, (255, 255, 255)), (square_x + 5, square_y + 5))
        screen.blit(font.render(sign_text, True, sign_color), (square_x + 5, square_y + 40))

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
