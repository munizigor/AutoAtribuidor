# gestorsei/cli.py
import getpass
from gestorsei.config import SEI_URL, FIREFOX_BINARY, GECKO_LOG_PATH, DEBUG_LOG_PATH, BANNER, CSV_DIR
from gestorsei.webdriver_factory import create_firefox_driver
from gestorsei.sei_client import SeiClient
from gestorsei.handlers.processos import consultar_andamentos, ler_processos_recebidos
from gestorsei.handlers.pesquisa import salvar_processos_unidade
from gestorsei.utils.env import load_sei_credentials

def main():
    print(BANNER)

    # tenta carregar do .env (raiz do projeto)
    print("Verificando se há credenciais salvas... ")
    usuario, senha, orgao_value = load_sei_credentials()

    # fallback para input se não existir
    if not usuario:
        usuario = input("\nInforme sua matrícula: ").strip()

    if not senha:
        senha = getpass.getpass("Informe a Senha: ")

    if not orgao_value:
        orgao_value = input("Informe o código do órgão: ").strip()

    driver = create_firefox_driver(
        firefox_binary=FIREFOX_BINARY,
        gecko_log_path=str(GECKO_LOG_PATH),
        headless=False,
    )

    sei = SeiClient(driver)
    sei.open(SEI_URL)
    sei.login(usuario, senha, orgao_value=orgao_value)

    # -------------------------------------------------------
    # Aqui ficam os comandos do seu sistema (menu simples)
    # -------------------------------------------------------
    print("\nO que deseja fazer?")
    print("1 - Extrair Andamentos SEI a partir de um CSV de processos")
    print("2 - Ler processos recebidos e salvar CSV")
    print("3 - Pesquisar processos por unidade e salvar CSV")
    opcao = input("Escolha (1/2/3): ").strip()

    if opcao == "1":
        consultar_andamentos(sei, CSV_DIR / "processos.csv")
        print("\n✅ Processos abertos com sucesso.")

    elif opcao == "2":
        output = CSV_DIR / "processos_recebidos.csv"
        ler_processos_recebidos(sei, output)
        print(f"\n✅ CSV salvo em: {output}")

    elif opcao == "3":
        cod_unidade = input("Informe o código da unidade: ").strip()
        output = CSV_DIR / "processos_save.csv"
        salvar_processos_unidade(sei, cod_unidade, output)
        print(f"\n✅ CSV salvo em: {output}")

    else:
        print("\n❌ Opção inválida.")

    # opcional: fechar browser ao final
    # driver.quit()
