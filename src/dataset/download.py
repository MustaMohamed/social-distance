from src.common import Constants
import os
import re

from src.dataset.drive import Drive


class DatasetDownloader:
    def __init__(self, drive: Drive = None):
        self.drive = drive

    def get_local_dataset_files_names(self):
        files = os.listdir(Constants.LOCAL_DATASET_PATH)
        files.sort(key=lambda f: int(re.sub('\D', '', f)))
        return [Constants.LOCAL_DATASET_PATH + file for file in files]

    def get_drive_dataset_files_names(self):
        if self.drive.check_colab():
            files = os.listdir(Constants.DRIVE_DATASET_PATH)
            return files
        else:
            files = self.drive.drive_manage.ListFile(
                {'q': "'{}' in parents and trashed=false".format(Constants.DRIVE_DATASET_FOLDER_ID)}).GetList()
            return [file['title'] for file in files]

    def download_dataset_from_drive(self):
        files = self.drive.drive_manage.ListFile(
            {'q': Constants.DRIVE_DATASET_FOLDER_ID + " in parents and trashed=false"}).GetList()
        for file in files:
            print('Title: %s, ID: %s' % (file['title'], file['id']))
            file_name = file['title']
            # Get the folder ID that you want
            file_id = file['id']
            file = self.drive.drive_manage.CreateFile({'id': file_id})
            file.GetContentFile(Constants.LOCAL_DATASET_PATH + file_name)

    def download_file_from_drive(self, file_name):
        if self.drive.check_colab():
            return Constants.DRIVE_DATASET_PATH + file_name
        else:
            files = self.drive.drive_manage.ListFile(
                {'q': "'{}' in parents and trashed=false".format(Constants.DRIVE_DATASET_FOLDER_ID)}).GetList()
            file_id = ''
            for file in files:
                # print('Title: %s, ID: %s' % (file['title'], file['id']))
                # Get the folder ID that you want
                if file['title'] == file_name:
                    file_id = file['id']

            if not os.path.exists(Constants.LOCAL_DATASET_PATH):
                os.mkdir(Constants.LOCAL_DATASET_PATH)

            if not os.path.exists(Constants.LOCAL_DATASET_PATH + file_name):
                file = self.drive.drive_manage.CreateFile({'id': file_id})
                file.GetContentFile(Constants.LOCAL_DATASET_PATH + file_name)

            return Constants.LOCAL_DATASET_PATH + file_name
