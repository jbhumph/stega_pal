from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
)
from PySide6.QtCore import Signal

class FilePicker(QWidget):
    # Allows user to browse and select files from filesystem

    file_selected = Signal(str)

    def __init__(self, label="Select File", parent=None):
        super().__init__(parent)
        self._file_path = ""
        self._setup_ui(label)

    def _setup_ui(self, label):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        label = QLabel(label)
        label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(label)

        # File Path input
        input_layout = QHBoxLayout()
        input_layout.setSpacing(5)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("No file selected...")
        self.path_input.setReadOnly(True)
        self.path_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
            }
        """)
        input_layout.addWidget(self.path_input)

        self.browse_button = QPushButton("Browse")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: #e0e0e0;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
        self.browse_button.clicked.connect(self._browse_file)
        input_layout.addWidget(self.browse_button)

        layout.addLayout(input_layout)

    def _browse_file(self):
        # Opens file browser
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*.*)"
        )
        if file_path:
            self._file_path = file_path
            self.path_input.setText(file_path)
            self.file_selected.emit(file_path)

    def get_file_path(self):
        # Return the currently selected file path
        return self._file_path

    def set_file_filter(self, filter_string):
        # Set the file filter for the dialog 
        self._file_filter = filter_string

    def clear(self):
        # Clear the selected file
        self._file_path = ""
        self.path_input.clear()