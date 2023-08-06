# Copyright 2022 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""Module to provide a registry for configuration constructors"""

import logging
from typing import Type

from config_builder import BaseConfigClass

from mlcvzoo_base.api.registry import MLCVZooRegistry

logger = logging.getLogger(__name__)


class ConfigRegistry(MLCVZooRegistry[Type[BaseConfigClass]]):

    """
    Class to provide a registry for configuration constructors
    """

    def __init__(self) -> None:
        MLCVZooRegistry.__init__(self)
