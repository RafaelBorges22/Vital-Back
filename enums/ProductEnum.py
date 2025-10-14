from enum import Enum

class ProductEnum(Enum):
    CRITICO = 'Crítico'
    NORMAL = 'Normal'
    EXCESSO = 'Excesso'

    @staticmethod
    def from_quantity(quantity: int) -> str:
        if quantity <= 5:
            return ProductEnum.CRITICO.value
        elif 6 <= quantity <= 12:
            return ProductEnum.NORMAL.value
        else:
            return ProductEnum.EXCESSO.value