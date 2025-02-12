'''first implementation of the path follower class'''
import pygame
import numpy as np


class PathFollower:
    def __init__(self,way_points=[]):
        self.way_points = way_points   # list of waypoints
        self.next_waypoint = 0 # index of the next waypoint
        self.e_prev = 0 # previsous position error - for the PID controller
        self.e_acc = 0  # accumulated position error - for the PID controller
        self.at_waypoint = False

    def generate_angular_move(self, robot_pos, orientation):
        """ Generates the angular move to reach the next waypoint.
            The robot position is given by robot_pos.
            The waypoint is given by self.way_points[self.next_way_point].
        """
        # Get the next waypoint
        next_waypoint = self.way_points[self.next_waypoint]
        
        # Get the robot pose
        x = robot_pos.x
        y = robot_pos.y
        phi = orientation
        
        # Get the desired position
        xd = next_waypoint[0]
        yd = next_waypoint[1]
        
        # Get the position and orientation errors
        dist_err, phi_err = self.get_pose_error(xd, yd, x, y, phi)
        # print(f"Next waypoint: {next_waypoint}, Robot position: {robot_pos} - dist_err: {dist_err}, phi_err: {phi_err}")
        
        # Check if the robot is at the waypoint
        if dist_err < 20:
            self.at_waypoint = True
            self.update_way_points()
        else:
            self.at_waypoint = False

        # Calculate the angular move
        angular_speed, self.e_prev, self.e_acc = self.pid_controller(phi_err, self.e_prev, self.e_acc, 0.1)

        return angular_speed

    def update_way_points(self):
        if len(self.way_points) > self.next_waypoint + 1:
            self.next_waypoint += 1

    def get_pose_error(self, xd, yd, x, y, phi):
        """ Returns the position and orientation errors. 
            Orientation error is bounded between -pi and +pi radians.
        """
        # Position error:
        x_err = xd - x
        y_err = y - yd  # y axis is inverted in the screen!!!
        dist_err = np.sqrt(x_err**2 + y_err**2)

        # Orientation error
        phi_d = np.arctan2(y_err,x_err)
        phi_err = phi_d - phi

        # Limits the error to (-pi, pi):
        phi_err_correct = np.arctan2(np.sin(phi_err),np.cos(phi_err))

        return dist_err, phi_err_correct

    def pid_controller(self, e, e_prev, e_acc, delta_t, kp=7.0, kd=0, ki=0):
        """ PID algortithm: must be executed every delta_t seconds
        The error e must be calculated as: e = desired_value - actual_value
        e_prev contains the error calculated in the previous step.
        e_acc contains the integration (accumulation) term.
        """
        P = kp*e                      # Proportional term; kp is the proportional gain
        I = e_acc + ki*e*delta_t    # Intergral term; ki is the integral gain
        D = kd*(e - e_prev)/delta_t   # Derivative term; kd is the derivative gain

        output = P + I + D              # controller output

        # store values for the next iteration
        e_prev = e     # error value in the previous interation (to calculate the derivative term)
        e_acc = I      # accumulated error value (to calculate the integral term)

        return output, e_prev, e_acc

