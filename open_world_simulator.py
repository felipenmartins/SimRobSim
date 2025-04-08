import pygame
# from pygame.mixer_music import play
import math
from obstacle_class import RectangularObstacle
from obstacle_class import RectangularGridObstacle
from path_follower_class import PathFollower
from path_planner import Dijkstra
from robot_class import Robot
from button_class import Button 

# pygame setup
pygame.init()
pygame.mouse.set_visible(True)
pygame.display.set_caption("Simple Robot Simulator")
pygame.display.set_icon(pygame.image.load("roomba-top-view-removebg.png"))

running = True  # Exit the program when False

# Create the screen
screen = pygame.display.set_mode((1450, 700)) # width, height
BACKGROUND_COLOR = (220, 220, 220)

# -------------- Buttons --------------
BUTTONS_AREA_SIZE = 150 # Width of the buttons area

# Functions to call when buttons are clicked

# def on_click_quit_b():
#     # Change the global variable running to False to exit the program
#     global running
#     running = False


# Button colors
B_PURPLE = [100, 100, 255]
B_BLUE = [50, 50, 255]
B_PINK = [255, 100, 100]
B_RED = [255, 0, 0]
B_GREEN = [100, 255, 100]

# Create buttons
quit_button = Button(size=(120, 50), clr=B_PINK, cngclr=B_RED, text="Quit", font_size=20)
center_button = Button(size=(120, 50), clr=B_PURPLE, cngclr=B_GREEN, text="Center")
rotate_button = Button(size=(120, 50), clr=B_PURPLE, cngclr=B_GREEN, text="rot. 90°")
reset_button = Button(size=(120, 50), clr=B_PURPLE, cngclr=B_GREEN, text="Reset")
showPath_button = Button(size=(120, 50), clr=B_PURPLE, cngclr=B_GREEN, text="Show path")
followPath_button = Button(size=(120, 50), clr=B_PURPLE, cngclr=B_GREEN, text="Follow path")
waypoints_button = Button(size=(120, 50), clr=B_PURPLE, cngclr=B_GREEN, text="Waypoints")
# --------------------------------------


# Variables
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000  # delta_t = 60 ms 
count_frames = 0 # Count the number of frames
path = tuple() # Store the robot path
collision_counter = 0
TRIANG_SIZE = 15

# Flags
show_next_waypoint = True
show_all_waypoints = True
show_path = True # Show robot path on the screen when True
follow_path = False # Follow the path when True 
print_pos = True # Print the robot pose on the screen when True
draw_triangle = False # Draw a triangle to indicate the orientation of the robot
center_robot = False # Center the robot when True
reset_robot = False # Reset the robot when True
rotate_robot_90 = False # Rotate the robot when True

# settign up the obstacles ----------> To do: Create obstacles in the grid via mouse click
obstacle_obj=RectangularGridObstacle()
obstacle1=RectangularObstacle((0,100),"dark blue",100,100)
obstacle2=RectangularObstacle((0,0),"dark blue",50,500)
obstacle3=RectangularObstacle((800,300),"dark blue",500,100)
obstacle4=RectangularObstacle((800,300),"dark blue",100,300)
obstacle5=RectangularObstacle((800,0),"dark blue",100,200)
obstacle6=RectangularObstacle((200,500),"dark blue",300,100)
obstacle7=RectangularObstacle((200,300),"dark blue",100,300)
obstacles=[obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6, obstacle7]

# Robot variables 
# LIN_SPEED = 100  # pixels per second  -- fixed value for manual control from the keyboard
# ANG_SPEED = 1.58   # radians per second  -- fixed value for manual control from the keyboard
# ROBOT_SIZE = 100    # not in use
robot_start_coords =(50, 550) # Initial robot coordinates in pixels
orientation = 0  # initial robot orientation in radians
robot_goal_coords=(1100, 100)     # Goal coordinates in pixels

