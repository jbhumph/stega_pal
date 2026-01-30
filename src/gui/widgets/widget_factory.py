from PySide6.QtWidgets import QSpinBox, QWidget

from src.core.algo_configs import SettingDef, WidgetType

def _create_spinbox(parent, options):

    spinbox = QSpinBox(parent)
    spinbox.setMinimum(options.get("min", 0))
    spinbox.setMaximum(options.get("max", 100))
    spinbox.setValue(options.get("default", 0))
    return spinbox

@staticmethod
def create_widget(setting_def: SettingDef) -> tuple[QWidget, callable]:
    """Returns (widget, value_getter)"""
    # Dispatch to appropriate _create_* method based on widget_type
    if setting_def.widget_type == WidgetType.SPINBOX:
        widget = _create_spinbox(None, {
            "min": setting_def.min_value,
            "max": setting_def.max_value,
            "default": setting_def.default
        })
        value_getter = lambda: widget.value()
        return widget, value_getter
    # Add other widget types as needed