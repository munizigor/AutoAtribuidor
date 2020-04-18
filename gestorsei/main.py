from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, JavascriptException, NoSuchElementException
import time
from bs4 import BeautifulSoup
import getpass
import unicodedata
import re
import csv
import os

# Funcoes de inicio
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
main_path = os.path.dirname(os.path.abspath(__file__))
def full_path(file):
    return os.path.join(main_path,file)

banner = ''' \n\n\n\n
  /$$$$$$                        /$$                                /$$$$$$  /$$$$$$$$ /$$$$$$
 /$$__  $$                      | $$                               /$$__  $$| $$_____/|_  $$_/
| $$  \__/  /$$$$$$   /$$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$       | $$  \__/| $$        | $$  
| $$ /$$$$ /$$__  $$ /$$_____/|_  $$_/   /$$__  $$ /$$__  $$      |  $$$$$$ | $$$$$     | $$  
| $$|_  $$| $$$$$$$$|  $$$$$$   | $$    | $$  \ $$| $$  \__/       \____  $$| $$__/     | $$  
| $$  \ $$| $$_____/ \____  $$  | $$ /$$| $$  | $$| $$             /$$  \ $$| $$        | $$  
|  $$$$$$/|  $$$$$$$ /$$$$$$$/  |  $$$$/|  $$$$$$/| $$            |  $$$$$$/| $$$$$$$$ /$$$$$$
 \______/  \_______/|_______/    \___/   \______/ |__/             \______/ |________/|______/
                             
                             
                             Desenvolvido por: Igor MUNIZ da Silva
                                         MIT License
                                             2020
                                             
==============================================================================================
'''

# Definicao de Classes
class Servidor():
    def __init__(self,matricula):
        self.matricula = matricula
    def __str__(self):
        return self.matricula

class Operador(Servidor):
    def __init__(self,matricula,setor):
        #Recebe a matricula já definida na Parent Class
        super().__init__(matricula)
        self.setor = setor
    def __str__(self):
        return self.matricula+' - '+self.setor

class Processo():
    def __init__(self,processo):
        self.processo = processo
    def __str__(self):
        return self.processo+' - '+self.descricao

class Browser():
    def login(self):
        clear()
        print(banner)
        # Entrar no SEI
        usuario = input('\n\nInforme sua matrícula: ')
        password = getpass.getpass('Informe a Senha: ')
        options = Options()
        # options.headless = True #todo: definir se browser ficara ativo ou oculto
        driver = webdriver.Firefox(options=options)
        print('Abrindo o navegador...\n\n')
        driver.get('https://sei.df.gov.br/')
        time.sleep(3)
        driver.find_element_by_id('txtUsuario').send_keys(usuario)
        driver.find_element_by_id('pwdSenha').send_keys(password)
        Select(driver.find_element_by_id('selOrgao')).select_by_value('7')
        print('Logando no SEI...\n\n')
        driver.find_element_by_id('sbmLogin').click()
        #TODO:Se erro de login
        time.sleep(3)
        return driver

