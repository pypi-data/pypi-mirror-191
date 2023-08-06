# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""
Module for storing types that are shared across the mlcvzoo
"""

from nptyping import Int, NDArray, Shape

ImageType = NDArray[Shape["Height, Width, Any"], Int]
