from enum import Enum

class RoleName(str, Enum):
    admin = "admin"
    alumno = "alumno"
    profesor = "profesor"