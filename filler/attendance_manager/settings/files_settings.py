from .settings import Settings
import yaml


class FilesSettings(Settings):
    """ Stores access to particular data in config file for files """

    def __init__(self):
        super().__init__()

    def load_settings(self) -> dict:
        settings_paths_dict = self.load_main_settings()
        with open(settings_paths_dict['files_config_path']) as files_settings:
            files_settings_dict = yaml.load(files_settings, Loader=yaml.FullLoader)

        return files_settings_dict

    def update_settings(self, updated_config: dict):
        settings_paths_dict = self.load_main_settings()
        with open(settings_paths_dict['files_config_path'], 'w') as files_settings:
            new_data = yaml.dump(updated_config, files_settings)

