# gestorsei/utils/env.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class SeiCredentials:
    usuario: str
    senha: str
    orgao_value: str

def load_sei_credentials(env_path: str | None = None) -> tuple[str | None, str | None, str | None]:
    """
    Lê variáveis SEI_* do .env (se existir).
    Retorna (usuario, senha, orgao_value) podendo vir None.
    """
    load_dotenv(dotenv_path=env_path, override=False)

    usuario = os.getenv("SEI_USUARIO")
    senha = os.getenv("SEI_SENHA")
    orgao_value = os.getenv("SEI_ORGAO_VALUE")

    return usuario, senha, orgao_value
