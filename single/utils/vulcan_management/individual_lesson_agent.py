from base.vulcan_management.vulcan_agent import VulcanAgent
from single.plain_classes.vulcan_data import VulcanIndividualLessonData
from selenium.common.exceptions import NoSuchElementException

from time import sleep


class IndividualLessonAgent(VulcanAgent):

    def __init__(self, credentials: dict):
        super().__init__(credentials)

    def go_to_student_invidual_lessons(self, student_name: str):
        self.__select_other_journals()
        self.__select_revalidation_journal()
        sleep(0.5)
        self.__select_student(name=student_name)
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

    def __select_student(self, name: str):
        try:
            self.driver.find_element_by_xpath('//span[contains(text(), "Tomek")]/..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć ucznia : {name}")')

    def __go_to_course_of_class(self):
        try:
            self.driver.find_element_by_xpath('//td[contains(text(), "Przebieg zajęć")]/../../..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć elementu: Przebieg zajęć")')

    def add_lesson(self, data: VulcanIndividualLessonData):
        self.__click_add_lesson_btn()
        sleep(0.5)
        self.__fill_up_lesson_data(data)
        # self.__save_lesson()

    def __click_add_lesson_btn(self):
        try:
            self.driver.find_element_by_css_selector('#addEntry').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Dodaj")')

    def __fill_up_lesson_data(self, data: VulcanIndividualLessonData):
        try:
            date_input = self.driver.find_element_by_css_selector('#dfData-inputEl')
            textareas = self.driver.find_elements_by_xpath('//textarea')
            topic_area = textareas[0]
            comments_area = textareas[1]
            payment_select = self.driver.find_element_by_xpath('//input[contains(@value, "Dodatkowo płatne")]')
            num_of_hours = self.driver.find_element_by_xpath('//input[contains(@name, "LiczbaGodzin")]')

            # here to fill up date
            topic_area.send_keys(data.topic)
            comments_area.send_keys(data.comments)

            payment_select.click()
            self.driver.find_element_by_xpath(f'//li[contains(@class, "x-boundlist-item") and contains(text(), "{data.payment_type}")]').click()

            num_of_hours.send_keys(data.num_of_hours)
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Dodaj")')

    def __save_lesson(self):
        try:
            self.driver.find_element_by_xpath('//span[contains(text(), "Zapisz")]/../../..').click()
        except NoSuchElementException:
            self.driver.execute_script(f'console.log("Nie mogę znaleźć przycisku: Zapisz")')

    def add_attendance_to_lesson(self):
        self.__select_student_attendance()
        self.__enter_student_attendance_edit_mode()
        self.__change_attendance_status()

    def __select_student_attendance(self):
        pass

    def __enter_student_attendance_edit_mode(self):
        pass

    def __change_attendance_status(self):
        pass




