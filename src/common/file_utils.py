import os
from src.common import Constants


class FileUtils:
    FILE_TYPE_IMAGE = 'image'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_NOT_SUPPORTED = 'not_supported'

    @staticmethod
    def get_file_type(file):
        import mimetypes
        mimetypes.init()
        file_type = FileUtils.FILE_TYPE_NOT_SUPPORTED
        mimestart = mimetypes.guess_type(file)[0]
        if mimestart is not None:
            file_type = mimestart.split('/')[0]

        if file_type not in [FileUtils.FILE_TYPE_IMAGE, FileUtils.FILE_TYPE_VIDEO]:
            file_type = FileUtils.FILE_TYPE_NOT_SUPPORTED

        return file_type

    @staticmethod
    def file_name_without_ex(file_path):
        file = os.path.basename(file_path)
        return os.path.splitext(file)[0]

    @staticmethod
    def get_out_image_path(image_path):
        img_name = FileUtils.file_name_without_ex(image_path)
        return Constants.LOCAL_DATASET_PATH + '{}-out.png'.format(img_name)
