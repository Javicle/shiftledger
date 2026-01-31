class DatabaseError(Exception):
    """This exception thrown when error on database"""


class UserAlreadyExistsError(DatabaseError): ...


class TaskAlreadyExistsError(DatabaseError): ...


class TasksNotFoundError(DatabaseError): ...


class TelegramError(Exception):
    """This exception thrown when error on telegram"""


class UserNotFound(TelegramError):
    """When user is not found: example forwarded message from telegram channel

    Args:
        TelegramError (_type_): base telegram exception
    """

    ...


class FakeUser(TelegramError):
    """When user is bot

    Args:
        TelegramError (_type_): base telegram exception
    """

    ...


class TextNotFound(TelegramError):
    """When text is not found

    Args:
        TelegramError (_type_): base telegram exception
    """


class MessageNotFound(TelegramError):
    """When message is None or Deleted

    Args:
        TelegramError (_type_): base telegram exception
    """

    ...


class LessonsNotFoundError(DatabaseError):
    """When lessons not found for user error

    Args:
        DatabaseError (_type_): _description_
    """


class OverslappingLessonError(DatabaseError):
    """When lesson time overlap with existing lesson

    Args:
        DatabaseError (_type_): base database exception
    """

    ...


class CheckLimitLessonsError(DatabaseError):
    """When user reached maximum lessons limit

    Args:
        DatabaseError (_type_): base database exception
    """

    ...


class AssignmentNotFoundError(Exception):
    """Raised when assignment is not found"""

    pass


class AssignmentsNotFoundError(Exception):
    """Raised when no assignments are found"""

    pass
