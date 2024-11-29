from enum import Enum

class NewMemberResponseCodes(Enum):
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
                    return NewMemberResponseCodes.OK
                case "failed":
                    return NewMemberResponseCodes.FAILED
                case _:
                    raise ValueError
        except ValueError:
            raise Exception("New member was not created")