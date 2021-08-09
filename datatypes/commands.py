from dataclasses import dataclass
import math


def map_number(origin, min1, max1, min2, max2):
    return ((origin - min1) / (max1 - min1)) * (max2 - min2) + min2


movement_example = {
    'type': 'command',
    'movement': {
        'throttle': 0,  # -32 ~ 31
        'steer': 0  # -32 ~ 31
    }
}


@dataclass
class Movement:
    throttle: int
    steer: int

    def __init__(self, *data):
        """
        throttle: -32~31
        steer: -32~31

        :param data: (throttle, steer)
        """
        if len(data) == 1 and type(data[0]) is dict:
            assert data[0]['type'] == 'command'
            assert -32 <= data[0]['movement']['throttle'] < 32
            assert -32 <= data[0]['movement']['steer'] < 32

            self.throttle = int(data[0]['movement']['throttle'])
            self.steer = int(data[0]['movement']['steer'])
        elif len(data) == 2:
            assert -32 <= data[0] < 32
            assert -32 <= data[1] < 32
            self.throttle, self.steer = int(data[0]), int(data[1])
        else:
            raise TypeError

    def __iter__(self):
        yield 'type', 'command'
        yield 'movement', {'throttle': self.throttle, 'steer': self.steer}


joystick_example = {
    'type': 'command',
    'joystick': {
        'angle': 0,  # 0 ~ 359
        'strength': 0  # 0 ~ 100
    }
}


@dataclass
class Joystick:
    angle: int
    strength: int

    def __init__(self, *data):
        """
        angle: 0~359
        strength: 0~100

        :param data: (angle, strength)
        """
        if len(data) == 1 and type(data[0]) is dict:
            assert data[0]['type'] == 'command'
            assert 0 <= data[0]['joystick']['angle'] < 360
            assert 0 <= data[0]['joystick']['strength'] <= 100

            self.angle = int(data[0]['joystick']['angle'])
            self.strength = int(data[0]['joystick']['strength'])
        elif len(data) == 2:
            assert 0 <= data[0] < 359
            assert 0 <= data[1] <= 100
            self.angle, self.strength = data
        else:
            raise TypeError

    def __iter__(self):
        yield 'type', 'command'
        yield 'joystick', {'angle': self.angle, 'strength': self.strength}

    def as_movement(self):
        throttle = self.strength * math.sin(math.radians(self.angle))
        steer = self.strength * math.cos(math.radians(self.angle))
        throttle = map_number(throttle, -100, 100, -32, 32)
        steer = map_number(steer, -100, 100, -32, 32)
        return Movement(throttle, steer)
