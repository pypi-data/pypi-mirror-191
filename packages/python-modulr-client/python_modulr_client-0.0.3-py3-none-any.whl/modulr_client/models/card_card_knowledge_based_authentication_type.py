from enum import Enum


class CardCardKnowledgeBasedAuthenticationType(str, Enum):
    CITY_PARENTS_MET = "CITY_PARENTS_MET"
    FAVOURITE_CHILDHOOD_FRIEND = "FAVOURITE_CHILDHOOD_FRIEND"
    FIRST_PET_NAME = "FIRST_PET_NAME"
    FIRST_CAR = "FIRST_CAR"
    MATERNAL_GRANDMOTHER_MAIDEN_NAME = "MATERNAL_GRANDMOTHER_MAIDEN_NAME"

    def __str__(self) -> str:
        return str(self.value)
