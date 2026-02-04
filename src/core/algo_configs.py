from dataclasses import dataclass
from typing import List, Any
from enum import Enum

class WidgetType(Enum):
    SPINBOX = "spinbox"
    CHECKBOX = "checkbox"
    SLIDER = "slider"
    COMBOBOX = "combobox"
    MULTI_CHECKBOX = "multi_checkbox"
    TEXTBOX = "textbox"

@dataclass
class SettingDef:
    key: str
    label: str
    widget_type: WidgetType
    default: Any
    min_value: int = None
    max_value: int = None
    options: List[str] = None
    tooltip: str = None

@dataclass
class AlgorithmConfig:
    name: str
    display_name: str
    media_type: str
    settings: List[SettingDef]
    description: str = ""

LSB_IMAGE_ENCODE = AlgorithmConfig(
    name="LSB",
    display_name="Least Significant Bit",
    media_type="image",
    settings=[
        SettingDef(
            key="delimiter",
            label="Delimiter",
            widget_type=WidgetType.COMBOBOX,
            default="NULL",
            options=["NULL Terminator", "Magic Sequence", "None"],
            tooltip="Type of delimiter to use for the payload."
        ),
        SettingDef(
            key="bit_planes",
            label="Bit Planes",
            widget_type=WidgetType.SPINBOX,
            default=1,
            min_value=1,
            max_value=4,
            tooltip="Number of least significant bit planes to use for encoding."
        ),
        SettingDef(
            key="color_channels",
            label="Color Channels",
            widget_type=WidgetType.MULTI_CHECKBOX,
            default=["R", "G", "B"],
            options=["R", "G", "B"],
            tooltip="Color channels to use for encoding."
        ),
        SettingDef(
            key="encryption",
            label="Encryption",
            widget_type=WidgetType.COMBOBOX,
            default="None",
            options=["None", "AES"],
            tooltip="Encrypt the payload before encoding."
        ),
        SettingDef(
            key="password",
            label="Password",
            widget_type=WidgetType.TEXTBOX,
            default="",
            tooltip="Password for encryption (if applicable)."
        ),
    ],
    description="Least Significant Bit encoding for images."
)

LSB_IMAGE_DECODE = AlgorithmConfig(
    name="LSB",
    display_name="Least Significant Bit",
    media_type="image",
    settings=[
        SettingDef(
            key="delimiter",
            label="Delimiter",
            widget_type=WidgetType.COMBOBOX,
            default="NULL",
            options=["NULL Terminator", "Magic Sequence", "None"],
            tooltip="Type of delimiter to use for the payload."
        ),
        SettingDef(
            key="bit_planes",
            label="Bit Planes",
            widget_type=WidgetType.SPINBOX,
            default=1,
            min_value=1,
            max_value=4,
            tooltip="Number of least significant bit planes to read for decoding."
        ),
        SettingDef(
            key="color_channels",
            label="Color Channels",
            widget_type=WidgetType.MULTI_CHECKBOX,
            default=["R", "G", "B"],
            options=["R", "G", "B"],
            tooltip="Color channels to read for decoding."
        ),
        SettingDef(
            key="encryption",
            label="Encryption",
            widget_type=WidgetType.COMBOBOX,
            default="None",
            options=["None", "AES"],
            tooltip="Encrypt the payload before encoding."
        ),
        SettingDef(
            key="password",
            label="Password",
            widget_type=WidgetType.TEXTBOX,
            default="",
            tooltip="Password for encryption (if applicable)."
        ),
    ],
)

ALGORITHM_REGISTRY = {
    ("image_encode", "LSB"): LSB_IMAGE_ENCODE,
    ("image_decode", "LSB"): LSB_IMAGE_DECODE,
}

def get_algorithm_config(section_id: str, algorithm_name: str) -> AlgorithmConfig:
    key = (section_id, algorithm_name)
    config = ALGORITHM_REGISTRY.get(key)
    if not config:
        raise ValueError(f"Algorithm configuration for {section_id} and {algorithm_name} not found.")
    return config