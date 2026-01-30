from PySide6.QtWidgets import QSpinBox, QWidget

from core.algo_configs import SettingDef, WidgetType

class WidgetFactory:
    """Factory for creating settings widgets from metadata"""

    @staticmethod
    def create_widget(setting_def: SettingDef) -> tuple[QWidget, callable]:
        """Returns (widget, value_getter)"""
        # Dispatch to appropriate _create_* method based on widget_type
        if setting_def.widget_type == WidgetType.SPINBOX:
            widget = WidgetFactory._create_spinbox(setting_def)
            value_getter = lambda: widget.value()
            return widget, value_getter
        # Add other widget types as needed
        else:
            raise ValueError(f"Unknown widget type: {setting_def.widget_type}")

    @staticmethod
    def _create_spinbox(setting_def: SettingDef) -> QSpinBox:
        spinbox = QSpinBox()
        spinbox.setMinimum(setting_def.min_value or 0)
        spinbox.setMaximum(setting_def.max_value or 100)
        spinbox.setValue(setting_def.default)
        return spinbox