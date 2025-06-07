"""alen3_controller_teleop controller."""

from controller import Keyboard, Supervisor
from controller.motor import Motor
from controller.inertial_unit import InertialUnit
from controller.altimeter import Altimeter
from general_controller import GeneralAlenController, WebotsToAlenConnection
from pid_controller import PidController

MAX_X = 0.3
MAX_Y = 0.3
MAX_VELOCITY = 10
SEA_LEVEL = 3.0

MOTOR_NAME = "motor"
IMU_NAME = "inertial unit"

robot = Supervisor()


def get_motor(name: str) -> Motor:
    possible_motor = robot.getDevice(name)
    if isinstance(possible_motor, Motor):
        return possible_motor
    else:
        raise Exception(f"{name=} is not a Motor")


def get_imu(name: str) -> InertialUnit:
    possible_unit = robot.getDevice(name)
    if isinstance(possible_unit, InertialUnit):
        return possible_unit
    raise Exception(f"{name} is not an InertialUnit")


global_motor = get_motor(MOTOR_NAME)
propellerDefPath = "ROBOT.SHAFT_BASE_POSE.PROPELLER_POSE.PROPELLER"
global_propeller_node = robot.getFromDef(propellerDefPath)
global_robot_node = robot.getFromDef("ROBOT")
global_imu = get_imu(IMU_NAME)
# global_altimeter = robot.getDevice("altimeter")
# if isinstance(global_altimeter, Altimeter):
#     global_altimeter = global_altimeter
# else:
#     raise Exception("not an altimeter")


connection = WebotsToAlenConnection(
    motor=global_motor,
    imu=global_imu,
    propeller_node=global_propeller_node,
    robot_node=global_robot_node,
    max_velocity=MAX_VELOCITY,
    max_x_turn=MAX_X,
    max_y_turn=MAX_Y,
    sea_level=SEA_LEVEL,
)


connection.init_motor()
connection.init_imu()

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

# inner_pid_target_angle = PidController(0.0, kP=-25.0, kI=-1.0, kD=-1.0)
inner_pid_target_angle = PidController(0.0, kP=-25.0)
out_pid_rudder_output = PidController(0.0, kP=1 / 30)

# depth_target = None

max_dive_angle = 30.0
max_rudder_output = 1.0


def handle_new_depth_target(depth_target: float) -> None:
    inner_pid_target_angle.update_set_point(depth_target)


def compute_new_target_angle(current_depth: float) -> float:
    pid_angle_output = inner_pid_target_angle.compute(current_depth)

    if abs(pid_angle_output) > max_dive_angle:
        pid_angle_output = (
            max_dive_angle if pid_angle_output > 0 else -1 * max_dive_angle
        )

    return -1 * pid_angle_output


def compute_new_rudder_output(new_target_angle: float, current_pitch: float) -> float:
    out_pid_rudder_output.update_set_point(new_target_angle)
    rudder_output = out_pid_rudder_output.compute(current_pitch)

    if abs(rudder_output) > max_rudder_output:
        rudder_output = (
            max_rudder_output if rudder_output > 0 else -1.0 * max_rudder_output
        )

    return rudder_output


def compute_rudder_angle(current_depth: float, current_pitch: float) -> float:
    angle_pid_output = compute_new_target_angle(current_depth)
    rudder_pid_output = compute_new_rudder_output(angle_pid_output, current_pitch)
    return rudder_pid_output


KEY_NUMBER_ZERO = 48
KEY_NUMBER_ONE = 49
KEY_NUMBER_TWO = 50
KEY_PERIOD = 46

# handle_new_depth_target(1.5)

handle_new_depth_target(2.0)
# print()

# alen.set_y_turn(0.3)
# alen.set_y_turn(1.0)

# global_altimeter.enable(10)

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

    # print("depth", connection.get_depth())
    # print("pitch", connection.get_pitch())
    # connection.get_pitch()
    # print(connection.get_pitch())

    # TODO:
    # se till att allt återställs vid shutdown?
    # skulle initiera allt också?

    # print(get_pitch())
    if key == KEY_NUMBER_ZERO:
        print("go to 0 meters, not implemented")
        # print(get_depth())
    if key == KEY_NUMBER_ONE:
        print("go to 1 meter")
        handle_new_depth_target(1.0)
    if key == KEY_NUMBER_TWO:
        print("go to 2 meters, not implemented")

    new_rudder_angle = compute_rudder_angle(
        connection.get_depth(), connection.get_pitch()
    )

    depth = connection.get_depth()
    # diff = 1.0 - depth

    # TODO: behöver nog plutta i en altitude meter??!
    # print(global_altimeter.getValue())

    print("depth", depth, "error", 2.0 - depth)
    # print("new rudder angle", new_rudder_angle)
    alen.set_y_turn(-new_rudder_angle)

    # print(key)


# Enter here exit cleanup code.
