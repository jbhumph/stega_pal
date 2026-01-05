from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QSplitter, QSizePolicy
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography Pal")
        self.setMinimumSize(1200, 700)

        # Section Definitions
        self.sections = {
            "image_encode": {
                "title": "Image Encoding",
                "description": "Hide data within image files using various steganography techniques. "
                               "The embedded data becomes invisible to the human eye while remaining "
                               "extractable with the correct decoding parameters.",
                "file_types": ".png, .bmp, .tiff",
                "algorithms": ["LSB"]
            }
        }

        self.current_section = "image_encode"
        self._setup_ui()

    def _setup_ui(self):
        # Setup the main UI layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create each column
        self.nav_column = self._create_nav_column()

        main_layout.addWidget(self.nav_column)


    def _create_nav_column(self):
        # Creates the navigation column to the left
        nav_widget = QWidget()
        nav_widget.setFixedWidth(180)
        nav_widget.setStyleSheet("QWidget {background-color: #2c3e50;} QPushButton {background-color: transparent; color: #cccccc; border: none; text-align: left; font-size: 13px;} QPushButton: hover {background-color: #3d3d3d;} QPushButton: checked {background-color: #0d6efd; color: white;}")

        layout = QVBoxLayout(nav_widget)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(2)

        # Add navigation buttons

        layout.addStretch()
        return nav_widget