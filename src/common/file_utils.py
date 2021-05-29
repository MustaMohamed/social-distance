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
