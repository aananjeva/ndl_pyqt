from enum import Enum

class LoginResponseCodes(Enum):
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
                    return LoginResponseCodes.OK
                case "failed":
                    return LoginResponseCodes.FAILED
                case _:
                    raise ValueError
        except ValueError:
            raise Exception("No such login code.")