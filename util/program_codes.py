from enum import Enum

class ResetPassword(Enum):
    RESET = 1

    def __str__(self):
        match self:
            case RESET:
                return "reset"





# class Members(Enum):
#     ACTIVE = 1
#     ALL = 0
#
#     def __str__(self):
#         match self:
#             case ACTIVE:
#                 return "list_active"
#             case ALL:
#                 return "list_all"

