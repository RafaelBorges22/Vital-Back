from enum import Enum

class ProductEnum(Enum):
    BAIXA_QUANTIDADE = "Baixa quantidade"
    MODERADO = "Moderado"
    BOA_QUANTIDADE = "Boa quantidade"

    @staticmethod
    def from_quantity(quantity: int) -> str:
        if quantity <= 5:
            return ProductEnum.BAIXA_QUANTIDADE.value
        elif 6 <= quantity <= 12:
            return ProductEnum.MODERADO.value
        else:
            return ProductEnum.BOA_QUANTIDADE.value