class ProcessoHandler(Browser):
    def abrir_processos(self,filepath):
        driver = super().login()
        with open(filepath,'r') as processos:
            processos_reader = csv.reader(processos)
            for line in processos_reader:
                if line[0] == '':
                    continue
                else:
                    try:
                        driver.find_element_by_id('txtPesquisaRapida').send_keys(line[0],Keys.ENTER)
                    except NoSuchElementException:
                        time.sleep(10)
                        driver.find_element_by_id('txtPesquisaRapida').send_keys(line[0], Keys.ENTER)
                # driver.find_element_by_id('txtPesquisaRapida').send_keys('00053-00088071/2018-01',Keys.ENTER)
                    time.sleep(3)
                    try:
                        driver.switch_to.frame('ifrVisualizacao')
                    except NoSuchElementException:
                        time.sleep(20)
                        driver.switch_to.frame('ifrVisualizacao')
                    try:
                        driver.execute_script('reabrirProcesso()')
                    except JavascriptException:
                        time.sleep(15)
                        driver.execute_script('reabrirProcesso()')
                    time.sleep(3)
                    try:
                        alert = driver.switch_to.alert
                        assert 'Processo já está aberto na unidade atual.' in alert.text or 'Processo está anexado.' in alert.text
                        alert.accept()
                    except NoAlertPresentException:
                        pass
                    driver.switch_to.default_content()

    def ler_processos(self):
        driver = super().login()
        # return driver
        with open(full_path('csv/processos_recebidos.csv'), mode='w') as processos_save:
            processos_writer = csv.writer(processos_save)
            processos_writer.writerow(['Processo','Descricao','Anotacoes','Tag'])
            while True:
                processos_recebidos = driver.find_element_by_id('tblProcessosRecebidos').find_element_by_tag_name(
                    'tbody')
                processos_recebidos_innerHTML = BeautifulSoup(processos_recebidos.get_attribute("innerHTML"),
                                                              "html.parser")
                processos = processos_recebidos_innerHTML.find_all('tr')
                for processo in processos[1:]:
                    children = processo.find_all('td')
                    processo_pi = Processo(children[2].text)
                    # processo_pi.checkbox = processos_recebidos.find_element_by_id(children[0].find('input').get('id'))
                    processo_pi.anotacao = ''
                    processo_pi.tag = ''
                    if len(children[1].find_all('a'))==0:
                        pass
                    else:
                        for child in children[1].find_all('a'):
                            processo_pi.anotacao = limpa_parenteses(child['onmouseover']) if (
                                        'anotacao_registrar' in child['href']) else processo_pi.anotacao
                            processo_pi.tag = limpa_parenteses(child['onmouseover']) if (
                                        'andamento_marcador_gerenciar' in child['href']) else processo_pi.tag
                    # processo_pi.visualizado = 'processoVisualizado' in children[2].find('a')['class']
                    # processo_pi.visitado = 'processoVisitado' in children[2].find('a')['class']
                    processo_pi.descricao = limpa_str_parenteses(children[2].find('a')['onmouseover'])
                    # processo_pi.link = 'https://sei.df.gov.br/sei/' + children[2].find('a')['href']
                    # processo_pi.matricula_operador = limpa_parenteses(children[3].text)
                    # if ('dependente' in processo_pi.descricao) or ('beneficiario' in processo_pi.descricao) or (
                    #         'luto' in processo_pi.descricao) or ('funeral' in processo_pi.descricao) or (
                    #         'moradia' in processo_pi.descricao):
                    #     processo_pi.checkbox.click()

                    processos_writer.writerow(
                        [processo_pi.processo, processo_pi.descricao, processo_pi.anotacao, processo_pi.tag])
                if len(driver.find_elements_by_id('lnkRecebidosProximaPaginaSuperior')) != 0:
                    driver.find_element_by_id('lnkRecebidosProximaPaginaSuperior').click()
                    time.sleep(5)
                else:
                    return
                #TODO: Continuar os de baixo
                #TODO: Usar urllib.parse para pegar parametros GET

    #         processo_pi.bool_assinado = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
    #         processo_pi.retorno_programado = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
    #         pickle.dump(processo_pi, file_pi)
    def atribuir (self):
        pass
    def arquivar (self):
        pass
    def etiquetar (self):
        pass
    def enviar (self):
        pass
    def atualizar_andamento (self):
        pass
    def concluir (self):
        pass
    def inserir_documento (self):
        pass
    def inserir_anotacao (self):
        pass

class Pesquisa(Browser):
    def ler_processos(self,cod_unidade):
        driver = super().login()
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li[4]/a').click()
        time.sleep(3)
        driver.execute_script('document.getElementById(\'hdnIdUnidade\').value='+cod_unidade)
        driver.find_element_by_id('sbmPesquisar').click()
        return driver
    def salvar_processos(self,cod_unidade):
        driver = self.ler_processos(cod_unidade)
        limit_count = driver.find_elements_by_class_name('barra')[0].text.split(' ')
        limit_count = int(limit_count[-1])
        print(limit_count)
        count=0
        with open(full_path('csv/processos_save.csv'), mode='w') as processos_save:
            processos_writer = csv.writer(processos_save)
            processos_writer.writerow(['Título', 'Processo'])
            while count<limit_count:
                for elem in driver.find_elements_by_class_name('resTituloEsquerda'):
                    processos_writer.writerow([elem.text,elem.text[elem.text.find("º")+2:elem.text.rfind("(")-1]])
                count+=10
                driver.execute_script('navegar('+str(count)+')')
                time.sleep(7)
class Atribuir():
    def __init__(self):
        ProcessoHandler().ler_processos()
        with open(full_path('csv/processos_recebidos.csv'), mode='r') as processos_read:
            # TODO: seguir tutorial https://github.com/justmarkham/pycon-2016-tutorial/blob/master/tutorial_with_output.ipynb
            pass

def limpa_parenteses(x):
    return x[x.find("(")+1:x.rfind(")")]
def limpa_str(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    if palavra != None:
        nfkd = unicodedata.normalize('NFKD', palavra)
    else:
        nfkd = ''
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    palavra_com_espacos = re.sub('[^a-zA-Z0-9 ,\'\\\]', ' ', palavraSemAcento)
    palavra_com_espacos = ' '.join(palavra_com_espacos.split())
    return palavra_com_espacos.replace('\' ','\'').replace(' \'','\'')
def limpa_str_parenteses(x):
    return limpa_str(limpa_parenteses(x)).lower()
def tooltip_string_to_list(x):
    return limpa_str_parenteses(x).split('\',\'')

# ProcessoHandler().abrir_processos(full_path('csv/processos_sample2.csv'))
# ProcessoHandler().ler_processos()
# Pesquisa().salvar_processos('110001369')