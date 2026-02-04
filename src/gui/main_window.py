from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget, QSplitter, QSizePolicy, QTextEdit, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from gui.widgets.file_picker import FilePicker
from gui.widgets.encoding_panel import EncodingPanel
from core.settings import Settings
from core.encoders import get_encoder
from core.decoders import get_decoder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography Pal")
        self.setMinimumSize(1200, 700)

        # Store original pixmaps for resizing
        self._input_pixmap = None
        self._output_pixmap = None

        # Section Definitions
        self.sections = {
            "image_encode": {
                "title": "Image Encoding",
                "class": "image",
                "description": "Hide data within image files using various steganography techniques. "
                               "The embedded data becomes invisible to the human eye while remaining "
                               "extractable with the correct decoding parameters.",
                "has_preview": True,
                "is_encoding": True,
                "file_types": ".png, .bmp, .tiff",
                "algorithms": ["LSB"]
            },
            "audio_encode": {
                "title": "Audio Encoding",
                "class": "audio",
                "description": "Embed secret data within audio files. Audio steganography exploits "
                               "the limitations of human hearing to hide information in sound files "
                               "without perceptible quality loss.",
                "has_preview": False,
                "is_encoding": True,
                "file_types": ".wav, .flac",
                "algorithms": []
            },
            "video_encode": {
                "title": "Video Encoding",
                "class": "video",
                "description": "Conceal data within video files by utilizing both spatial and temporal "
                               "redundancy. Video steganography offers high capacity due to the large "
                               "amount of data in video frames.",
                "has_preview": False,
                "is_encoding": True,
                "file_types": ".avi, .mkv",
                "algorithms": []
            },
            "batch_encode": {
                "title": "Batch Encoding",
                "class": "batch",
                "description": "Encode data across multiple files simultaneously. This feature allows "
                               "you to split larger payloads across several carrier files for increased "
                               "capacity and security.",
                "has_preview": False,
                "is_encoding": True,
                "file_types": "Multiple",
                "algorithms": []
            },
            "image_decode": {
                "title": "Image Decoding",
                "class": "image",
                "description": "Extract hidden data from steganographic images. Use the same parameters "
                               "that were used during encoding to successfully retrieve the concealed "
                               "information.",
                "has_preview": True,
                "is_encoding": False,
                "file_types": ".png, .bmp, .tiff",
                "algorithms": ["LSB"]
            },
            "audio_decode": {
                "title": "Audio Decoding",
                "class": "audio",
                "description": "Retrieve hidden data from audio files that contain steganographic content. "
                               "The decoding process reverses the encoding algorithm to extract the "
                               "original payload.",
                "has_preview": False,
                "is_encoding": False,
                "file_types": ".wav, .flac",
                "algorithms": []
            },
            "video_decode": {
                "title": "Video Decoding",
                "class": "video",
                "description": "Extract concealed data from video files. Video decoding analyzes frames "
                               "to retrieve the hidden information embedded during the encoding process.",
                "has_preview": False,
                "is_encoding": False,
                "file_types": ".avi, .mkv",
                "algorithms": []
            },
            "batch_decode": {
                "title": "Batch Decoding",
                "class": "batch",
                "description": "Decode data that was split across multiple carrier files. This process "
                               "reassembles the original payload from its distributed steganographic "
                               "containers.",
                "has_preview": False,
                "is_encoding": False,
                "file_types": "Multiple",
                "algorithms": []
            },
            "steganalysis": {
                "title": "Steganalysis",
                "class": "analysis",
                "description": "Analyze files for the presence of hidden data. Steganalysis tools help "
                               "detect steganographic content and evaluate the statistical properties "
                               "of potentially modified files.",
                "has_preview": False,
                "is_encoding": False,
                "file_types": "All supported",
                "algorithms": []
            },
            "settings": {
                "title": "Settings",
                "class": "settings",
                "description": "Configure application preferences, default parameters, and behavior. "
                               "Customize the steganography tools to match your workflow and requirements.",
                "has_preview": False,
                "is_encoding": False,
                "file_types": "",
                "algorithms": []
            },
            "about": {
                "title": "About",
                "class": "about",
                "description": "Steganography App v0.1.0\n\n"
                               "A comprehensive GUI application for hiding and extracting data using "
                               "various steganography techniques across multiple media types including "
                               "images, audio, and video files.",
                "has_preview": False,
                "is_encoding": False,
                "file_types": "",
                "algorithms": []
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

        # Initialize to default section
        self._switch_section("image_encode")


    def _create_nav_column(self):
        # Creates the navigation column to the left
        nav_widget = QWidget()
        nav_widget.setFixedWidth(180)
        nav_widget.setStyleSheet("QWidget {background-color: #2d2d2d;} QPushButton {background-color: transparent; color: #cccccc; border: none; padding: 12px 15px; text-align: left; font-size: 13px;} QPushButton:hover {background-color: #3d3d3d;} QPushButton:checked {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,stop: 0 #3f078c, stop: 1 #553285); color: white; font-weight: bold;}")

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
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, s=section_id: self._switch_section(s))
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

        # Title
        self.section_title = QLabel()
        self.section_title.setStyleSheet("font-size: 24px; font-weight: bold; border: none; background-color: transparent; color: #6d42bd;")
        layout.addWidget(self.section_title)

        # Description
        self.section_description = QLabel()
        self.section_description.setWordWrap(True)
        self.section_description.setStyleSheet("font-size: 14px; color: #aaaaaa; border: none; background-color: transparent;")
        layout.addWidget(self.section_description)

        # Preview Frames Container
        self.preview_container = QWidget()
        self.preview_container.setStyleSheet("border: none;")
        preview_layout = QHBoxLayout(self.preview_container)
        preview_layout.setContentsMargins(0, 10, 0, 0)
        preview_layout.setSpacing(15)

        # Input Preview Frame
        self.input_frame = QFrame()
        self.input_frame.setMinimumHeight(300)
        input_layout = QVBoxLayout(self.input_frame)
        self.input_label = QLabel("Input Preview")
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_label.setStyleSheet("border: none; color: #888888;")
        self.input_image = QLabel()
        self.input_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_image.setStyleSheet("border: none;")
        self.input_image.setText("No image loaded")
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_image, 1)

        # Output Preview Frame
        self.output_frame = QFrame()
        self.output_frame.setMinimumHeight(300)
        output_layout = QVBoxLayout(self.output_frame)
        self.output_label = QLabel("Output Preview")
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_label.setStyleSheet("border: none; color: #888888;")

        # Stacked widget to switch between image and text display
        self.output_stack = QStackedWidget()
        self.output_stack.setStyleSheet("border: none;")

        # Image display (index 0)
        self.output_image = QLabel()
        self.output_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_image.setText("No output yet")
        self.output_stack.addWidget(self.output_image)

        # Text display (index 1)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: transparent; color: #e0e0e0; border: none;")
        self.output_stack.addWidget(self.output_text)

        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_stack, 1)

        # Make both frames equal width
        self.input_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.output_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        preview_layout.addWidget(self.input_frame, 1)
        preview_layout.addWidget(self.output_frame, 1)

        layout.addWidget(self.preview_container)
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

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; margin: 0px; padding: 0px; } QScrollBar:vertical { background-color: #2d2d2d; width: 8px; margin: 0px; } QScrollBar::handle:vertical { background-color: #555555; border-radius: 4px; } QScrollBar::handle:vertical:hover { background-color: #777777; } QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0)
        scroll_layout.setSpacing(15)

        # File Picker
        self.file_picker = FilePicker()
        scroll_layout.addWidget(self.file_picker)

        # Allowed File Types
        self.file_types_label = QLabel()
        self.file_types_label.setStyleSheet("font-size: 12px; color: #888888;")
        scroll_layout.addWidget(self.file_types_label)

        # Payload Picker
        self.payload_picker = FilePicker("Select Payload")
        scroll_layout.addWidget(self.payload_picker)

        # Payload File Types
        self.payload_types_label = QLabel("Allowed types: All Files")
        self.payload_types_label.setStyleSheet("font-size: 12px; color: #888888;")
        scroll_layout.addWidget(self.payload_types_label)

        # Encoding Panel Algo Options
        self.encoding_panel = EncodingPanel()
        scroll_layout.addWidget(self.encoding_panel)
        layout.addStretch()

        scroll_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area, 1)

        # Action button
        self.action_button = QPushButton("Encode")
        self.action_button.setEnabled = False
        layout.addWidget(self.action_button)
        self.action_button.clicked.connect(self._on_action_button_clicked)

        return options_widget
    
    
    def _switch_section(self, section_id):
        # Changes scenes between different options
        self.current_section = section_id
        self.section = self.sections[section_id]
        self.type = ""
        if self.section["is_encoding"]:
            self.type = "encode"
        else:
            self.type = "decode"

        # Update navigation buttons
        for btn, sid in self.nav_button_group:
            btn.setChecked(sid == section_id)

        # Update title and description
        self.section_title.setText(self.section["title"])
        self.section_description.setText(self.section["description"])

        # Show hide preview frames
        self.preview_container.setVisible(self.section["has_preview"])

        # Update output label for preview windows
        if self.section["has_preview"]:
            if self.section["is_encoding"]:
                self.output_label.setText("Encoded Output")
                self.output_image.setText("No output yet")
            else:
                self.output_label.setText("Decoded Data")
                self.output_image.setText("No decoded data yet")

        # Update file types window
        if self.section["file_types"]:
            self.file_types_label.setText(f"Allowed types: {self.section['file_types']}")
            self.file_types_label.setVisible(True)
        else:
            self.file_types_label.setVisible(False)

        # Update encoding panel
        self.encoding_panel.set_section(section_id, self.section["algorithms"])
        self.encoding_panel.setVisible(bool(self.section["algorithms"]))

        # Update file picker visibility
        if section_id == "image_encode":
            print("Image encode selected")
            self.file_picker.setVisible(True)
            self.file_types_label.setVisible(True)
            self.payload_picker.setVisible(True)
            self.payload_types_label.setVisible(True)
        elif section_id == "image_decode":
            self.file_picker.setVisible(True)
            self.file_types_label.setVisible(True)
            self.payload_picker.setVisible(False)
            self.payload_types_label.setVisible(False)
        else:
            self.file_picker.setVisible(False)
            self.file_types_label.setVisible(False)
            self.payload_picker.setVisible(False)
            self.payload_types_label.setVisible(False)

        # Update action button
        if self.section["is_encoding"]:
            self.action_button.setText("Encode")
        else:
            self.action_button.setText("Decode")

        # Hide action button when appropriate
        self.action_button.setVisible(section_id not in ["settings", "about", "steganalysis"])

        # Listen for file picker
        if self.current_section == "image_encode":
            self.file_picker.file_selected.connect(self._load_input_image)

        self.payload_picker.file_selected.connect(self._load_payload_file)

    def _load_input_image(self, file_path):
        # Load image into input preview
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self._input_pixmap = pixmap
            self._update_image_display()
        else:
            self.input_image.setText("Failed to load image")

    def _load_payload_file(self, file_path):
        # Load payload file (for encoding)
        # display txt file content in output preview for now
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            self.output_text.setText(content)
            self.output_stack.setCurrentIndex(1)  # Switch to text view
        except Exception as e:
            self.output_image.setText("Failed to load payload")

    def _update_image_display(self):
        # Update the displayed image to fit current size
        if self._input_pixmap and not self._input_pixmap.isNull():
            scaled_pixmap = self._input_pixmap.scaled(
                self.input_image.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.input_image.setPixmap(scaled_pixmap)

        if self._output_pixmap and not self._output_pixmap.isNull():
            scaled_pixmap = self._output_pixmap.scaled(
                self.output_image.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.output_image.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        # Handle window resize events
        super().resizeEvent(event)
        self._update_image_display()

    def _on_action_button_clicked(self):
        # Handle encode/decode action when button clicked
        f_path = self.file_picker.get_file_path()
        p_path = self.payload_picker.get_file_path()
        o_path = f_path.replace(".png", "_steg.png")
        settings = Settings()
        settings.update_settings(self.encoding_panel.get_settings())
        print(settings.get_all_settings())

        # Select and run encoder/decoder
        if self.type == "encode":
            # Load payload data
            with open(p_path, 'r') as f:
                payload = f.read()

            # Encrypt if enabled
            encoder = get_encoder(self.section["class"], self.encoding_panel.get_selected_algorithm())
            result = encoder.encode(f_path, payload, settings, o_path)
            self.display_output(result, "image")
        else:
            decoder = get_decoder(self.section["class"], self.encoding_panel.get_selected_algorithm())
            result = decoder.decode(f_path, settings)
            print(result)
            self.display_output(result, "text")


    def display_output(self, result, type):
        # Display output of operation
        if type == "image":
            pixmap = QPixmap(result)
            if not pixmap.isNull():
                self._output_pixmap = pixmap
                self._update_image_display()
            else:
                self.output_image.setText("Failed to load image")
            self._output_pixmap = pixmap
            self._update_image_display()
            self.output_stack.setCurrentIndex(0)  # Switch to image view
        else:
            self.output_text.setText(result)
            self.output_stack.setCurrentIndex(1)  # Switch to text view
        
