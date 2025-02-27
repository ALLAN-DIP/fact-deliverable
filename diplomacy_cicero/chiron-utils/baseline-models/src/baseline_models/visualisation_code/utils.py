from enum import Enum


class OrderEnum(Enum):
    NO_ORDER = 0
    HOLD_ORDER = 1
    MOVE_ORDER = 2
    SUPPORT_MOVE_ORDER = 3
    SUPPORT_HOLD_ORDER = 4
    CONVOY_ORDER = 5

    BUILD_ORDER = 6
    DISBAND_ORDER = 7
