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
    motor.setVelocity(0)
    
    iterations = 0
    while robot.step(TIME_STEP) != -1:
        if iterations == 20:
            print("startar motor")
            motor.setVelocity(10)            
        
        iterations += 1


if __name__ == "__main__":
    robot = Robot()    
    run_robot(robot)
    


 # immersionProperties [
    # DEF SWIMMING_POOL_IMMERSION_PROPERTIES ImmersionProperties {
      # fluidName "swimming pool"
      # dragForceCoefficients 0.1 0 0
      # dragTorqueCoefficients 0.001 0 0
      # viscousResistanceTorqueCoefficient 0.005
    # }
  # ]
  # boundingObject USE S
  # physics Physics {
    # density 500
    # damping Damping {
      # linear 0.5
      # angular 0.5
    # }
  # }
  
  # salamander
  # dragforceCoeffiecients 1 2 1
  # dragTorqueCoefficients 0 0 0
  # visc.ResistanceForceCoefficient 0
  # visc.ResistanceTorqueCoefficient 5