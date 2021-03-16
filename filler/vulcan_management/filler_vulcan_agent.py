from time import sleep

from selenium.common.exceptions import NoSuchElementException

from base.vulcan_management.vulcan_agent import VulcanAgent
from ..plain_classes.vulcan_data import FillerVulcanData
from ..utils.errors.argument_error import InvalidArgumentError


def parse_attendance_dict_to_html_string(presence_dict: dict) -> str:
    """ Returns string data wrapped into HTML tags """
    parsed_data_string = ""
    for name, is_present in presence_dict.items():
        if is_present:
            parsed_data_string += f'<p>{name} <i class="fas fa-check present"></i></p>'
        else:
            parsed_data_string += f'<p>{name} <i class="fas fa-times-circle not-present"></i></p>'

    return parsed_data_string


class FillerVulcanAgent(VulcanAgent):

    def __init__(self, credentials: dict, vulcan_data: FillerVulcanData):
        super().__init__(credentials, vulcan_data)

    def go_to_attendance_correction(self):
        self.__select_date()
        sleep(1)
        self.__select_lesson()
        sleep(1)
        self.__enter_attendance_correction()
        sleep(1)

    def __select_date(self):
        """ Selects weekday where attendance should be changed.
         First selects 'niedziela' to avoid default behavior in Vulcan page that sometimes extend lessen list in current weekday. """
        try:
            self.driver.find_element_by_xpath(f'//span[contains(text(), "niedziela")]/../img').click()
            sleep(1)
            self.driver.find_element_by_xpath(f'//span[contains(text(), "{self.vd.day.lower()}")]/../img').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script(f"console.log('#Error# Problem z wybraniem {self.vd.day} z rozpiski.');")

    def __select_lesson(self):
        """ Selects lesson on left side bar """
        if int(self.vd.lesson) <= 0 or int(self.vd.lesson) > 9:
            self.driver.execute_script("alert('#Error# Nie można znaleźć lekcji z poza przedziału 1-9.');")
            raise InvalidArgumentError(message='Lessons are count between 1-9.')

        lesson = str(self.vd.lesson) + '.'
        try:
            self.driver.find_element_by_xpath(f'//span[contains(text(), "{lesson}")]/..').click()
        except NoSuchElementException as e:
            print(e)
            self.driver.execute_script("console.log('#Error# Problem z wybraniem podanej lekcji.');")
            return -1

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

    def change_attendance(self, students_from_csv: set = None):
        """ Place appropriate presency symbol to students """
        students_from_page: set = self.__get_all_students_from_page()
        if students_from_csv:
            presence_dict: dict = self.__get_attendance_dict(students_from_page=students_from_page,
                                                             students_from_csv=students_from_csv)
            self.__select_start_point_on_attendance_list(int(self.vd.lesson))
            self.__set_students_presency(presence_dict=presence_dict)
            self.create_draggable_list(presence_dict=presence_dict)
            return presence_dict
        self.__select_start_point_on_attendance_list(int(self.vd.lesson))
        self.__set_students_presency(students_from_csv)

    def __get_all_students_from_page(self) -> set:
        """ Webscrapes all students existing on current page and converts them to form similar to converted teams
        data """
        participants_objects = self.driver.find_elements_by_xpath(
            '//td[contains(@style, "width: 160px") and string-length(text()) > 5]')
        all_participants = set()
        for participant in participants_objects:
            participant_fullname: str = participant.get_attribute('data-qtip').strip()
            surname = participant_fullname.split()[0]
            name = participant_fullname.split()[1]

            converted_name = name + " " + surname

            all_participants.add(converted_name)

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

    def __select_start_point_on_attendance_list(self, lesson: int):
        """ Selects first td from top on first student below given lesson """
        lesson_attendance_row = self.driver.find_element_by_xpath(
            '//td[contains(@style, "width: 160px") and string-length(text()) > 5]/..')
        first_student_data_key = lesson_attendance_row.get_attribute('data-key')
        first_student_attendance_log = \
        self.driver.find_elements_by_xpath(f'//tr[@data-key="{first_student_data_key}" and count(./td)=10]')[1]
        first_student_attendance_status = first_student_attendance_log.find_elements_by_css_selector('td')
        first_student_attendance_status[lesson].click()

    def __set_students_presency(self, presence_dict=None):
        if not self.vd.file_not_loaded and presence_dict is not None:
            self.__set_presency_based_on_dict(presence_dict=presence_dict)
        else:
            self.__set_same_presency_to_all_students()

    def __set_presency_based_on_dict(self, presence_dict: dict):
        """ Sets presency status to studens based on dict which was created based on file from teams. """
        presence_icon = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "●")]')
        absent_icon = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "{self.vd.absent_symbol}")]')

        for name, is_present in presence_dict.items():
            if is_present:
                presence_icon.click()
            else:
                absent_icon.click()

    def __set_same_presency_to_all_students(self):
        """ Sets same presency status to all students on page """
        students_from_page: set = self.__get_all_students_from_page()
        presence_icon = self.driver.find_element_by_xpath(
            f'//span[contains(@class, "clickableText") and contains(text(), "{self.vd.absent_symbol}")]')

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
                    box-shadow: 2px 2px 2px 2px #BBB;
                    max-height: 50vh;
                    overflow: hidden scroll;         
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

    def repeat_for_second_lesson(self, presence_dict: dict = None):
        self.__select_start_point_on_attendance_list(lesson=int(self.vd.lesson) + 1)
        self.__set_students_presency(presence_dict=presence_dict)