# For simulation purposes, the robot position is stored as a Vector2 object
# and the previous robot position is stored as a tuple
robot_pos = pygame.Vector2(robot_start_coords)  # initial robot position
prev_robot_pos = (robot_pos.x, robot_pos.y) # Store the previous robot position

# Create path planning object
start_path = (robot_start_coords[0]//100, robot_start_coords[1]//100)
goal_path = (robot_goal_coords[0]//100, robot_goal_coords[1]//100)
path_planner = Dijkstra(start_path, goal_path,obstacle_obj)
path_planned = path_planner.plan(path_planner.grid, path_planner.costs, path_planner.start, path_planner.goal)
print(f"Path: {path_planned}")
reversed_path = False   # Flag to indicate if the path is reversed

# Get waypoints in pixels (scale to the screen)
waypoints = []
for p in path_planned:
    waypoints.append((p[0]*100 + 50, p[1]*100 + 50))
print(f"Waypoints: {waypoints}")

# Create the path follower object
path_follower = PathFollower(waypoints)

# Create robot object
robot=Robot(dt)
robot.set_pose([robot_start_coords[0], robot_start_coords[1], orientation])
robot.set_speed(lin_speed = robot.MAX_LIN_SPEED/2, ang_speed = robot.MAX_ANG_SPEED/2)

# Create robot surface and rectangle for simulation
robot_surface = pygame.image.load(robot.robot_img).convert_alpha()
robot_rect = robot_surface.get_rect()
robot_rect.center = robot_pos

# Draw the robot
# Make a copy of the robot_surface to rotate it with respect to the original one
new_robot_surface = pygame.transform.rotate(robot_surface, orientation%360)
new_robot_rect = new_robot_surface.get_rect()
new_robot_rect.center = robot_pos

# Print instructions to control the robot and interact with the simulator
print("Welcome to the Simple Robot Simulator!")
print("Use the arrow keys to move the robot or the buttons to control the simulator.")
# print("Press 'c' to move the robot to the Center of the screen.")
# print("Press '9' to rotate the robot by 90 degrees.")
# print("Press 'p' to toggle Printing the robot position.")
# print("Press 's' to toggle Showing the robot path.")
# print("Press 'r' to Reset (clear) the robot path.")
# print("Press 't' to draw a Triangle to indicate the orientation of the robot.")
# print("Press 'f' to Follow the path defined by the waypoints.")
# print("Press 'w' to show the Waypoints on the screen.")
# print("Press 'q' to Quit the program.")


# Main loop

while running:

    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Move robot only if mouse clicked inside the screen
            if event.pos[0] < screen.get_width() - BUTTONS_AREA_SIZE:
                robot.set_pose([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], orientation])
            if quit_button.rect.collidepoint(event.pos):
                running = False
            if center_button.rect.collidepoint(event.pos):
                center_robot = True
            if rotate_button.rect.collidepoint(event.pos):
                rotate_robot_90 = True
            if reset_button.rect.collidepoint(event.pos):
                reset_robot = True
            if showPath_button.rect.collidepoint(event.pos):
                show_path = not show_path
            if followPath_button.rect.collidepoint(event.pos):	
                follow_path = not follow_path
            if waypoints_button.rect.collidepoint(event.pos):
                show_all_waypoints = not show_all_waypoints

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            # Move the robot to the center of the screen and reset its orientation
            if keys[pygame.K_c]:
                center_robot = True
            # Toggle printing of robot position
            if keys[pygame.K_p]:
                print_pos = not print_pos
            # Toggle robot path 
            if keys[pygame.K_s]:
                show_path = not show_path
            # Clear the robot path and achieved waypoints
            if keys[pygame.K_r]:
                reset_robot = True
            # Rotate the robot by 90 degrees
            if keys[pygame.K_9]:
                rotate_robot_90 = True
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
            # Change robot speeds by pressing + and -
            if keys[pygame.K_EQUALS]:
                robot.set_speed(lin_speed=robot.lin_speed+10, ang_speed=robot.ang_speed+0.1)
            if keys[pygame.K_MINUS]:
                robot.set_speed(lin_speed=robot.lin_speed-10, ang_speed=robot.ang_speed-0.1)
            # Quit the program
            if keys[pygame.K_q]:
                running = False
    
    # Test flags and execute corresponding actions
    if center_robot:
        robot.set_pose([screen.get_width() / 2, screen.get_height() / 2, 0])
        center_robot = False

    if reset_robot:
        path = tuple()
        path_follower.next_waypoint = 0 # index of the next waypoint
        robot.set_pose([robot_start_coords[0], robot_start_coords[1], 0])
        robot.set_speed(lin_speed = robot.MAX_LIN_SPEED/2, ang_speed = robot.MAX_ANG_SPEED/2)
        # If path has been reversed, reverse it back
        if reversed_path:
            waypoints.reverse()
            reversed_path = not reversed_path
        reset_robot = False

    if rotate_robot_90:
        robot.set_pose([robot.get_pose()[0], robot.get_pose()[1], robot.get_pose()[2] + math.pi/2])
        rotate_robot_90 = False

    # # Update robot_pos and orientation variables
    robot_pos[0], robot_pos[1], orientation = robot.get_pose()

    # If final waypoint is reached, stop following the path and reverse the waypoints list
    if path_follower.is_at_final_waypoint:
        follow_path = False
        # Reverse waypoints list
        waypoints.reverse()
        reversed_path = not reversed_path
        # Reset the next waypoint index
        path_follower.reset_next_waypoint_index()

    # Draw the screen
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    
    # Draw the center of the grid
    # horizontal_line = pygame.draw.line(screen, "gray", (0, screen.get_height() / 2), (screen.get_width(), screen.get_height() / 2))
    # vertical_line = pygame.draw.line(screen, "gray", (screen.get_width() / 2, 0), (screen.get_width() / 2, screen.get_height()))    

    # Draw a grid of 100x100 pixels
    for i in range(0, screen.get_width(), 100):
        pygame.draw.line(screen, "light gray", (i, 0), (i, screen.get_height()))
    for i in range(0, screen.get_height(), 100):
        pygame.draw.line(screen, "light gray", (0, i), (screen.get_width(), i))

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
        robot_pos[0], robot_pos[1], orientation = robot.move(lin_speed=abs(robot.lin_speed), ang_speed=0)
    if keys[pygame.K_DOWN]:
        robot_pos[0], robot_pos[1], orientation = robot.move(lin_speed=-abs(robot.lin_speed), ang_speed=0)
    if keys[pygame.K_LEFT]:
        robot_pos[0], robot_pos[1], orientation = robot.move(lin_speed=0, ang_speed=abs(robot.ang_speed))
    if keys[pygame.K_RIGHT]:
        robot_pos[0], robot_pos[1], orientation = robot.move(lin_speed=0, ang_speed=-abs(robot.ang_speed))

    # let path follwer change the robot position
    if follow_path:
        # Linear speed is constant; Angular speed depends on the next waypoint
        robot.ang_speed = path_follower.generate_angular_move(robot_pos, orientation)
        robot_pos[0], robot_pos[1], orientation = robot.move()


    # Limit the robot position to the screen
    if robot_pos.x > screen.get_width() - BUTTONS_AREA_SIZE:
        robot.set_pose([screen.get_width() - BUTTONS_AREA_SIZE, robot_pos.y, orientation])
    if robot_pos.y > screen.get_height():
        robot.set_pose([robot_pos.x, screen.get_height(), orientation])
    if robot_pos.x < 0:
        robot.set_pose([0, robot_pos.y, orientation])
    if robot_pos.y < 0:
        robot.set_pose([robot_pos.x, 0, orientation])  


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

    # Draw the obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle.color, obstacle.obs, 0,1)
        # collide = obstacle.obs.colliderect(new_robot_rect)
        collide = obstacle.obs.collidepoint(robot_pos) # Center of the robot
        # Check other points around the robot

        # If collide after moving, move with negative speed of same amplitude
        if collide:
            collision_counter += 1
            print(f"{collision_counter} collisions detected.") 
            # Apply negative speed to return to non-collision state. 
            # *** Does NOT work for collisions in manual mode with negative linear speed! ***
            robot_pos[0], robot_pos[1], orientation = robot.move(lin_speed=-robot.lin_speed, ang_speed=-robot.ang_speed)

    font_size = int(screen.get_height() * 0.03)  # 3% of screen height
    font = pygame.font.Font(None, font_size)

    # instructions = (
    #     "Use the arrow keys. Press 'C' to center, '9' to rotate 90 degrees, 'P' to print pose,"
    #     "'S' to show path, 'R' to Reset path, 'W' to show waypoints, "
    #     "'F' to follow path, 'Q' to quit."
    # )    
    # text_i = font.render(instructions, True, (50, 50, 70))
    # screen.blit(text_i, (25, screen.get_height() - 30))

    if print_pos:
        # Print the robot position and orientation at the bottom of the screen
        text = font.render(f"Robot position: {int(robot_pos.x), int(robot_pos.y)} pixels; orientation: {int(orientation * 180/math.pi)} degrees.", True, (50, 50, 70))
        screen.blit(text, (25, screen.get_height() - 15))
        text = font.render(f"Linear speed: {robot.lin_speed} pixels/s; Angular speed: {int(robot.ang_speed * 180/math.pi)} degrees/s.", True, (50, 50, 70))
        screen.blit(text, (500, screen.get_height() - 15))

    # Draw the buttons area
    pygame.draw.line(screen, "black", (screen.get_width() - BUTTONS_AREA_SIZE, 0), (screen.get_width() - BUTTONS_AREA_SIZE, screen.get_height()))    
    pygame.draw.line(screen, "black", (screen.get_width() - BUTTONS_AREA_SIZE + 2, 0), (screen.get_width() - BUTTONS_AREA_SIZE + 2, screen.get_height()))    

    # Draw buttons
    quit_button.rect.topleft = (screen.get_width() - quit_button.rect.width - 10, screen.get_height() - quit_button.rect.height - 10)
    quit_button.draw(screen)
    center_button.rect.topleft = (screen.get_width() - center_button.rect.width - 10, center_button.rect.height - 40)
    center_button.draw(screen)
    rotate_button.rect.topleft = (screen.get_width() - rotate_button.rect.width - 10, rotate_button.rect.height + 20)
    rotate_button.draw(screen)
    reset_button.rect.topleft = (screen.get_width() - reset_button.rect.width - 10, reset_button.rect.height + 80)
    reset_button.draw(screen)
    showPath_button.rect.topleft = (screen.get_width() - showPath_button.rect.width - 10, showPath_button.rect.height + 140)
    showPath_button.draw(screen)
    followPath_button.rect.topleft = (screen.get_width() - followPath_button.rect.width - 10, followPath_button.rect.height + 200)
    followPath_button.draw(screen)
    waypoints_button.rect.topleft = (screen.get_width() - waypoints_button.rect.width - 10, waypoints_button.rect.height + 260)
    waypoints_button.draw(screen)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(100) / 1000
    count_frames += 1 # Increment the frame counter

    # If the robot is moving, store its position in the path list and update the previous robot position
    if ((int(robot.get_pose()[0]) != prev_robot_pos[0]) or (int(robot.get_pose()[1]) != prev_robot_pos[1])):
        path += ((int(robot.get_pose()[0]), int(robot.get_pose()[1])),)
        prev_robot_pos = (int(robot.get_pose()[0]), int(robot.get_pose()[1]))
        prev_robot_orientation = robot.get_pose()[2]

pygame.quit()