# gestorsei/handlers/processos.py
import random
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, JavascriptException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gestorsei.domain.models import Processo
from gestorsei.utils.strings import limpa_parenteses, limpa_str_parenteses
from gestorsei.utils.io_csv import read_csv_rows, write_csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def abrir_processo(sei, num_processo):
    """Busca um processo específico e garante que a página carregou."""
    driver = sei.driver
    wait = WebDriverWait(driver, 40)
    
    # ✅ 1. Garante que estamos fora de qualquer iframe antes de pesquisar
    driver.switch_to.default_content() # Sempre volta ao topo
    campo = wait.until(EC.element_to_be_clickable((By.ID, "txtPesquisaRapida")))
    campo.clear()
    campo.send_keys(num_processo, Keys.ENTER)
    time.sleep(1)
    driver.switch_to.default_content()

def consultar_andamentos(sei, csv_path: Path):
    """Lê o CSV e, para cada processo, clica em Consultar Andamento."""
    driver = sei.driver
    wait = WebDriverWait(driver, 15)

    for line in read_csv_rows(csv_path):
        if not line or not line[0].strip():
            continue

        proc = line[0].strip()
        print(f"Processando: {proc}")

        try:
            # 1. Abre o processo e já entra no iframe da Árvore
            abrir_processo(sei, proc)

            # 2. Localiza e clica no botão de Consultar Andamento
            # Usamos o ID que você forneceu: divConsultarAndamento
            # Espera o frame da árvore (menu esquerdo) carregar, pois é onde os botões ficam
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
            botao_andamento = wait.until(EC.element_to_be_clickable((By.ID, "divConsultarAndamento")))
            botao_andamento.click()

            # Espera o frame da árvore (menu esquerdo) carregar, pois é onde os botões ficam
            driver.switch_to.default_content()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrConteudoVisualizacao")))
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))

            print(f"✓ Andamentos consultados para {proc}")
            
            # Aqui você pode adicionar a lógica para ler a tabela de andamentos se precisar
            
        except TimeoutException:
            print(f"✗ Erro: Botão ou Processo {proc} não encontrado.")
        except Exception as e:
            print(f"⚠ Erro inesperado no processo {proc}: {e}")
        finally:
            # Garante que volta para o conteúdo principal para a próxima busca
            driver.switch_to.default_content()

            # --- Throttling Randômico ---
            # random.uniform gera um número flutuante (ex: 3.42s) o que é menos "robótico"
            delay = random.uniform(1, 2)
            print(f"Aguardando {delay:.2f}s antes da próxima requisição...")
            time.sleep(delay)

def ler_processos_recebidos(sei, output_csv_path: Path):
    """
    Lê a tabela 'Processos Recebidos' e salva em CSV:
    Processo, Descricao, Anotacoes, Tag
    """
    driver = sei.driver

    rows_out: list[list[str]] = []

    while True:
        processos_recebidos = (
            driver.find_element(By.ID, "tblProcessosRecebidos")
            .find_element(By.TAG_NAME, "tbody")
        )

        soup = BeautifulSoup(processos_recebidos.get_attribute("innerHTML"), "html.parser")
        processos = soup.find_all("tr")

        for processo in processos[1:]:
            children = processo.find_all("td")
            if len(children) < 3:
                continue

            processo_pi = Processo(children[2].text)
            processo_pi.anotacao = ""
            processo_pi.tag = ""

            if len(children[1].find_all("a")) != 0:
                for child in children[1].find_all("a"):
                    href = child.get("href", "")
                    onmouseover = child.get("onmouseover", "")

                    if "anotacao_registrar" in href:
                        processo_pi.anotacao = limpa_parenteses(onmouseover)
                    elif "andamento_marcador_gerenciar" in href:
                        processo_pi.tag = limpa_parenteses(onmouseover)

            # descrição vem do tooltip no onmouseover do link do processo
            a_tag = children[2].find("a")
            if a_tag and a_tag.get("onmouseover"):
                processo_pi.descricao = limpa_str_parenteses(a_tag["onmouseover"])
            else:
                processo_pi.descricao = ""

            rows_out.append([processo_pi.processo, processo_pi.descricao, processo_pi.anotacao, processo_pi.tag])

        # paginação
        if len(driver.find_elements(By.ID, "lnkRecebidosProximaPaginaSuperior")) != 0:
            driver.find_element(By.ID, "lnkRecebidosProximaPaginaSuperior").click()
            time.sleep(5)
        else:
            break

    write_csv(
        output_csv_path,
        header=["Processo", "Descricao", "Anotacoes", "Tag"],
        rows=rows_out,
    )
