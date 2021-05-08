class MdException(Exception):
    pass


class DownloadException(MdException):
    pass


class NoFollowRedirect(DownloadException):
    pass


class InvalidStatusCode(DownloadException):
    pass


class InvalidFileLength(DownloadException):
    pass
