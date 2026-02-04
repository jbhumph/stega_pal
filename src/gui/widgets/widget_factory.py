from PySide6.QtWidgets import QSpinBox, QWidget, QCheckBox, QComboBox, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

from core.algo_configs import SettingDef, WidgetType

class WidgetFactory:
    """Factory for creating settings widgets from metadata"""

    @staticmethod
    def create_widget(setting_def: SettingDef) -> tuple[QWidget, callable]:
        label = QLabel(setting_def.label)
        label.setStyleSheet("font-size: 12px; color: #888888;")

        if setting_def.widget_type == WidgetType.SPINBOX:
            widget = WidgetFactory._create_spinbox(setting_def)
            value_getter = lambda: widget.value()
            return widget, value_getter, label
        elif setting_def.widget_type == WidgetType.CHECKBOX:
            widget = WidgetFactory._create_checkbox(setting_def)
            value_getter = lambda: widget.isChecked()
            return widget, value_getter, label
        elif setting_def.widget_type == WidgetType.SLIDER:
            widget = WidgetFactory._create_slider(setting_def)
            value_getter = lambda: widget.value()
            return widget, value_getter, label
        elif setting_def.widget_type == WidgetType.COMBOBOX:
            widget = WidgetFactory._create_combobox(setting_def)
            value_getter = lambda: widget.currentText()
            return widget, value_getter, label
        elif setting_def.widget_type == WidgetType.MULTI_CHECKBOX:
            widget = WidgetFactory._create_multi_checkbox(setting_def)
            value_getter = lambda: [cb.text() for cb in widget.findChildren(QCheckBox) if cb.isChecked()]
            return widget, value_getter, label
        elif setting_def.widget_type == WidgetType.TEXTBOX:
            widget = WidgetFactory._create_textbox(setting_def)
            value_getter = lambda: widget.text()
            return widget, value_getter, label
        else:
            raise ValueError(f"Unknown widget type: {setting_def.widget_type}")

    @staticmethod
    def _create_spinbox(setting_def: SettingDef) -> QSpinBox:
        spinbox = QSpinBox()
        spinbox.setMinimum(setting_def.min_value or 0)
        spinbox.setMaximum(setting_def.max_value or 100)
        spinbox.setValue(setting_def.default)
        spinbox.setStyleSheet("""
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
        """)
        return spinbox
    
    @staticmethod
    def _create_checkbox(setting_def: SettingDef) -> QCheckBox:
        checkbox = QCheckBox(setting_def.label)
        checkbox.setChecked(setting_def.default)
        return checkbox

    @staticmethod
    def _create_slider(setting_def: SettingDef) -> QWidget:
        slider = QSlider()
        slider.setMinimum(setting_def.min_value or 0)
        slider.setMaximum(setting_def.max_value or 100)
        slider.setValue(setting_def.default)
        return slider

    @staticmethod
    def _create_combobox(setting_def: SettingDef) -> QWidget:
        combobox = QComboBox()
        if setting_def.options:
            combobox.addItems(setting_def.options)
        if setting_def.default in setting_def.options:
            combobox.setCurrentText(setting_def.default)
        combobox.setStyleSheet("""
            QComboBox {   
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
            }
            
        """)
        return combobox

    @staticmethod
    def _create_multi_checkbox(setting_def: SettingDef) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        for option in setting_def.options or []:
            checkbox = QCheckBox(option)
            checkbox.setChecked(option in setting_def.default)
            layout.addWidget(checkbox)
        return container
    
    @staticmethod
    def _create_textbox(setting_def: SettingDef) -> QLineEdit:
        textbox = QLineEdit()
        textbox.setEchoMode(QLineEdit.EchoMode.Password)
        textbox.setText(setting_def.default)
        textbox.setPlaceholderText("Enter password here")
        textbox.setStyleSheet("""
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
        """)
        return textbox