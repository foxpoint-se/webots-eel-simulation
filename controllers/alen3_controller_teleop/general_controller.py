import math
from controller import Node
from controller.motor import Motor
from controller.inertial_unit import InertialUnit
from typing import Callable, Literal


class GeneralAlenController:
    def __init__(
        self,
        set_speed: Callable[[float], None],
        set_x_turn: Callable[[float], None],
        set_y_turn: Callable[[float], None],
        get_depth: Callable[[], float],
        get_pitch: Callable[[], float],
    ) -> None:
        self.motor_state: Literal["stopped", "forwards", "backwards"] = "stopped"
        self.turn_state: Literal["center", "left", "right"] = "center"
        self.set_speed = set_speed
        self.set_x_turn = set_x_turn
        self.set_y_turn = set_y_turn
        self.get_depth = get_depth
        self.get_pitch = get_pitch
        self.current_pitch = 0.0
        self.current_depth = 0.0
        self.update()

    def update(self) -> None:
        self.current_pitch = self.get_pitch()
        self.current_depth = self.get_depth()

    def go_forward(self) -> None:
        if self.motor_state != "forwards":
            self.motor_state = "forwards"
            print("going forward")
            self.set_speed(1)

    def stop(self) -> None:
        if self.motor_state != "stopped":
            self.motor_state = "stopped"
            print("stopping")
            self.set_speed(0)

    def backwards(self) -> None:
        if self.motor_state != "backwards":
            self.motor_state = "backwards"
            print("backing")
            self.set_speed(-1.0)

    def turn_left(self) -> None:
        if self.turn_state != "left":
            self.turn_state = "left"
            print("going left")
            self.set_x_turn(-1.0)

    def turn_right(self) -> None:
        if self.turn_state != "right":
            self.turn_state = "right"
            print("going right")
            self.set_x_turn(1.0)

    def center(self) -> None:
        if self.turn_state != "center":
            self.turn_state = "center"
            print("centering")
            self.set_x_turn(0.0)


class WebotsToAlenConnection:
    def __init__(
        self,
        motor: Motor,
        imu: InertialUnit,
        propeller_node: Node,
        robot_node: Node,
        max_velocity: float,
        max_x_turn: float,
        max_y_turn: float,
        sea_level: float,
    ) -> None:
        self.motor = motor
        self.imu = imu
        self.propeller_node = propeller_node
        self.robot_node = robot_node
        self.max_velocity = max_velocity
        self.max_x_turn = max_x_turn
        self.max_y_turn = max_y_turn
        self.sea_level = sea_level

    def init_motor(self) -> None:
        self.motor.setPosition(float("inf"))
        self.motor.setVelocity(0.0)

    def init_imu(self, sampling_period: int = 10) -> None:
        self.imu.enable(sampling_period)

    def set_speed(self, speed_factor: float) -> None:
        new_speed = speed_factor * self.max_velocity
        self.motor.setVelocity(new_speed)

    def set_x_turn(self, factor: float) -> None:
        new_x_turn = factor * self.max_x_turn
        field = self.propeller_node.getField("shaftAxis")
        old_value = field.getSFVec3f()
        new_value = [old_value[0], new_x_turn, old_value[2]]
        field.setSFVec3f(new_value)

    def set_y_turn(self, factor: float) -> None:
        new_y_turn = factor * self.max_y_turn
        field = self.propeller_node.getField("shaftAxis")
        old_value = field.getSFVec3f()
        new_value = [old_value[0], old_value[1], new_y_turn]
        field.setSFVec3f(new_value)

    def get_depth(self) -> float:
        translation_field = self.robot_node.getField("translation")
        translation = translation_field.getSFVec3f()
        # print("translation", translation)
        current_elevation = translation[2]
        return self.sea_level - current_elevation

    # def get_pitch(self) -> float:
    #     rotation_field = self.robot_node.getField("rotation")
    #     rotation = rotation_field.getSFRotation()
    #     print("rotation", rotation)
    #     pitch_radians = rotation[3]
    #     pitch_degrees = math.degrees(pitch_radians) - 90
    #     return pitch_degrees

    def get_pitch(self) -> float:
        pitch_radians = self.imu.getRollPitchYaw()[1]
        pitch_degrees = math.degrees(pitch_radians)
        return pitch_degrees
