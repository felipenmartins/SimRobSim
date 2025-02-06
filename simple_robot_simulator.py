# Example file showing a circle moving on screen
import pygame
from pygame.mixer_music import play
import math

# pygame setup
pygame.init()
pygame.mouse.set_visible(True)
pygame.display.set_caption("Simple Robot Simulator")
pygame.display.set_icon(pygame.image.load("robot-face.png"))

# Create the screen
screen = pygame.display.set_mode((1280, 720))
BACKGROUND_COLOR = (220, 220, 220)
count_frames = 0 # Count the number of frames

clock = pygame.time.Clock()
running = True  # Exit the program when False
dt = clock.tick(60) / 1000  # delta_d = 60 ms 
print_pos = True # Print the robot pose on the screen when True
show_path = True # Show robot path on the screen when True
path = tuple() # Store the robot path

LIN_SPEED = 200  # pixels per second
ANG_SPEED = 2    # radians per second
ROBOT_SIZE = 100
robot_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)  # initial position
orientation = 0  # initial orientation in radians
prev_robot_pos = (robot_pos.x, robot_pos.y) # Store the previous robot position

# robot_surface = pygame.Surface((ROBOT_SIZE, ROBOT_SIZE))
robot_surface = pygame.image.load("roomba-top-view-removebg.png").convert_alpha()
# robot_surface.set_colorkey("white")
robot_rect = robot_surface.get_rect()
robot_rect.center = robot_pos

# Draw the triangle inside the robot_surface to indicate the orientation
TRIANG_SIZE = 16
draw_triangle = False

# Make a copy of the robot_surface to rotate it with respect to the original one
new_robot_surface = pygame.transform.rotate(robot_surface, orientation%360)
new_robot_rect = new_robot_surface.get_rect()
new_robot_rect.center = robot_pos

# Functions

def robot_linear_mov(lin_speed, robot_pos):
    '''Apply linear movement to the robot at desired linear speed 
    and return new reobot position.'''
    robot_pos.x += lin_speed * math.cos(orientation) * dt
    robot_pos.y -= lin_speed * math.sin(orientation) * dt

    return robot_pos


def robot_angular_mov(ang_speed, orientation):
    '''Apply angular movement to the robot at desired angular speed
    and return new robot orientation.'''
    orientation += ang_speed * dt
    if orientation > math.pi:
        orientation -= 2 * math.pi
    elif orientation < - math.pi:
        orientation += 2 * math.pi

    return orientation


# Print instructions to control the robot and interact with the simulator
print("Welcome to the Simple Robot Simulator!")
print("Use the arrow keys to move the robot.")
print("Press 'c' to move the robot to the Center of the screen.")
print("Press '9' to rotate the robot by 90 degrees.")
print("Press 'p' to toggle Printing the robot position.")
print("Press 's' to toggle Showing the robot path.")
print("Press 'r' to Reset (clear) the robot path.")
print("Press 't' to draw a Triangle to indicate the orientation of the robot.")


# Main loop

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            robot_pos.x, robot_pos.y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            # Move the robot to the center of the screen and reset its orientation
            if keys[pygame.K_c]:
                robot_pos.x = screen.get_width() / 2
                robot_pos.y = screen.get_height() / 2
                orientation = 0
            # Toggle printing of robot position
            if keys[pygame.K_p]:
                print_pos = not print_pos
            # Toggle robot path 
            if keys[pygame.K_s]:
                show_path = not show_path
            # Clear the robot path
            if keys[pygame.K_r]:
                path = tuple()
            # Rotate the robot by 90 degrees
            if keys[pygame.K_9]:
                orientation += math.pi/2
                if orientation > math.pi:
                    orientation -= 2 * math.pi
            # Draw a triangle to indicate the orientation of the robot
            if keys[pygame.K_t]:
                draw_triangle = not draw_triangle

    # If the robot is moving, store its position in the path list and update the previous robot position
    if ((int(robot_pos.x) != prev_robot_pos[0]) or (int(robot_pos.y) != prev_robot_pos[1])):
        path += ((int(robot_pos.x), int(robot_pos.y)),)
        prev_robot_pos = (int(robot_pos.x), int(robot_pos.y))

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    # Draw the grid
    horizontal_line = pygame.draw.line(screen, "gray", (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
    vertical_line = pygame.draw.line(screen, "gray", (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))    

    # Move the robot with the arrow keys
    keys = pygame.key.get_pressed()
    # Move the robot
    if keys[pygame.K_UP]:
        robot_pos = robot_linear_mov(LIN_SPEED, robot_pos)
    if keys[pygame.K_DOWN]:
        robot_pos = robot_linear_mov(-LIN_SPEED, robot_pos)
    if keys[pygame.K_LEFT]:
        orientation = robot_angular_mov(ANG_SPEED, orientation)
    if keys[pygame.K_RIGHT]:
        orientation = robot_angular_mov(-ANG_SPEED, orientation)

    # Limit the robot position to the screen
    if robot_pos.x > screen.get_width():
        robot_pos.x = screen.get_width()
    if robot_pos.y > screen.get_height():
        robot_pos.y = screen.get_height()
    if robot_pos.x < 0:
        robot_pos.x = 0
    if robot_pos.y < 0:
        robot_pos.y = 0  

    # Draw the robot path
    if show_path and len(path) > 1:
        pygame.draw.lines(screen, "blue", False, path, 2)

    new_robot_surface = pygame.transform.rotate(robot_surface, orientation * 180/math.pi)
    new_robot_rect = new_robot_surface.get_rect()

    # Draw the triangle inside the robot_surface to indicate the orientation
    if draw_triangle:
        robot_image = pygame.draw.polygon(robot_surface, "black", (
            (robot_rect.h/2 - TRIANG_SIZE, robot_rect.w/2 - TRIANG_SIZE),
            (robot_rect.h/2 - TRIANG_SIZE, robot_rect.w/2 + TRIANG_SIZE),
            (robot_rect.h/2 + TRIANG_SIZE, robot_rect.w/2)))


    # Draw the robot
    # pygame.draw.circle(screen, "purple", robot_pos, ROBOT_SIZE)
    new_robot_rect.center = int(robot_pos.x), int(robot_pos.y)
    screen.blit(new_robot_surface, new_robot_rect)

    font = pygame.font.Font(None, 22)
    text_i = font.render("Control the robot with the arrow keys. Press 'C' to center, '9' to rotate 90 degrees, 'P' to print pose, 'S' to show path, 'R' to Reset path, 'T' to draw a triangle.", True, "gray")
    screen.blit(text_i, (25, 10))

    if print_pos:
        # Print the robot position and orientation at the bottom of the screen
        font = pygame.font.Font(None, 24)
        text_p = font.render(f"Robot position: {int(robot_pos.x), int(robot_pos.y)} pixels; orientation: {int(orientation * 180/math.pi)} degrees.", True, "black")
        screen.blit(text_p, (25, screen.get_height() - 20))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    count_frames += 1 # Increment the frame counter

pygame.quit()