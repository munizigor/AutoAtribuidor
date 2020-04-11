from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import getpass
import unicodedata
import re

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
        print('Iniciando o programa...\n\n')
        # Entrar no SEI
        usuario = input('Informe sua matrícula: ')
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
    def processos_list(self):
        processos_recebidos = super().login().find_element_by_id('tblProcessosRecebidos').find_element_by_tag_name('tbody')
        processos_recebidos_innerHTML = BeautifulSoup(processos_recebidos.get_attribute("innerHTML"), "html.parser")
        processos = processos_recebidos_innerHTML.find_all('tr')
        return processos,processos_recebidos
    def selecionar(self):
        processos = self.processos_list()
        for processo in processos[0][1:]:
            children = processo.find_all('td')
            processo_pi = Processo(children[2].text)
            processo_pi.checkbox = processos[1].find_element_by_id(children[0].find('input').get('id'))
            processo_pi.visualizado = 'processoVisualizado' in children[2].find('a')['class']
            processo_pi.visitado = 'processoVisitado' in children[2].find('a')['class']
            processo_pi.descricao = limpastr(entre_parenteses(children[2].find('a')['onmouseover'])).lower()
            processo_pi.link = 'https://sei.df.gov.br/sei/' + children[2].find('a')['href']
            processo_pi.matricula_operador = entre_parenteses(children[3].text)
            # pickle.dump(processo_pi, file_pi)
            print(processo_pi)
            if ('dependente' in processo_pi.descricao) or ('beneficiario' in processo_pi.descricao) or (
                    'luto' in processo_pi.descricao) or ('funeral' in processo_pi.descricao) or (
                    'moradia' in processo_pi.descricao):
                processo_pi.checkbox.click()
            #TODO: Continuar os de baixo
            #TODO: O children[1] pode conter até quatro <a>. Primeira Anotação, segunda informacao de assinatura e a terceira a tag. Deve-se entao pegar o getAttribute('onmouseover') de todos os <a> que esse children tiver
            #TODO: Usar urllib.parse para pegar parametros GET

#         processo_pi.anotacao = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         processo_pi.bool_assinado = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         processo_pi.retorno_programado = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         processo_pi.tag = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
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

def entre_parenteses(x):
    return x[x.find("(")+1:x.rfind(")")]
def limpastr(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    if palavra != None:
        nfkd = unicodedata.normalize('NFKD', palavra)
    else:
        nfkd = ''
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 ,\'\\\]', '', palavraSemAcento)

ProcessoHandler().selecionar()