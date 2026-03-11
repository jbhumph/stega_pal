from typing import Any, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QSpinBox, QGroupBox
)
from PySide6.QtCore import Signal, QEvent

from core.algo_configs import WidgetType, get_algorithm_config, SettingDef
from .widget_factory import WidgetFactory

class EncodingPanel(QWidget):
    # Widget for setting encoding algo options

    algorithm_changed = Signal(str)
    settings_changed = Signal(dict)
    tooltip_hovered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._section_id = None
        self._current_algorithm = None
        self._current_config = None
        self._current_settings = {}
        self._value_getters = {}
        self._widget_tooltips = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Algorithm Selector
        algo_label = QLabel("Algorithm")
        algo_label.setStyleSheet("font-weight: bold; font-size: 13px")
        layout.addWidget(algo_label)

        self.algo_combo = QComboBox()
        self.algo_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #e0e0e0;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #e0e0e0;
                selection-background-color: #0d6efd;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #6d42bd;
                selection-background-color: #6d42bd;
            }
        """)
        self.algo_combo.currentTextChanged.connect(self._on_algorithm_changed)
        layout.addWidget(self.algo_combo)

        self.options_group = QGroupBox("Options")
        self.options_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #e0e0e0;
                border: 1px solid #404040;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        self.options_layout = QVBoxLayout(self.options_group)
        self.options_layout.setSpacing(10)
        layout.addWidget(self.options_group)
        self.options_group.setVisible(False)

    def set_section(self, section_id: str, algorithms: list):
        # Sets available algorithms in selector
        self._section_id = section_id
        self.algo_combo.clear()

        if algorithms:
            self.algo_combo.addItems(algorithms)
            self._current_algorithm = algorithms[0]
            self._rebuild_options()
            self.algo_combo.setVisible(True)
            self.options_group.setVisible(True)
        else:
            self.algo_combo.setVisible(False)
            self.options_group.setVisible(False)

    def _on_algorithm_changed(self, algorithm: str):
        self._current_algorithm = algorithm
        self._rebuild_options()
        self.algorithm_changed.emit(algorithm)

    def _rebuild_options(self):
        # Clear existing options
        self._clear_layout(self.options_layout)
        self._value_getters.clear()

        if not self._current_algorithm or not self._section_id:
            return  
        
        try:
            self._current_config = get_algorithm_config(self._section_id, self._current_algorithm)
        except ValueError as e:
            print(f"Error loading config: {e}")
            self.options_group.setVisible(False)
            return
        
        self.encryption_widget = None
        self.password_widget = None
        self.password_text_label = None
        for setting in self._current_config.settings:
            widget, value_getter, label = WidgetFactory.create_widget(setting)
            self.options_layout.addWidget(label)
            self.options_layout.addWidget(widget)
            self._value_getters[setting.key] = value_getter

            if setting.widget_type == WidgetType.SPINBOX:
                widget.valueChanged.connect(self._emit_settings_changed)
            elif setting.widget_type == WidgetType.COMBOBOX:
                widget.currentTextChanged.connect(self._emit_settings_changed)
            elif setting.widget_type == WidgetType.MULTI_CHECKBOX:
                for cb in widget.findChildren(QCheckBox):
                    cb.stateChanged.connect(self._emit_settings_changed)

            # emit signal if tooltip is hovered
            if setting.tooltip:
                self._widget_tooltips[widget] = setting.tooltip
                widget.installEventFilter(self)


            if setting.key == "password":
                widget.setVisible(False)
                self.password_widget = widget
                label.setVisible(False)
                self.password_text_label = label
            if setting.key == "encryption":
                widget.currentTextChanged.connect(self._on_encryption_changed)


        self.options_layout.addStretch()
        self.options_group.setVisible(True)

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())

    def get_selected_algorithm(self) -> Optional[str]:
        return self._current_algorithm
    
    def get_settings(self) -> dict[str, Any]:
        settings = {}
        for key, getter in self._value_getters.items():
            settings[key] = getter()
        return settings
    
    def set_settings(self, settings: dict[str, Any]) -> None:
        # Set setting values. Implement as needed.
        return 0
    
    def _on_encryption_changed(self, value: str):
        if value != "None":
            if self.password_widget:
                self.password_widget.setVisible(True)
            if self.password_text_label:
                self.password_text_label.setVisible(True)
        else:
            if self.password_widget:
                self.password_widget.setVisible(False)
            if self.password_text_label:
                self.password_text_label.setVisible(False)


    def _emit_settings_changed(self):
        self.settings_changed.emit(self.get_settings())


    def eventFilter(self, watched_object, event):
        if event.type() == QEvent.Type.Enter:
            tooltip_text = self._widget_tooltips.get(watched_object)
            if tooltip_text:
                self.tooltip_hovered.emit(tooltip_text)
            return False
        elif event.type() == QEvent.Type.Leave:
            if watched_object in self._widget_tooltips:
                self.tooltip_hovered.emit("")  # Clear tooltip on leave
            return False
        return super().eventFilter(watched_object, event)