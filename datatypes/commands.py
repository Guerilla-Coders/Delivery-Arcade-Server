from dataclasses import dataclass
from consts import SoundEffectsConstants
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


sound_effects_example = {
    'type': 'command',
    'sound_effects': {
        'mode': SoundEffectsConstants.DEFAULT_MODE,
        'random': SoundEffectsConstants.DEFAULT_RANDOM,
        'language': SoundEffectsConstants.DEFAULT_LANGUAGE
    }
}


@dataclass
class SoundEffect:
    mode: int
    random: int
    language: int

    def __init__(self, *data):
        """
        mode : 0 ~ FINAL_MODE
        random : 1 ~ FINAL_RANDOM
        language : 0 ~ FINAL_LANGUAGE

        Let the current settings rely on 'random = 1 & language = 0' which are DEFAULT values.

        refer to consts/SoundEffectsConstants for further details.
        """
        if len(data) == 1 and type(data[0]) is dict:
            assert data[0]['type'] == 'sound_effects'
            assert 0 <= data[0]['sound_effects']['mode'] <= SoundEffectsConstants.FINAL_MODE
            assert 1 <= data[0]['sound_effects']['random'] <= SoundEffectsConstants.FINAL_RANDOM
            assert 0 <= data[0]['sound_effects']['language'] <= SoundEffectsConstants.FINAL_LANGUAGE

            self.mode = int(data[0]['sound_effects']['mode'])
            self.random = int(data[0]['sound_effects']['random'])
            self.language = int(data[0]['sound_effects']['language'])

        elif len(data) == 3:
            assert 0 <= data[0] < 5
            assert 1 <= data[1] < 2
            assert 0 <= data[2] < 3
            self.mode, self.random, self.language = data
        else:
            raise TypeError

    def __iter__(self):
        yield 'type', 'command'
        yield 'sound_effects', {'mode': self.mode, 'random': self.random, 'language': self.language}
