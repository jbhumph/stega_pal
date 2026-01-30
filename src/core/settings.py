class Settings:
    def __init__(self):
        self.algorithm_settings = {}

    def update_settings(self, settings: dict):
        self.algorithm_settings.update(settings)

    def get_setting(self, key: str, default=None):
        return self.algorithm_settings.get(key, default)
