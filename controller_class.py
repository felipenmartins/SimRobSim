class PIDController:
    def __init__(self,robot):
        self.robot=robot

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

    def pid_controller(self, e, e_prev, e_acc, delta_t, kp=4.0, kd=2.0, ki=0.2):
        """ PID algortithm: must be executed every delta_t seconds
        The error e must be calculated as: e = desired_value - actual_value
        e_prev contains the error calculated in the previous step.
        e_acc contains the integration (accumulation) term.
        """
        # Try the following PID parameters and check the robot behaviour:
        # kp=1.0, kd=0.0, ki=0.0
        # kp=0.0, kd=1.0, ki=0.0
        # kp=0.0, kd=0.0, ki=1.0
        # kp=4.0, kd=0.0, ki=0.0
        # kp=4.0, kd=0.0, ki=0.2
        # kp=4.0, kd=2.0, ki=0.2
    
        P = kp*e                      # Proportional term; kp is the proportional gain
        I = e_acc + ki*e*delta_t      # Intergral term; ki is the integral gain
        D = kd*(e - e_prev)/delta_t   # Derivative term; kd is the derivative gain

        # Limit the integral term to avoid windup
        I = max(-3, min(3, I))  # limit the integral term

        output = P + I + D              # controller output

        # store values for the next iteration
        e_prev = e     # error value in the previous interation (to calculate the derivative term)
        e_acc = I      # accumulated error value (to calculate the integral term)

        return output, e_prev, e_acc
