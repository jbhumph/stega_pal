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
        self.center_column = self._create_center_column()
        self.options_column = self._create_options_column()

        main_layout.addWidget(self.nav_column)
        main_layout.addWidget(self.center_column, 1)
        main_layout.addWidget(self.options_column)


    def _create_nav_column(self):
        # Creates the navigation column to the left
        nav_widget = QWidget()
        nav_widget.setFixedWidth(180)
        nav_widget.setStyleSheet("QWidget {background-color: #2d2d2d;} QPushButton {background-color: transparent; color: #cccccc; border: none; text-align: left; font-size: 13px;} QPushButton: hover {background-color: #3d3d3d;} QPushButton: checked {background-color: #0d6efd; color: white;}")

        layout = QVBoxLayout(nav_widget)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(2)

        # Add navigation buttons
        nav_buttons = [
            ("Image Encoding", "image_encode"),
            ("Audio Encoding", "audio_encode"),
            ("Video Encoding", "video_encode"),
            ("Batch Encoding", "batch_encode"),
            ("Image Decoding", "image_decode"),
            ("Audio Decoding", "audio_decode"),
            ("Video Decoding", "video_decode"),
            ("Batch Decoding", "batch_decode"),
            ("Steganalysis", "steganalysis"),
            ("Settings", "settings"),
            ("About", "about"),
        ]
    
        self.nav_button_group = []
        for label, section_id in nav_buttons:
            btn = QPushButton(label)
            btn.setCheckable = True
            #btn.clicked.connect(lambda checked, s=section_id: self._switch_section(s))
            layout.addWidget(btn)
            self.nav_button_group.append((btn, section_id))

        layout.addStretch()
        return nav_widget
    
    def _create_center_column(self):
        # Creates center column containing main working window
        center_widget = QWidget()
        center_widget.setStyleSheet("QWidget {background-color: #1e1e1e;} QLabel {color: #e0e0e0;} QFrame {background-color: #2d2d2d; border: 1px solid #404040; border-radius:4px;}")
        layout = QVBoxLayout(center_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.section_title = QLabel()
        self.section_title.setStyleSheet("font-size: 24px; font-weight: bold; border: none;")
        layout.addWidget(self.section_title)

        self.section_description = QLabel()
        self.section_description.setWordWrap(True)
        self.section_description.setStyleSheet("font-size: 14px; color: #aaaaaa; border: none;")
        layout.addWidget(self.section_description)

        layout.addStretch()

        return center_widget
    
    def _create_options_column(self):
        # Creates right column for selecting options
        options_widget = QWidget()
        options_widget.setFixedWidth(280)
        options_widget.setStyleSheet("QWidget {background-color: #252525;} QLabel {color: #e0e0e0;} QPushButton {background-color: #0d6efd; color: white; border: none; padding: 10px 20px; border-radius: 4px; font-size: 14px;} QpushButton: hover {background-color: #0b5ed7;} QPushButton:disabled {background-color: #555555; color: #888888}")

        layout= QVBoxLayout(options_widget)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)

        layout.addStretch()

        # Action button
        self.action_button = QPushButton("Encode")
        self.action_button.setEnabled = False
        layout.addWidget(self.action_button)

        return options_widget