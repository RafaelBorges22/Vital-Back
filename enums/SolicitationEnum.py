from enum import Enum

class SolicitationEnum(Enum):
    PENDING = "PENDENTE"
    APPROVED = "APROVADO"
    REJECTED = "REJEITADO"

    @staticmethod
    def from_status(status: str) -> str:
        status = status.upper()
        if status == "PENDENTE":
            return SolicitationEnum.PENDING.value
        elif status == "APROVADO":
            return SolicitationEnum.APPROVED.value
        elif status == "REJEITADO":
            return SolicitationEnum.REJECTED.value
        else:
            raise ValueError(f"Status inválido: {status}")