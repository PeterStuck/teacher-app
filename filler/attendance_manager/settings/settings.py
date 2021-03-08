import yaml
from wku_django.settings import BASE_DIR


class Settings:
    """ Class only for inherit to other classes """

    def load_settings(self) -> dict:
        pass

    def load_main_settings(self) -> dict:
        with open(BASE_DIR / 'filler/static/filler/files/config/main_config.yaml') as settings:
            settings_paths_dict = yaml.load(settings, Loader=yaml.FullLoader)

        return settings_paths_dict

    def update_settings(self, updated_config: dict):
        pass