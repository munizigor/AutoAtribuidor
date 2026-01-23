# gestorsei/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent  # ajuste se necessário

load_dotenv(dotenv_path=PROJECT_DIR / ".env", override=False)
SEI_URL = os.getenv("SEI_URL")
FIREFOX_BINARY = os.getenv("FIREFOX_BINARY")

CSV_DIR = PROJECT_DIR / "csv"
DEBUG_LOG_PATH = PROJECT_DIR / ".cursor" / "debug.log"
GECKO_LOG_PATH = PROJECT_DIR / "geckodriver.log"


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

