# gestorsei/utils/strings.py
import re
import unicodedata

def limpa_parenteses(x: str) -> str:
    # retorna o conteúdo entre parênteses
    if not isinstance(x, str) or "(" not in x or ")" not in x:
        return ""
    return x[x.find("(") + 1 : x.rfind(")")]

def limpa_str(palavra: str | None) -> str:
    """
    - Remove acentos
    - Mantém letras/números/espaço/virgula/apóstrofo
    - Normaliza múltiplos espaços
    """
    if palavra is not None:
        nfkd = unicodedata.normalize("NFKD", palavra)
    else:
        nfkd = ""
    palavra_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])

    palavra_com_espacos = re.sub(r"[^a-zA-Z0-9 ,\'\\]", " ", palavra_sem_acento)
    palavra_com_espacos = " ".join(palavra_com_espacos.split())
    return palavra_com_espacos.replace("' ", "'").replace(" '", "'")

def limpa_str_parenteses(x: str) -> str:
    return limpa_str(limpa_parenteses(x)).lower()

def tooltip_string_to_list(x: str) -> list[str]:
    # mesmo comportamento do seu código: split por ',' após limpeza
    s = limpa_str_parenteses(x)
    if not s:
        return []
    return s.split("','")
