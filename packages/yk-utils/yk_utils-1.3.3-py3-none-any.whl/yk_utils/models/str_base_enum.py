from .base_enum import BaseEnum


class StrBaseEnum(BaseEnum):
    """ StrBaseEnum will allow for the enum-value to be of the same
        value as the key, when using auto()
     """
    def _generate_next_value_(name, start, count, last_values):
        return name
