from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QSpinBox, QGroupBox
)
from PySide6.QtCore import Signal

class EncodingPanel(QWidget):
    # Widget for setting encoding algo options

    options_changed = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._algorithms = []
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
        options_layout = QVBoxLayout(self.options_group)
        options_layout.setSpacing(10)


    def set_algorithms(self, algorithms):
        return 0
    
    def _on_algorithm_changed(self, algorithms):
        return 0