from base.utils.spared_time_counter import count_spared_time
from filler.attendance_manager.data_readers.attendance_data_reader import AttendanceDataReader
from filler.plain_classes.vulcan_data import FillerVulcanData
from .filler_vulcan_agent import FillerVulcanAgent


class FillerVulcanRunner:
    """ Main engine to fill students presence on Vulcan Uonet page """

    def __init__(self, vulcan_data: FillerVulcanData, credentials: dict):
        self.vd = vulcan_data
        self.adr = AttendanceDataReader()
        self.vulcan_agent = FillerVulcanAgent(credentials, vulcan_data=self.vd)

    @count_spared_time
    def run(self):
        """
        Start point for choose which sequence to run, based on check if file was uploaded and if lesson is double .
        Returns spared time in seconds by decorator.
        """
        if self.vd.is_double_lesson and not self.vd.file_not_loaded:
            self.__run_sequence_double_lesson_with_file()
        elif not self.vd.file_not_loaded and not self.vd.is_double_lesson:
            self.__run_sequence_with_file()
        elif self.vd.file_not_loaded and self.vd.is_double_lesson:
            self.__run_sequence_double_lesson_without_file()
        else:
            self.__run_sequence_without_file()

    def __run_sequence_with_file(self):
        """ Whole sequence from login into page to fill up students attendance using uploaded file """
        students_from_csv = self.__get_students_from_teams_file()
        self.vulcan_agent.go_to_lessons_menu()
        self.vulcan_agent.go_to_attendance_correction()
        return self.vulcan_agent.change_attendance(students_from_csv=students_from_csv)

    def __run_sequence_double_lesson_with_file(self):
        """ Sequence to fill up same attendace on given lesson and one lesson after """
        presence_dict = self.__run_sequence_with_file()
        self.vulcan_agent.repeat_for_second_lesson(presence_dict=presence_dict)

    def __run_sequence_without_file(self):
        """ Whole sequence from login into page to fill up students same attendance """
        self.vulcan_agent.go_to_lessons_menu()
        self.vulcan_agent.go_to_attendance_correction()
        self.vulcan_agent.change_attendance()

    def __run_sequence_double_lesson_without_file(self):
        """ Sequence to fill up same attendace to all students on given lesson and one lesson after """
        self.__run_sequence_without_file()
        self.vulcan_agent.repeat_for_second_lesson(presence_dict=None)

    def __get_students_from_teams_file(self):
        self.adr.convert_teams_file(self.vd.filename)
        return self.adr.get_participants(self.vd.filename)