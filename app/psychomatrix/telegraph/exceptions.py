class TelegraphException(Exception):
    def __init__(self, error):
        if isinstance(error, dict):
            error = f'Response error: {error}'
        super().__init__(error)


class ContentTooBigError(TelegraphException):
    def __init__(self):
        error = "Content too big"
        super().__init__(error)


class ParsingException(Exception):
    ...


class NotAllowedTag(ParsingException):
    ...


class InvalidHTML(ParsingException):
    ...


class RetryAfterError(TelegraphException):
    ...


class FileTypeError(TelegraphException):
    ...


class FileEmptyError(TelegraphException):
    ...


class FileToBigError(TelegraphException):
    ...
