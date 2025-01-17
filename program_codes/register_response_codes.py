from enum import Enum

class RegisterResponseCodes(Enum):
    OK = 1,
    FAILED = 0

    def __str__(self):
        return self.name

    @classmethod
    def string_to_enum(cls, string):
        string_lowercase = string.lower()
        try:
            match string_lowercase:
                case "ok":
                    return RegisterResponseCodes.OK
                case "failed":
                    return RegisterResponseCodes.FAILED
                case _:
                    raise ValueError
        except ValueError:
            raise Exception("No such register code.")