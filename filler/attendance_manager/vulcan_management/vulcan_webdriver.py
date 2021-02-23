from selenium.webdriver import Chrome
from filler.attendance_manager.settings.webdriver_settings import WebdriverSettings


class VulcanWebdriver(Chrome):

    def __init__(self):
        self.settings = WebdriverSettings()
        self.settings_dict = self.settings.load_settings()
        executable_path = self.settings_dict['path']
        super().__init__(executable_path)

    def open_vulcan_page(self):
        self.get(self.settings_dict['vulcan_url'])