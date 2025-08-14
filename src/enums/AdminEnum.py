from enum import Enum

class AdminEnum(Enum):
    MASTER = "Master"
    PLENO = "Pleno"
    JUNIOR = "Junior"

    @staticmethod
    def from_level(level: int) -> str:
        if level == 1:
            return AdminEnum.MASTER.value
        elif level == 2:
            return AdminEnum.PLENO.value
        elif level == 3:
            return AdminEnum.JUNIOR.value
        else: 
            raise ValueError(f"Nível inválido: {level}")

    @staticmethod
    def to_level(name: str) -> int:
        name = name.capitalize()
        if name == AdminEnum.MASTER.value:
            return 1
        elif name == AdminEnum.PLENO.value:
            return 2
        elif name == AdminEnum.JUNIOR.value:
            return 3
        else:
            raise ValueError(f"Nome de level inválido: {name}")
