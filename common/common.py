from enum import Enum


class ROLE(Enum):
    SUPER_ADMIN = "SUPER_ADMIN",
    ADMIN = "ADMIN",
    USER = "USER",
    NO_USER = "NO_USER"


def get_buttons_for_role(role: ROLE, list_button: list) -> list:
    return list(map(lambda a: a[1], filter(lambda e: role in e[0], list_button)))

