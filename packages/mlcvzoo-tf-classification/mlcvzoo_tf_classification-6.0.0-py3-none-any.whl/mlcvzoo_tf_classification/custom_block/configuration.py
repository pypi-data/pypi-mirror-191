# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""
This configuration class is for building python objects from the configuration file.
The respective config fields are parsed via the related component from config_builder module.
"""

import related
from attr import define

from mlcvzoo_tf_classification.configuration import Config, TrainConfig
from mlcvzoo_tf_classification.const import OptimizerTypes


@define
class CustomBlockTrainConfig(TrainConfig):
    """
    Here the hyper parameters for training are extracted.
    """

    __related_strict__ = True

    optimizer: str = related.StringField(default=OptimizerTypes.SGD)


@define
class CustomBlockConfig(Config):
    """
    Here the model specific training configuration is extracted and the respective
    detailed config class as listed above is called.
    """

    __related_strict__ = True

    train_config: CustomBlockTrainConfig = related.ChildField(
        cls=CustomBlockTrainConfig
    )
