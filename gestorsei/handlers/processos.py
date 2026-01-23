# gestorsei/handlers/processos.py
import csv
import random
import time
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, JavascriptException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gestorsei.domain.models import Processo
from gestorsei.utils.strings import limpa_parenteses, limpa_str_parenteses
from gestorsei.utils.io_csv import read_csv_rows, write_csv

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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = csv_path.parent / f"historico_andamentos_completo_{timestamp}.csv"
    
    # Prepara cabeçalho
    with output_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Processo", "Data/Hora", "Unidade", "Usuário", "Descrição"])
    
    print(f"Arquivo de saída criado: {output_file}")

    for line in read_csv_rows(csv_path):
        if not line or not line[0].strip():
            continue

        proc = line[0].strip()
        print(f"Processando: {proc}")
        
        # Buffer local para este processo
        process_history_data = []

        try:
            # 1. Abre o processo e já entra no iframe da Árvore
            abrir_processo(sei, proc)

            # 2. Localiza e clica no botão de Consultar Andamento
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
            botao_andamento = wait.until(EC.element_to_be_clickable((By.ID, "divConsultarAndamento")))
            botao_andamento.click()

            # Volta para o default e entra nos iframes de visualização
            driver.switch_to.default_content()
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrConteudoVisualizacao")))
            
            # Aqui pode ser ifrVisualizacao ou direto o conteudo, dependendo da versao do SEI
            # O código original assumia ifrVisualizacao. Vamos manter, mas ficar atentos.
            try:
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
            except TimeoutException:
                # As vezes não tem ifrVisualizacao se abrir direto na div
                pass

            # 3. Garante que está exibindo o histórico completo (P) e não resumido (R)
            try:
                # O elemento hidden hdnTipoHistorico guarda o estado atual (P ou R)
               # Pode não existir se a página não carregou bem, mas o wait cuida
                hdn_tipo = wait.until(EC.presence_of_element_located((By.ID, "hdnTipoHistorico")))
                valor_tipo = hdn_tipo.get_attribute("value")

                if valor_tipo != "P":
                     # ALTERAÇÃO: Ao invés de usar a função JS verHistorico('P'),
                    # setamos o valor do hidden e submetemos o formulário.
                    driver.execute_script("arguments[0].value = 'P';", hdn_tipo)
                    hdn_tipo.submit()
                    time.sleep(1) 

                # Espera a tabela de historico estar disponivel
                wait.until(EC.presence_of_element_located((By.ID, "tblHistorico")))
                
            except (NoSuchElementException, Exception):
                print(f"Erro ao verificar tipo de histórico ou carregar página para {proc}")
                process_history_data.append([proc, "ERRO: Falha ao carregar histórico", "", "", ""])
                continue

            # 4. Loop Recursivo de Paginação
            while True:
                # Parse da tabela
                soup = BeautifulSoup(driver.page_source, "html.parser")
                tabela = soup.find("table", {"id": "tblHistorico"})

                if tabela:
                    rows = tabela.find_all("tr")
                    # Pula o cabeçalho (primeira tr)
                    for row in rows[1:]:
                        cols = row.find_all("td")
                        cols_text = [c.get_text() for c in cols]
                        if len(cols_text) >= 4:
                            # Assumindo indices padrao
                            data_hora = cols_text[0]
                            unidade = cols_text[1]
                            usuario = cols_text[2]
                            descricao = cols_text[3]
                            process_history_data.append([proc, data_hora, unidade, usuario, descricao])
                
                # Verifica paginação
                try:
                    proxima = driver.find_element(By.ID, "lnkInfraProximaPaginaInferior")
                    if proxima.is_displayed() and proxima.is_enabled():
                        proxima.click()
                        # Espera recarregar a tabela (staleness ou element present)
                        time.sleep(1) 
                        wait.until(EC.presence_of_element_located((By.ID, "tblHistorico")))
                    else:
                        break
                except NoSuchElementException:
                    break

            print(f"✓ Andamentos (Histórico) extraídos para {proc}: {len(process_history_data)} registros.")

        except TimeoutException:
            print(f"✗ Erro: Timeout ao processar {proc}.")
            process_history_data.append([proc, "ERRO: Timeout ao tentar localizar elementos ou carregar página", "", "", ""])
        except Exception as e:
            print(f"⚠ Erro inesperado no processo {proc}: {e}")
            process_history_data.append([proc, f"ERRO: {str(e)}", "", "", ""])
        finally:
            driver.switch_to.default_content()
            
            # --- Incremental Save ---
            if process_history_data:
                try:
                    with output_file.open("a", encoding="utf-8", newline="") as f:
                        writer = csv.writer(f)
                        for row in process_history_data:
                            writer.writerow(row)
                except Exception as csv_err:
                    print(f"Erro ao salvar CSV incremental: {csv_err}")

            # Throttling
            time.sleep(random.uniform(1, 2))

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
