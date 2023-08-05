# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""Module for enumerating options of formats"""
from enum import Enum

from mlcvzoo_base.configuration.structs import BaseType


class CSVOutputStringFormats(BaseType):
    BASE = "BASE"
    YOLO = "YOLO"


class MOTChallengeFormats(Enum):
    MOT15 = "mot15"
    MOT1617 = "mot1617"
    MOT20 = "mot20"
