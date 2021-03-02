from .vulcan_webdriver import VulcanWebdriver
from selenium.common.exceptions import NoSuchElementException
from filler.utils.errors.argument_error import InvalidArgumentError
from filler.plain_classes.vulcan_data import VulcanData

from time import sleep


def parse_attendance_dict_to_html_string(presence_dict: dict) -> str:
    """ Returns string data wrapped into HTML tags """
    parsed_data_string = ""
    for name, is_present in presence_dict.items():
        if is_present:
            parsed_data_string += f'<p>{name} <i class="fas fa-check present"></i></p>'
        else:
            parsed_data_string += f'<p>{name} <i class="fas fa-times-circle not-present"></i></p>'

    return parsed_data_string


class VulcanAI:
    """ Class to perform actions on Vulcan Uonet page """

    def __init__(self, credentials: dict):
        self.driver = VulcanWebdriver()
        self.driver.open_vulcan_page()
        self.credentials = (credentials['email'], credentials['password'])

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

    def select_department(self, department: str):
        """ Selects department on main page """
        try:
            self.driver.find_element_by_xpath(f'//span[text()="{department}"]/..').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script("alert('#Error# Problem ze znalezieniem podanego departamentu.');")

    def select_date(self, weekday: str = None):
        """ Selects weekday where attendance should be changed.
         First selects 'niedziela' to avoid default behavior in Vulcan page that sometimes extend lessen list in current weekday. """
        try:
            self.driver.find_element_by_xpath(f'//span[contains(text(), "niedziela")]/../img').click()
            sleep(1)
            self.driver.find_element_by_xpath(f'//span[contains(text(), "{weekday.lower()}")]/../img').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script(f"alert('#Error# Problem z wybraniem {weekday} z rozpiski.');")

    def select_lesson(self, lesson_number: int):
        """ Selects lesson on left side bar """
        if lesson_number <= 0 or lesson_number > 9:
            self.driver.execute_script("alert('#Error# Nie można znaleźć lekcji z poza przedziału 1-9.');")
            raise InvalidArgumentError(message='Lessons are count between 1-9.')

        lesson = str(lesson_number) + '.'
        try:
            self.driver.find_element_by_xpath(f'//span[contains(text(), "{lesson}")]/..').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script("alert('#Error# Problem z wybraniem podanej lekcji.');")
            return -1

    def change_attendance(self, vulcan_data: VulcanData, students_from_csv: set = None):
        """ Whole sequence from entering into attendance correction to place appropriate presency symbol to students """
        self.__enter_attendance_correction()
        students_from_page: list = self.__get_all_students_from_page()
        presence_dict: dict = self.__get_attendance_dict(students_from_page=students_from_page,
                                                         students_from_csv=students_from_csv)
        self.select_start_point_on_attendance_list(lesson=int(vulcan_data.lesson))
        self.set_students_presency(vulcan_data=vulcan_data, presence_dict=presence_dict)
        return presence_dict

    def __enter_attendance_correction(self):
        """ Enters into attendance list edit mode """
        try:
            sleep(0.25)
            self.driver.find_element_by_xpath('//span[contains(text(), "Frekwencja")]/../../..').click()
            sleep(0.5)
            self.driver.find_element_by_xpath('//span[contains(text(), "Zmień frekwencję")]/../..').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script("alert('#Error# Problem z znalezieniem opcji zmiany frekwencji w menu.');")

    def __get_all_students_from_page(self) -> list:
        """ Webscrapes all students existing on current page and converts them to form similar to converted teams
        data """
        participants_objects = self.driver.find_elements_by_xpath(
            '//td[contains(@style, "width: 160px") and string-length(text()) > 5]')
        all_participants = list()
        for participant in participants_objects:
            participant_fullname: str = participant.text
            surname = participant_fullname.split()[0]
            name = participant_fullname.split()[1]

            converted_name = name + " " + surname

            if converted_name in all_participants:
                continue
            all_participants.append(converted_name)

        return all_participants

    def __get_attendance_dict(self, students_from_page, students_from_csv):
        """ Compare two collections and returns a dict, where keys are names and values are bools, depend of presency of student on lesson.
         Student is present if exists on attendance list from Teams. """
        presence_dict = dict()
        for participant in students_from_page:
            if participant in students_from_csv:
                presence_dict[participant] = True
            else:
                presence_dict[participant] = False

        return presence_dict

    def select_start_point_on_attendance_list(self, lesson: int):
        """ Selects first td from top on first student below given lesson """
        lesson_attendance_row = self.driver.find_element_by_xpath(
            '//td[contains(@style, "width: 160px") and string-length(text()) > 5]/..')
        first_student_data_key = lesson_attendance_row.get_attribute('data-key')
        first_student_attendance_log = self.driver.find_elements_by_xpath(f'//tr[@data-key="{first_student_data_key}" and count(./td)=10]')[1]
        first_student_attendance_status = first_student_attendance_log.find_elements_by_css_selector('td')
        first_student_attendance_status[lesson].click()

    def set_students_presency(self, vulcan_data, presence_dict=None):
        if not vulcan_data.file_not_loaded and presence_dict is not None:
            self.__set_presency_based_on_dict(presence_dict=presence_dict, absent_symbol=vulcan_data.absent_symbol)
        else:
            students_from_page: list = self.__get_all_students_from_page()
            self.__set_same_presency_to_all_students(students_from_page=students_from_page, symbol=vulcan_data.absent_symbol)

    def __set_presency_based_on_dict(self, presence_dict: dict, absent_symbol: str):
        """ Sets presency status to studens based on dict which was created based on file from teams. """
        presence_icon = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "●")]')
        absent_icon = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "{absent_symbol}")]')

        for name, is_present in presence_dict.items():
            if is_present:
                presence_icon.click()
            else:
                absent_icon.click()

    def __set_same_presency_to_all_students(self, students_from_page: list, symbol):
        """ Sets same presency status to all students on page """
        presence_icon = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "{symbol}")]')

        for _ in students_from_page:
            presence_icon.click()

    def create_draggable_list(self, presence_dict: dict):
        """ Creates draggable HTML element on top of page that contains list of all students with icons based on
        their presency status. """
        parsed_data = parse_attendance_dict_to_html_string(presence_dict=presence_dict)
        self.driver.execute_script(f"""
            // add fontawesome to page head
            document.querySelector('head').innerHTML += '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css" integrity="sha512-HK5fgLBL+xu6dm/Ii3z4xhlSUyZgTT9tuc/hSrtw6uzJOvgRr2a9jyxxT1ely+B+xFAmJKVSTbpM/CuL7qxO8w==" crossorigin="anonymous" />';

            let body = document.querySelector('body');

            let draggable = document.createElement('div');
            draggable.id = 'draggable_list';
            draggable.innerHTML = `
              <div id="draggable_list_header">Lista obecności <i class="fas fa-times" id="close_attendance_list" onclick="close_attendance_list()"></i></div>
              {parsed_data}`;
            body.appendChild(draggable);

            const head = document.querySelector('head');

            let draggable_styles = document.createElement('style');
            draggable_styles.id = 'draggable_styles';
            draggable_styles.innerHTML += `
                #draggable_list {{
                    position: absolute;
                    z-index: 20000;
                    background-color: #fff;
                    text-align: center;
                    border-color: #CCC;
                    border-radius: 0.375rem 0.25rem;
                    box-shadow: 2px 2px 2px 2px #BBB         
                }}

                #draggable_list_header {{
                    padding: 15px;
                    cursor: move;
                    z-index: 10;
                    background-color: #2196F3;
                    color: #fff;
                    font-weight: bold;
                    font-size: 1.25rem;
                    letter-spacing: 2px;
                    border-radius: .375rem .375rem 0 0;
                }}

                p {{
                    font-weight: bold;
                    padding: 10px;
                    border-bottom: 1px solid #AAA;
                    margin: 0;
                }}

                .not-present {{
                    color: #e40017;
                    font-size: 1.5rem;
                    margin-left: 5px;
                }}

                .present {{
                    color: #54e346;
                    font-size: 1.5rem;
                    margin-left: 5px;
                }}

                #close_attendance_list {{
                    color: #333;
                    cursor: pointer;
                }}
                `;
            head.appendChild(draggable_styles);

            presence_list_script = document.createElement('script');
            presence_list_script.id = 'presence_list_script';
            presence_list_script.innerHTML = `
                function close_attendance_list() {{
                    const attendance_list = document.querySelector('#draggable_list');
                    attendance_list.style.display = 'none';
                }}

                dragElement(document.getElementById("draggable_list"));

                function dragElement(elmnt) {{
                  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
                  if (document.getElementById(elmnt.id + "_header")) {{
                    // if present, the header is where you move the DIV from:
                    document.getElementById(elmnt.id + "_header").onmousedown = dragMouseDown;
                  }} else {{
                    // otherwise, move the DIV from anywhere inside the DIV:
                    elmnt.onmousedown = dragMouseDown;
                  }}

                  function dragMouseDown(e) {{
                    e = e || window.event;
                    e.preventDefault();
                    // get the mouse cursor position at startup:
                    pos3 = e.clientX;
                    pos4 = e.clientY;
                    document.onmouseup = closeDragElement;
                    // call a function whenever the cursor moves:
                    document.onmousemove = elementDrag;
                  }}

                  function elementDrag(e) {{
                    e = e || window.event;
                    e.preventDefault();
                    // calculate the new cursor position:
                    pos1 = pos3 - e.clientX;
                    pos2 = pos4 - e.clientY;
                    pos3 = e.clientX;
                    pos4 = e.clientY;
                    // set the element's new position:
                    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
                  }}

                  function closeDragElement() {{
                    // stop moving when mouse button is released:
                    document.onmouseup = null;
                    document.onmousemove = null;
                  }}
                }}`;

                body.appendChild(presence_list_script);
        """)

