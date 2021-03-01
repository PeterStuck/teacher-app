from filler.utils.errors.argument_error import InvalidArgumentError
from filler.plain_classes.teams_data import TeamsData
from filler.attendance_manager.settings.files_settings import FilesSettings

from wku_django.settings import BASE_DIR

import pandas as pd


class AttendanceDataReader:

    def __init__(self):
        self.settings = FilesSettings()
        self.settings_dict = self.settings.load_settings()

    def convert_teams_file(self, filename):
        """ Reads file downloaded from Teams, get sliced informations and parse to new csv file with correct format """
        file_path = str(BASE_DIR / self.settings_dict["raw_teams_file_path"]) + "\\" + filename
        self.__copy_file_to_archive(original_file_path=file_path, filename=filename)
        with open(f'{file_path}', "r", encoding="utf16") as attendance_data:
            participants = list()
            actions = list()
            dates = list()

            for line in attendance_data.readlines()[1:]:
                line = line.replace("\t", ",")
                splitted_line = line.split(",")

                participant = splitted_line[0]
                action = splitted_line[1]
                date = splitted_line[2]

                participants.append(participant)
                actions.append(action)
                dates.append(date)

        td = TeamsData(participants=participants, actions=actions, dates=dates)
        self.recreate_csv_file(td, filename)

    def __copy_file_to_archive(self, original_file_path, filename):
        """ Copies original file into desktop repository with appropriate unique file name """
        archive_file_path = self.settings_dict["archive_desktop_path"] + "/" + filename
        with open(original_file_path, "r", encoding="utf16") as original_file:
            file_content = original_file.readlines()

        with open(f'{archive_file_path}', "w+") as archive_file:
            for line in file_content:
                archive_file.write(line)

    def recreate_csv_file(self, td: TeamsData, filename: str):
        """ Creates new csv file using data from teams file with better format """
        if td is None:
            raise InvalidArgumentError('Teams dataset are empty!')

        data_dict = {
            "uczestnik": td.participants,
            "akcja": td.actions,
            "data": td.dates
        }

        data = pd.DataFrame(data_dict)
        converted_path = str(BASE_DIR / self.settings_dict['coverted_files_path']) + "/" + filename
        data.to_csv(f'{converted_path}')

    def get_participants(self, filename: str):
        """ Reads lesson participants from recreated file and returns as set of them without duplicates """
        converted_path = str(BASE_DIR / self.settings_dict['coverted_files_path']) + "/" + filename
        attendance_data = pd.read_csv(f'{converted_path}')
        return set(attendance_data.uczestnik.to_list())