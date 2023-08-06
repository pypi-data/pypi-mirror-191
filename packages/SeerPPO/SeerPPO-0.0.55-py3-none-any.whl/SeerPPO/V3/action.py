from typing import Any

import gym.spaces
import numpy as np
from rlgym.utils.action_parsers import ActionParser
from rlgym.utils.gamestates import GameState
from gym.spaces import Discrete


class SeerActionV3(ActionParser):
    def __init__(self):
        super().__init__()
        self._lookup_table = self.make_lookup_table()

    @staticmethod
    def make_lookup_table():
        actions = []
        # Ground
        for throttle in (-1, 0, 1):
            for steer in (-1, 0, 1):
                for boost in (0, 1):
                    for handbrake in (0, 1):
                        if boost == 1 and throttle != 1:
                            continue
                        actions.append([throttle or boost, steer, 0, steer, 0, 0, boost, handbrake])
        # Aerial
        for pitch in (-1, 0, 1):
            for yaw in (-1, 0, 1):
                for roll in (-1, 0, 1):
                    for jump in (0, 1):
                        for boost in (0, 1):
                            if jump == 1 and yaw != 0:  # Only need roll for sideflip
                                continue
                            if pitch == roll == jump == 0:  # Duplicate with ground
                                continue
                            actions.append([boost, yaw, pitch, yaw, roll, jump, boost, 0])
        actions = np.array(actions)
        return actions

    def get_action_space(self) -> gym.spaces.Space:
        return Discrete(len(self._lookup_table))

    def parse_actions(self, actions: Any, state: GameState) -> np.ndarray:
        return self._lookup_table[actions]


if __name__ == '__main__':
    ap = SeerActionV3()
    action_space = ap.get_action_space()
    table = ap.make_lookup_table()

    print(table)

    throttle = 0
    steer = 1
    pitch = 2
    yaw = 3
    roll = 4
    jump = 5
    boost = 6
    handbrake = 7

    jump_mask = np.ones(len(table))
    boost_mask = np.ones(len(table))
    pitch_roll_mask = np.ones(len(table))
    handbrake_mask = np.ones(len(table))

    for i in range(len(ap.make_lookup_table())):

        if table[i][jump]:
            jump_mask[i] = 0

        if table[i][boost]:
            boost_mask[i] = 0

        if table[i][pitch] or table[i][roll]:
            pitch_roll_mask[i] = 0

        if table[i][handbrake]:
            handbrake_mask[i] = 0

    print(np.array2string(jump_mask, separator=","))
    print(np.array2string(boost_mask, separator=","))
    print(np.array2string(pitch_roll_mask, separator=","))
    print(np.array2string(handbrake_mask, separator=","))
