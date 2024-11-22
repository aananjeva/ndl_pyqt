from enum import Enum

class ListAllMembersResponseCodes(Enum):
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
                    return ListAllMembersResponseCodes.OK
                case "failed":
                    return ListAllMembersResponseCodes.FAILED
                case _:
                    return ValueError
        except ValueError:
            raise Exception("Members cannot be listed")