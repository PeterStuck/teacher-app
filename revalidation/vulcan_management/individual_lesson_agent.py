from base.vulcan_management.vulcan_agent import VulcanAgent
from ..plain_classes.vulcan_data import RevalidationVulcanData
from selenium.common.exceptions import NoSuchElementException

from time import sleep


class IndividualLessonAgent(VulcanAgent):

    def __init__(self, credentials: dict, vulcan_data: RevalidationVulcanData):
        super().__init__(credentials, vulcan_data)

    def go_to_student_invidual_lessons(self):
        self.__select_other_journals()
        sleep(0.5)
        self.__select_revalidation_journal()
        sleep(0.5)
        self.__select_student()
        sleep(0.5)
        self.__go_to_course_of_class()

    def __select_other_journals(self):
        try:
            self.driver.find_element_by_xpath('//span[contains(text(), "Dziennik zajęć innych")]/../../..').click()
        except NoSuchElementException:
            self.driver.execute_script('console.log("Nie mogę znaleźć elementu : Dziennik zajęć innych")')

    def __select_revalidation_journal(self):
        try:
            self.driver.find_element_by_css_selector('#rbbnDziennikZajecRewalidWychowBtn').click()
        except NoSuchElementException:
            self.driver.execute_script('console.log("Nie mogę znaleźć elementu : Dziennik zajęć rewalidacyjnych")')

    def __select_student(self):
        try:
            self.driver.find_element_by_xpath(f'//span[contains(text(), "{self.vd.student.name}")]/..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć ucznia : {self.vd.student.name}")')

    def __go_to_course_of_class(self):
        try:
            self.driver.find_element_by_xpath('//td[contains(text(), "Przebieg zajęć")]/../../..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć elementu: Przebieg zajęć")')

    def add_lesson(self):
        self.__click_add_lesson_btn()
        sleep(0.75)
        self.__fill_up_lesson_data()
        sleep(0.25)
        self.__save_lesson()

    def __click_add_lesson_btn(self):
        try:
            self.driver.find_element_by_css_selector('#addEntry').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Dodaj")')

    def __fill_up_lesson_data(self):
        try:
            date_input = self.driver.find_element_by_css_selector('#dfData-inputEl')
            textareas = self.driver.find_elements_by_xpath('//textarea')
            topic_area = textareas[0]
            comments_area = textareas[1]
            payment_select = self.driver.find_element_by_xpath('//input[contains(@value, "Dodatkowo płatne")]')
            num_of_hours = self.driver.find_element_by_xpath('//input[contains(@name, "LiczbaGodzin")]')

            date_input.clear()
            date_input.send_keys(self.vd.date)
            topic_area.send_keys(self.vd.topic)
            comments_area.send_keys(self.vd.comments)

            payment_select.click()
            self.driver.find_element_by_xpath(f'//li[contains(@class, "x-boundlist-item") and contains(text(), "{self.vd.payment_type}")]').click()

            num_of_hours.send_keys(self.vd.num_of_hours)
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Dodaj lub pól formularza")')

    def __save_lesson(self):
        try:
            self.driver.find_element_by_xpath('//span[contains(text(), "Zapisz")]/../../..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Zapisz")')

    def add_attendance_to_lesson(self):
        sleep(1)
        self.__select_student_attendance()
        sleep(1)
        self.__enter_student_attendance_edit_mode()
        sleep(0.5)
        self.__change_attendance_status()

    def __select_student_attendance(self):
        try:
            self.driver.find_element_by_xpath('//td[contains(text(), "Frekwencja")]/../../..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Frekwencja")')

    def __enter_student_attendance_edit_mode(self):
        try:
            particular_date_element = \
                self.driver.find_element_by_xpath(f'//div[contains(@style, "transform:rotate(-90deg)") and contains(text(), "{self.vd.date}")]/..')
            all_date_elements = \
                self.driver.find_elements_by_xpath('//div[contains(@style, "transform:rotate(-90deg)")]/..')

            attendace_edit_icon_index = all_date_elements.index(particular_date_element)

            particular_attendance_edit_icon = self.driver.find_elements_by_xpath('//div[contains(@class, "editFrekwencja")]')[attendace_edit_icon_index]
            particular_attendance_edit_icon.click()
        except (NoSuchElementException, ValueError):
            self.driver.execute_script(f'console.log("Nie mogę znaleźć odpowiedniej daty")')

    def __change_attendance_status(self):
        try:
            self.driver.find_element_by_xpath('//td[contains(text(), "?")]').click()

            presence_symbol = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "{self.vd.presence_symbol}")]')
            presence_symbol.click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć pola obecności do wypełnienia.")')




