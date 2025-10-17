from enum import Enum

class ProductEnum(Enum):
    CRITICO = 'Crítico'
    NORMAL = 'Normal'
    EXCESSO = 'Excesso'

    @staticmethod
    def from_quantity(saldo: int, min_stock: int, med_stock: int) -> str:
        if saldo <= min_stock:
            return ProductEnum.CRITICO.value
        elif saldo <= med_stock:
            return ProductEnum.NORMAL.value
        else:
            return ProductEnum.EXCESSO.value
