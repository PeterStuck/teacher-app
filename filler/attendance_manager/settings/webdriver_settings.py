from .settings import Settings
import yaml


class WebdriverSettings(Settings):
    """ Stores access to particular data in config file for Chrome webdriver """

    def __init__(self):
        super().__init__()

    def load_settings(self) -> dict:
        settings_paths_dict = self.load_main_settings()
        with open(settings_paths_dict['webdriver_config_path']) as webdriver_settings:
            webdriver_settings_dict = yaml.load(webdriver_settings, Loader=yaml.FullLoader)

        return webdriver_settings_dict

    def update_settings(self, updated_config: dict):
        settings_paths_dict = self.load_main_settings()
        with open(settings_paths_dict['webdriver_config_path'], 'w') as webdriver_settings:
            new_data = yaml.dump(updated_config, webdriver_settings)