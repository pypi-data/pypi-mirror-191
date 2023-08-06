from enum import Enum, auto
from typing import Any, Dict, NamedTuple, Type

from yolox.exp import Exp as YOLOXBaseExp

from mlcvzoo_yolox.third_party.yolox.exps.yolox_nano import Exp as YOLOXNanoExp


class YOLOXExperiments(Enum):
    NANO = "NANO"
    TINY = "TINY"
    S = "S"
    M = "M"
    L = "L"
    X = "X"


class YOLOXSettingsTuple(NamedTuple):

    constructor: Type[YOLOXBaseExp]
    attribute_dict: Dict[str, Any]


yolox_experiment_settings: Dict[str, YOLOXSettingsTuple] = {
    YOLOXExperiments.NANO.value.upper(): YOLOXSettingsTuple(
        constructor=YOLOXNanoExp, attribute_dict={}  # everything as in default
    ),
    YOLOXExperiments.TINY.value.upper(): YOLOXSettingsTuple(
        constructor=YOLOXBaseExp,
        attribute_dict={
            "depth": 0.33,
            "width": 0.375,
            "input_size": (416, 416),
            "mosaic_scale": (0.5, 1.5),
            "random_size": (10, 20),
            "test_size": (416, 416),
            "enable_mixup": False,
        },
    ),
    YOLOXExperiments.S.value.upper(): YOLOXSettingsTuple(
        constructor=YOLOXBaseExp, attribute_dict={"depth": 0.33, "width": 0.5}
    ),
    YOLOXExperiments.M.value.upper(): YOLOXSettingsTuple(
        constructor=YOLOXBaseExp, attribute_dict={"depth": 0.67, "width": 0.75}
    ),
    YOLOXExperiments.L.value.upper(): YOLOXSettingsTuple(
        constructor=YOLOXBaseExp, attribute_dict={}  # everything as in default
    ),
    YOLOXExperiments.X.value.upper(): YOLOXSettingsTuple(
        constructor=YOLOXBaseExp, attribute_dict={"depth": 1.33, "width": 1.25}
    ),
}
