# gestorsei/config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent  # ajuste se necessário

CSV_DIR = PROJECT_DIR / "csv"
DEBUG_LOG_PATH = PROJECT_DIR / ".cursor" / "debug.log"
GECKO_LOG_PATH = PROJECT_DIR / "geckodriver.log"

SEI_URL = "https://sei.df.gov.br/"
FIREFOX_BINARY = r"C:\Program Files\Mozilla Firefox\firefox.exe"

BANNER = r"""
  /$$$$$$  /$$$$$$$$ /$$$$$$          /$$$$$$$  /$$$$$$ /$$         /$$$$$$  /$$$$$$$$
 /$$__  $$| $$_____/|_  $$_/         | $$__  $$|_  $$_/| $$        /$$__  $$|__  $$__/
| $$  \__/| $$        | $$           | $$  \ $$  | $$  | $$       | $$  \ $$   | $$   
|  $$$$$$ | $$$$$     | $$           | $$$$$$$/  | $$  | $$       | $$  | $$   | $$   
 \____  $$| $$__/     | $$           | $$____/   | $$  | $$       | $$  | $$   | $$   
 /$$  \ $$| $$        | $$           | $$        | $$  | $$       | $$  | $$   | $$   
|  $$$$$$/| $$$$$$$$ /$$$$$$         | $$       /$$$$$$| $$$$$$$$|  $$$$$$/   | $$   
 \______/ |________/|______/         |__/      |______/|________/ \______/    |__/ 

                                      ✈
                                S E I   P I L O T
                     Automação de Rotina Processual no SEI

                     Desenvolvido por: Igor MUNIZ da Silva
                              MIT License
                                2026

==============================================================================================
"""

