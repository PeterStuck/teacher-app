from time import sleep

from selenium.common.exceptions import NoSuchElementException

from .vulcan_webdriver import VulcanWebdriver


class VulcanAgent:
    """ Class to perform actions on Vulcan Uonet page """

    def __init__(self, credentials: dict, vulcan_data = None):
        self.driver = VulcanWebdriver()
        self.driver.open_vulcan_page()
        self.credentials = (credentials['email'], credentials['password'])
        self.vd = vulcan_data

    def go_to_lessons_menu(self):
        self.login_into_service()
        sleep(1)
        self.__select_department()
        sleep(1.5)

    def login_into_service(self):
        """ Login into Vulcan Uonet with passed credentials """
        try:
            self.driver.find_element_by_css_selector(".loginButton").click()
            self.__send_credentials()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script("alert('#Error# Nie udało się znaleźć przycisku logowania.');")

    def __send_credentials(self):
        """ Pastes login data into fields on page and submit them """
        try:
            email_input = self.driver.find_element_by_css_selector("#LoginName")
            email_input.send_keys(self.credentials[0])

            pass_input = self.driver.find_element_by_css_selector("#Password")
            pass_input.send_keys(self.credentials[1])

            login_submit_btn = self.driver.find_element_by_xpath('//input[@value="Zaloguj się >"]')
            login_submit_btn.click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script(
                "alert('#Error# Problem ze znalezieniem elementów lub wprowadzeniem danych do zalogowania.');")

    def __select_department(self):
        """ Selects department on main page """
        try:
            self.driver.find_element_by_xpath(f'//span[text()="{self.vd.departments}"]/..').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script("alert('#Error# Problem ze znalezieniem podanego departamentu.');")

