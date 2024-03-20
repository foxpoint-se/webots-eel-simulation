"""alen3_controller_teleop controller."""

from controller import Keyboard, Supervisor
from controller.motor import Motor
from general_controller import GeneralAlenController, WebotsToAlenConnection

MAX_X = 0.3
MAX_Y = 0.3
MAX_VELOCITY = 10
SEA_LEVEL = 3.0

MOTOR_NAME = "motor"

robot = Supervisor()


def get_motor(name: str) -> Motor:
    possible_motor = robot.getDevice(name)
    if isinstance(possible_motor, Motor):
        return possible_motor
    else:
        raise Exception(f"{MOTOR_NAME=} is not a motor")


global_motor = get_motor(MOTOR_NAME)
propellerDefPath = "ROBOT.SHAFT_BASE_POSE.PROPELLER_POSE.PROPELLER"
global_propeller_node = robot.getFromDef(propellerDefPath)
global_robot_node = robot.getFromDef("ROBOT")


connection = WebotsToAlenConnection(
    motor=global_motor,
    propeller_node=global_propeller_node,
    robot_node=global_robot_node,
    max_velocity=MAX_VELOCITY,
    max_x_turn=MAX_X,
    max_y_turn=MAX_Y,
)


connection.init_motor()

timestep = int(robot.getBasicTimeStep())
keyboard = robot.getKeyboard()
keyboard.enable(100)

alen = GeneralAlenController(
    get_depth=connection.get_depth,
    get_pitch=connection.get_pitch,
    set_speed=connection.set_speed,
    set_x_turn=connection.set_x_turn,
    set_y_turn=connection.set_y_turn,
)


KEY_NUMBER_ZERO = 48
KEY_NUMBER_ONE = 49
KEY_NUMBER_TWO = 50
KEY_PERIOD = 46

while robot.step(timestep) != -1:
    alen.update()
    key = keyboard.getKey()
    if key == Keyboard.UP:
        alen.go_forward()
    if key == Keyboard.DOWN:
        alen.backwards()
    if key == Keyboard.LEFT:
        alen.turn_left()
    if key == Keyboard.RIGHT:
        alen.turn_right()
    if key == Keyboard.HOME:
        alen.center()
    if key == KEY_PERIOD:
        alen.stop()

    # print(get_pitch())
    # if key == KEY_NUMBER_ZERO:
    #     print("go to 0 meters")
    #     print(get_depth())
    # if key == KEY_NUMBER_ONE:
    #     # print("go to 1 meter")
    #     get_pitch()
    # if key == KEY_NUMBER_TWO:
    #     print("go to 2 meters")

    # print(key)


# Enter here exit cleanup code.
