"""# Read google drive contnet"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from src.common import Constants


class Drive:

    def __init__(self):
        self.drive_manage = self.auth_drive()

    def __gdrive_auth(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # client_secrets.json need to be in the same directory as the script
        drive = GoogleDrive(gauth)
        return drive

    def auth_drive(self):
        if self.check_colab():
            return self.__init_dive_colab()
        else:
            return self.__init_drive_local()

    def __init_drive_local(self):
        return self.__gdrive_auth()

    def check_colab(self):
        from IPython import get_ipython
        is_on_colab = 'google.colab' in str(get_ipython())
        return is_on_colab

    def __init_dive_colab(self):
        try:
            from google.colab import drive
            drive.mount(Constants.DRIVE_ROOT_PATH)
            return drive
        except ImportError:
            print('You are running local!!')
