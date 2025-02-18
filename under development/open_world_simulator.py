# Example file showing a circle moving on screen
import pygame
from pygame.mixer_music import play
import math
from obstacle_class import RectangularObstacle
from path_follower_class import PathFollower
from path_planner import Dijkstra

# pygame setup
pygame.init()
pygame.mouse.set_visible(True)
pygame.display.set_caption("Simple Robot Simulator")
pygame.display.set_icon(pygame.image.load("roomba-top-view-removebg.png"))

# Create the screen
screen = pygame.display.set_mode((1280, 720)) # width, height
BACKGROUND_COLOR = (220, 220, 220)

# settign up the obstacles
obstacle1=RectangularObstacle((50,100),"black",100,100)
obstacle2=RectangularObstacle((0,0),"black",50,500)
obstacle3=RectangularObstacle((800,300),"black",500,100)
obstacle4=RectangularObstacle((800,300),"black",100,300)
obstacle5=RectangularObstacle((800,0),"black",100,200)
obstacle6=RectangularObstacle((200,500),"black",300,100)
obstacle7=RectangularObstacle((200,300),"black",100,300)
obstacles=[obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6, obstacle7]

# Create Robot
LIN_SPEED = 200  # pixels per second
ANG_SPEED = 2    # radians per second
ROBOT_SIZE = 100    # not in use
# robot_start_coords = (screen.get_width() / 2, screen.get_height() / 2)
robot_start_coords =(1200, 100) # Initial robot coordinates in pixels
robot_goal_coords=(00, 600)     # Goal coordinates in pixels
robot_pos = pygame.Vector2(robot_start_coords)  # initial robot position
orientation = 0  # initial robot orientation in radians
prev_robot_pos = (robot_pos.x, robot_pos.y) # Store the previous robot position
# robot_surface = pygame.Surface((ROBOT_SIZE, ROBOT_SIZE))
robot_surface = pygame.image.load("roomba-top-view-removebg.png").convert_alpha()
robot_rect = robot_surface.get_rect()
robot_rect.center = robot_pos

# Create path planning object
start_path = (robot_start_coords[0]//100, robot_start_coords[1]//100)
goal_path = (robot_goal_coords[0]//100, robot_goal_coords[1]//100)
path_planner = Dijkstra(start_path, goal_path)
path_planned = path_planner.plan(path_planner.grid, path_planner.costs, path_planner.start, path_planner.goal)
print(f"Path: {path_planned}")

# Get waypoints in pixels (scale to the screen)
waypoints = []
for p in path_planned:
    waypoints.append((p[0]*100 + 50, p[1]*100 + 50))
print(f"Waypoints: {waypoints}")

# Create the path follower object
path_follower = PathFollower(waypoints)

# Variables
# waypoints = [(700,300), (400,120), (282, 400), (700, 50), (700, 640)]
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000  # delta_d = 60 ms 
count_frames = 0 # Count the number of frames
path = tuple() # Store the robot path
collision_counter = 0
TRIANG_SIZE = 15

# Flags
follow_path = False
show_next_waypoint = True
show_all_waypoints = True
running = True  # Exit the program when False
print_pos = True # Print the robot pose on the screen when True
show_path = True # Show robot path on the screen when True
draw_triangle = False # Draw a triangle to indicate the orientation of the robot

# Draw the robot
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
print("Press 'f' to Follow the path defined by the waypoints.")
print("Press 'w' to show the Waypoints on the screen.")
print("Press 'q' to Quit the program.")


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
            # Clear the robot path and achieved waypoints
            if keys[pygame.K_r]:
                path = tuple()
                path_follower.next_waypoint = 0 # index of the next waypoint
                robot_pos.x = robot_start_coords[0]  # initial position
                robot_pos.y = robot_start_coords[1]  # initial position
                orientation = 0  # initial orientation in radians
            # Rotate the robot by 90 degrees
            if keys[pygame.K_9]:
                orientation += math.pi/2
                if orientation > math.pi:
                    orientation -= 2 * math.pi
            # Draw a triangle to indicate the orientation of the robot
            if keys[pygame.K_t]:
                draw_triangle = not draw_triangle
            # Follow the path defined by the waypoints
            if keys[pygame.K_f]:
                follow_path = not follow_path
            # Show the waypoints on the screen
            if keys[pygame.K_w]:
                show_all_waypoints = not show_all_waypoints
            # Show Next waypoint
            if keys[pygame.K_n]:
                show_next_waypoint = not show_next_waypoint
            # Quit the program
            if keys[pygame.K_q]:
                running = False

    # If the robot is moving, store its position in the path list and update the previous robot position
    if ((int(robot_pos.x) != prev_robot_pos[0]) or (int(robot_pos.y) != prev_robot_pos[1])):
        path += ((int(robot_pos.x), int(robot_pos.y)),)
        prev_robot_pos = (int(robot_pos.x), int(robot_pos.y))
        prev_robot_orientation = orientation

    # If final waypoint is reached, stop following the path
    if path_follower.is_at_final_waypoint:
        follow_path = False
        path_follower.reset_next_waypoint_index()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    # Draw the grid
    horizontal_line = pygame.draw.line(screen, "gray", (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
    vertical_line = pygame.draw.line(screen, "gray", (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))    

    # Draw the waypoints
    if show_all_waypoints:
        for waypoint in waypoints:
            pygame.draw.circle(screen, "red", waypoint, 5)

    # Draw the next waypoint
    if show_next_waypoint:
        pygame.draw.circle(screen, "blue", waypoints[path_follower.next_waypoint], 5)

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

    # let path follwer change the robot position
    if follow_path:
        # Linear speed is constant
        robot_pos = robot_linear_mov(LIN_SPEED,robot_pos)
        # Orientation depends on the next waypoint
        orientation = robot_angular_mov(path_follower.generate_angular_move(robot_pos, orientation), orientation)

    # Limit the robot position to the screen
    if robot_pos.x > screen.get_width():
        robot_pos.x = screen.get_width()
    if robot_pos.y > screen.get_height():
        robot_pos.y = screen.get_height()
    if robot_pos.x < 0:
        robot_pos.x = 0
    if robot_pos.y < 0:
        robot_pos.y = 0  

    #Draw the obstacle
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle.color, obstacle.obs, 0,1)
        collide = obstacle.obs.colliderect(new_robot_rect)
        if collide:
            collision_counter += 1
            print(f"{collision_counter} collisions detected.") 
            break

    # If collide after moving, restore the previous robot position    
    if collide:
        try:
            robot_pos.x = path[-3][0] # prev_robot_pos[0]
            robot_pos.y = path[-3][1] # prev_robot_pos[1]
            orientation = prev_robot_orientation
        except:
            robot_pos.x = screen.get_width() / 2
            robot_pos.y = screen.get_height() / 2
            orientation = 0

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
    text_i = font.render("Use the arrow keys. Press 'C' to center, '9' to rotate 90 degrees, 'P' to print pose, 'S' to show path, 'R' to Reset path, 'W' to show waypoints, 'F' to follow path, 'Q' to quit.", True, (70, 70, 120))
    screen.blit(text_i, (25, 10))

    if print_pos:
        # Print the robot position and orientation at the bottom of the screen
        font = pygame.font.Font(None, 22)
        text = font.render(f"Robot position: {int(robot_pos.x), int(robot_pos.y)} pixels; orientation: {int(orientation * 180/math.pi)} degrees.", True, (70, 70, 120))
        screen.blit(text, (25, screen.get_height() - 20))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    count_frames += 1 # Increment the frame counter

pygame.quit()