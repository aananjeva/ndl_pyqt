from enum import Enum

class MagneticLockResponseCodes(Enum):
    OPEN = 1,
    CLOSE = 0

    def __str__(self):
        return self.name

    @classmethod
    def string_to_enum(cls, string):
        string_lowercase = string.lower()
        try:
            match string_lowercase:
                case "open":
                    return MagneticLockResponseCodes.OPEN
                case "close":
                    return MagneticLockResponseCodes.CLOSE
                case _:
                    raise ValueError
        except ValueError:
            raise Exception("The lock is closed")