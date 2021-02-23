from filler.plain_classes.vulcan_data import VulcanData
from filler.attendance_manager.data_readers.attendance_data_reader import AttendanceDataReader
from .vulcan_ai import VulcanAI

from time import sleep


class VulcanAttendanceFiller:
    """ Main engine to fill students presence on Vulcan Uonet page """

    def __init__(self, data: VulcanData, is_double_lesson: bool):
        self.data = data
        self.adr = AttendanceDataReader()
        self.filename = ''
        self.vulcan_agent: VulcanAI = None
        self.is_double_lesson = is_double_lesson

    def start_sequence(self):
        """ Start point for choose which sequence run, based on check if file was uploaded """
        self.vulcan_agent = VulcanAI()
        if self.is_double_lesson and not self.data.file_not_loaded:
            presence_dict = self.__sequence_double_lesson_with_file()
            self.__show_draggable_attendance_list(presence_dict)
        elif not self.data.file_not_loaded and not self.is_double_lesson:
            presence_dict = self.__sequence_with_file()
            self.__show_draggable_attendance_list(presence_dict)
        elif self.data.file_not_loaded and self.is_double_lesson:
            self.__sequence_double_lesson_without_file()
        else:
            self.__sequence_without_file()

    def __sequence_with_file(self):
        """ Whole sequence from login into page to fill up students attendance using uploaded file """
        self.__convert_teams_file()
        self.__go_to_attendance_edit()
        students_from_csv = self.__get_students_from_csv_file()
        presence_dict = self.vulcan_agent.change_attendance(vulcan_data=self.data, students_from_csv=students_from_csv)
        return presence_dict

    def __sequence_double_lesson_with_file(self):
        """ Sequence to fill up same attendace on given lesson and one lesson after """
        presence_dict = self.__sequence_with_file()
        self.__fill_up_second_lesson(presence_dict=presence_dict)
        return presence_dict

    def __sequence_without_file(self):
        """ Whole sequence from login into page to fill up students same attendance """
        self.__go_to_attendance_edit()
        self.vulcan_agent.change_attendance(vulcan_data=self.data)

    def __sequence_double_lesson_without_file(self):
        """ Sequence to fill up same attendace to all students on given lesson and one lesson after """
        self.__sequence_without_file()
        self.__fill_up_second_lesson(presence_dict=None)

    def __go_to_attendance_edit(self):
        """ Passes through login, department and lesson selection on given date to attendance edit page """
        self.vulcan_agent.login_into_service()
        sleep(1)
        self.vulcan_agent.select_department(department=self.data.department)
        sleep(1)
        self.vulcan_agent.select_date(weekday=self.data.day)
        sleep(1)
        self.vulcan_agent.select_lesson(lesson_number=int(self.data.lesson))
        sleep(1)

    def __convert_teams_file(self):
        self.filename = str(self.data.date) + '-' + self.data.department + '-' + self.data.lesson + '.csv'
        self.adr.convert_teams_file(self.filename)

    def __get_students_from_csv_file(self):
        return self.adr.get_participants(self.filename)

    def __fill_up_second_lesson(self, presence_dict):
        self.vulcan_agent.select_start_point_on_attendance_list(lesson=int(self.data.lesson) + 1)
        self.vulcan_agent.set_students_presency(vulcan_data=self.data, presence_dict=presence_dict)

    def __show_draggable_attendance_list(self, presence_dict):
        self.vulcan_agent.create_draggable_list(presence_dict=presence_dict)