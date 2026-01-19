class Settings():
    def __init__(self, o_type, algo):
        self.encoding_algorithm = "LSB"
        self.error_correction = False
        self.payload_encryption = False
        self.compression = False

        self.settings = {}
        self._setup_defaults(o_type, algo)

    def _setup_defaults(self, o_type, a_type):
        if o_type == "encode":
            if a_type == "image_encode":
                self.settings = {
                    "bit_planes": 1,
                    "color_channels": ["R", "G", "B"],
                    "randomize_positions": False
                }
            elif a_type == "DCT":
                self.settings = {
                    "bit_planes": 1,
                    "color_channels": ["R", "G", "B"],
                    "randomize_positions": False
                }
        elif o_type == "decode":
            # Decoding definitions
            pass

    def update_setting(self, key, value):
        if key in self.settings:
            self.settings[key] = value

    def get_settings(self, key):
        return self.settings.get(key, None)