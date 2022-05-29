class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class MissingOption(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, option=None):
        default_msg = "Failed to find option "
        if option is None:
            option = default_msg
        super().__init__(default_msg + "'" + option + "'")


class WrongOptionType(Error):
    def __init__(self, option, typeid):
        super().__init__("Expecting option '" + option + "' with type " + str(typeid))
