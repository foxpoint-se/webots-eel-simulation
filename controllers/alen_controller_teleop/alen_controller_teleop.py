"""alen_controller_teleop controller."""

import math
from typing import Literal
from controller import Keyboard, Supervisor, Node, Robot
from controller.field import Field
from general_controller import do_stuff

do_stuff()

MAX_X = 0.05
MAX_Y = 0.5
MAX_VELOCITY = 5
SEA_LEVEL = 0.0

MOTOR_NAME = "motor"

robot = Supervisor()

robot.getDevice("motor").setPosition(float("inf"))


def set_speed(speed_factor: float) -> None:
    new_speed = speed_factor * MAX_VELOCITY
    robot.getDevice("motor").setVelocity(new_speed)


def set_x_turn(factor: float) -> None:
    new_x_turn = factor * MAX_X
    propeller_node = robot.getFromDef("ROBOT.PROPELLER")
    field = propeller_node.getField("shaftAxis")
    old_value = field.getSFVec3f()
    new_value = [old_value[0], new_x_turn, old_value[2]]
    field.setSFVec3f(new_value)


def set_y_turn(factor: float) -> None:
    new_y_turn = factor = MAX_Y
    propeller_node = robot.getFromDef("ROBOT.PROPELLER")
    field = propeller_node.getField("shaftAxis")
    old_value = field.getSFVec3f()
    new_value = [new_y_turn, old_value[1], old_value[2]]
    field.setSFVec3f(new_value)


def get_depth() -> float:
    translation_field = robot.getFromDef("ROBOT").getField("translation")
    translation = translation_field.getSFVec3f()
    # print(translation)
    return -translation[2]


def get_pitch() -> float:
    rotation_field = robot.getFromDef("ROBOT").getField("rotation")
    rotation = rotation_field.getSFRotation()
    pitch_radians = rotation[3]
    pitch_degrees = math.degrees(pitch_radians) - 90
    return pitch_degrees
    # factor = rotation[]
    # return translation[2]


# TODO:
# tror att det vore fördelaktigt att sätta propellern
# på en fiktiv axel liksom. sätt en pinne där bak
# som jag kan kontrollera i förhållande till resten liksom.
# då borde krafterna ge sig därefter


set_speed(1)
set_x_turn(0.0)


# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
keyboard = robot.getKeyboard()
keyboard.enable(100)


class Alen:
    def __init__(self) -> None:
        self.motor_state: Literal["stopped", "forwards", "backwards"] = "stopped"
        self.turn_state: Literal["center", "left", "right"] = "center"
        self.current_pitch = 0.0
        self.current_depth = 0.0
        self.update()
        self.depth_target = 0.0

    def update(self) -> None:
        self.current_pitch = get_pitch()
        self.current_depth = get_depth()

    def go_forward(self) -> None:
        if self.motor_state != "forwards":
            self.motor_state = "forwards"
            print("going forward")
            set_speed(1)

    def stop(self) -> None:
        if self.motor_state != "stopped":
            self.motor_state = "stopped"
            print("stopping")
            set_speed(0)

    def turn_left(self) -> None:
        if self.turn_state != "left":
            self.turn_state = "left"
            print("going left")
            set_x_turn(1.0)

    def turn_right(self) -> None:
        if self.turn_state != "right":
            self.turn_state = "right"
            print("going right")
            set_x_turn(-1.0)

    def center(self) -> None:
        if self.turn_state != "center":
            self.turn_state = "center"
            print("centering")
            set_x_turn(0.0)


set_y_turn(-1)

alen = Alen()

KEY_NUMBER_ZERO = 48
KEY_NUMBER_ONE = 49
KEY_NUMBER_TWO = 50

while robot.step(timestep) != -1:
    alen.update()
    key = keyboard.getKey()
    if key == Keyboard.UP:
        alen.go_forward()
    if key == Keyboard.DOWN:
        alen.stop()
    if key == Keyboard.LEFT:
        alen.turn_left()
    if key == Keyboard.RIGHT:
        alen.turn_right()
    if key == Keyboard.HOME:
        alen.center()

    # print(get_pitch())
    if key == KEY_NUMBER_ZERO:
        print("go to 0 meters")
        print(get_depth())
    if key == KEY_NUMBER_ONE:
        # print("go to 1 meter")
        get_pitch()
    if key == KEY_NUMBER_TWO:
        print("go to 2 meters")

    # print(key)


# Enter here exit cleanup code.
