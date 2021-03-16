from filler.plain_classes.vulcan_data import FillerVulcanData
from filler.attendance_manager.data_readers.attendance_data_reader import AttendanceDataReader
from base.vulcan_management.vulcan_agent import VulcanAgent
from base.utils.spared_time_counter import count_spared_time

from time import sleep


class FillerVulcanRunner:
    """ Main engine to fill students presence on Vulcan Uonet page """

    def __init__(self, vulcan_data: FillerVulcanData, credentials: dict):
        self.vd = vulcan_data
        self.adr = AttendanceDataReader()
        self.filename = ''
        self.vulcan_agent: VulcanAgent = None
        self.is_double_lesson = self.vd.is_double_lesson
        self.credentials = credentials

    @count_spared_time
    def run(self):
        """
        Start point for choose which sequence to run, based on check if file was uploaded and if lesson is double .
        Returns spared time in seconds by decorator.
        """
        self.vulcan_agent = VulcanAgent(self.credentials, vulcan_data=self.vd)
        if self.is_double_lesson and not self.vd.file_not_loaded:
            presence_dict = self.__sequence_double_lesson_with_file()
            self.__show_draggable_attendance_list(presence_dict)
        elif not self.vd.file_not_loaded and not self.is_double_lesson:
            presence_dict = self.__sequence_with_file()
            self.__show_draggable_attendance_list(presence_dict)
        elif self.vd.file_not_loaded and self.is_double_lesson:
            self.__sequence_double_lesson_without_file()
        else:
            self.__sequence_without_file()

    def __sequence_with_file(self):
        """ Whole sequence from login into page to fill up students attendance using uploaded file """
        self.__convert_teams_file()
        self.__go_to_attendance_edit()
        students_from_csv = self.__get_students_from_csv_file()
        presence_dict = self.vulcan_agent.change_attendance(vulcan_data=self.vd, students_from_csv=students_from_csv)
        return presence_dict

    def __sequence_double_lesson_with_file(self):
        """ Sequence to fill up same attendace on given lesson and one lesson after """
        presence_dict = self.__sequence_with_file()
        self.__fill_up_second_lesson(presence_dict=presence_dict)
        return presence_dict

    def __sequence_without_file(self):
        """ Whole sequence from login into page to fill up students same attendance """
        self.__go_to_attendance_edit()
        self.vulcan_agent.change_attendance(vulcan_data=self.vd)

    def __sequence_double_lesson_without_file(self):
        """ Sequence to fill up same attendace to all students on given lesson and one lesson after """
        self.__sequence_without_file()
        self.__fill_up_second_lesson(presence_dict=None)

    def __go_to_attendance_edit(self):
        """ Passes through login, department and lesson selection on given date to attendance edit page """
        self.vulcan_agent.login_into_service()
        sleep(1)
        self.vulcan_agent.select_department()
        sleep(1.5)
        self.vulcan_agent.select_date(weekday=self.vd.day)
        sleep(1)
        self.vulcan_agent.select_lesson(lesson_number=int(self.vd.lesson))
        sleep(1)

    def __convert_teams_file(self):
        self.filename = str(self.vd.date) + '-' + self.vd.department + '-' + self.vd.lesson + '.csv'
        self.adr.convert_teams_file(self.filename)

    def __get_students_from_csv_file(self):
        return self.adr.get_participants(self.filename)

    def __fill_up_second_lesson(self, presence_dict):
        self.vulcan_agent.select_start_point_on_attendance_list(lesson=int(self.vd.lesson) + 1)
        self.vulcan_agent.set_students_presency(vulcan_data=self.vd, presence_dict=presence_dict)

    def __show_draggable_attendance_list(self, presence_dict):
        self.vulcan_agent.create_draggable_list(presence_dict=presence_dict)