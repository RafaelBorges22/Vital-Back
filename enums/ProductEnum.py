from enum import Enum

class ProductEnum(Enum):
    CRITICO = 'Crítico'
    NORMAL = 'Normal'
    EXCESSO = 'Excesso'

    @staticmethod
    def from_quantity(saldo: int) -> str:
        if saldo <= 5:
            return ProductEnum.CRITICO.value
        elif 6 <= saldo <= 12:
            return ProductEnum.NORMAL.value
        else:
            return ProductEnum.EXCESSO.value