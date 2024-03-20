"""4wheel_robot_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

# get the time step of the current world.
# timestep = int(robot.getBasicTimeStep())

TIME_STEP = 64

motor_name = "motor"

def run_robot(robot: Robot) -> None:    
    motor = robot.getDevice(motor_name)
    motor.setPosition(float('inf'))
    motor.setVelocity(10)


if __name__ == "__main__":
    robot = Robot()    
    run_robot(robot)
    
