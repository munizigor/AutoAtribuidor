# gestorsei/domain/models.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Servidor:
    matricula: str

    def __str__(self) -> str:
        return self.matricula

@dataclass
class Operador(Servidor):
    setor: str = ""

    def __str__(self) -> str:
        return f"{self.matricula} - {self.setor}"

@dataclass
class Processo:
    processo: str
    descricao: str = ""
    anotacao: str = ""
    tag: str = ""
    link: Optional[str] = None

    def __str__(self) -> str:
        # evita quebrar caso descricao ainda não tenha sido preenchida
        return f"{self.processo} - {self.descricao}".strip(" -")
