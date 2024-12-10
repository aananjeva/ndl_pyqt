from dataclasses import dataclass


@dataclass
class Member:
    name: str
    images_path: str
    authorization: str
    access_remaining_date_time: str
