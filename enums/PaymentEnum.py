from enum import Enum

class PaymentEnum(Enum):
    DINHEIRO = "DINHEIRO"
    CARD = "CARTÃO"
    PIX = "PIX"
    PRODUTOS = "PRODUTOS"

    @staticmethod
    def from_payment_method(method: str) -> str:
        method = method.lower()
        if method == "Dinheiro" or method == "dinheiro":
            return PaymentEnum.DINHEIRO.value
        elif method == "Cartão" or method == "cartão":
            return PaymentEnum.CARD.value
        elif method == "Pix" or method == "pix":
            return PaymentEnum.PIX.value
        elif method == "Produtos" or method == "produtos":
            return PaymentEnum.PRODUTOS.value
        else:
            raise ValueError(f"Método de pagamento inválido: {method}")