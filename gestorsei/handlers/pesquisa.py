# gestorsei/handlers/pesquisa.py
import time
from pathlib import Path
from selenium.webdriver.common.by import By

from gestorsei.utils.io_csv import write_csv

def abrir_pesquisa_unidade(sei, cod_unidade: str):
    driver = sei.driver

    # mantém o seu XPath (ideal seria trocar por seletor mais robusto)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/ul/li[4]/a").click()
    time.sleep(3)

    driver.execute_script(f"document.getElementById('hdnIdUnidade').value={cod_unidade}")
    driver.find_element(By.ID, "sbmPesquisar").click()
    return driver

def salvar_processos_unidade(sei, cod_unidade: str, output_csv_path: Path):
    driver = abrir_pesquisa_unidade(sei, cod_unidade)

    limit_text = driver.find_elements(By.CLASS_NAME, "barra")[0].text.split(" ")
    limit_count = int(limit_text[-1])

    rows_out: list[list[str]] = []
    count = 0

    while count < limit_count:
        for elem in driver.find_elements(By.CLASS_NAME, "resTituloEsquerda"):
            texto = elem.text
            # mesma extração que você faz hoje
            processo_num = texto[texto.find("º") + 2 : texto.rfind("(") - 1]
            rows_out.append([texto, processo_num])

        count += 10
        driver.execute_script(f"navegar({count})")
        time.sleep(7)

    write_csv(
        output_csv_path,
        header=["Título", "Processo"],
        rows=rows_out,
    )
