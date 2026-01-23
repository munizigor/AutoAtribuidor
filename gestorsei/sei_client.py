# gestorsei/sei_client.py
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class SeiClient:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        print(f"Abrindo o SEI em: {url}")
        self.driver.get(url)
        time.sleep(3)

    def login(self, usuario: str, senha: str, orgao_value: str = "7"):
        self.driver.find_element(By.ID, "txtUsuario").send_keys(usuario)
        self.driver.find_element(By.ID, "pwdSenha").send_keys(senha)
        Select(self.driver.find_element(By.ID, "selOrgao")).select_by_value(orgao_value)
        self.driver.find_element(By.ID, "sbmAcessar").click()
        time.sleep(3)
