from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import getpass
import pickle

class Servidor():
    def __init__(self,matricula):
        self.matricula = matricula

class Operador(Servidor):
    def __init__(self,matricula,setor):
        #Recebe a matricula já definida na Parent Class
        super().__init__(matricula)
        self.setor = setor
class Processo():
    def __init__(self,processo):
        self.processo = processo

class Browser():
    def start(self):
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
        processos_recebidos = driver.find_element_by_id('tblProcessosRecebidos').find_element_by_tag_name('tbody')
        processos_recebidos_innerHTML = BeautifulSoup(processos_recebidos.get_attribute("innerHTML"), "html.parser")
        processos_list=processos_recebidos_innerHTML.find_all('tr')
Browser().start()
# TODO: Estruturar os dados abaixo
def entre_parenteses(x):
    return x[x.find("(")+1:x.rfind(")")]
with open('processos_caixa_entrada.obj','w') as file_pi:
    for processo in processos_list[1:]:
        children = processo.find_all('td')
        processo_pi = Processo(children[2].text)
        processo_pi.checkbox = processos_recebidos.find_element_by_id(children[0].find('input').get('id'))
        processo_pi.visualizado = 'processoVisualizado' in children[2].find('a')['class']
        processo_pi.visitado = 'processoVisitado' in children[2].find('a')['class']
        processo_pi.descricao = entre_parenteses(children[2].find('a')['onmouseover'])
        processo_pi.link = 'https://sei.df.gov.br/sei/' + children[2].find('a')['href']
        processo_pi.matricula_operador = entre_parenteses(children[3].text)
        pickle.dump(processo_pi, file_pi)
            #TODO: Continuar os de baixo
            #TODO: O children[1] pode conter até quatro <a>. Primeira Anotação, segunda informacao de assinatura e a terceira a tag. Deve-se entao pegar o getAttribute('onmouseover') de todos os <a> que esse children tiver
            #TODO: Usar urllib.parse para pegar parametros GET

#         processo_pi.anotacao = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         processo_pi.bool_assinado = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         processo_pi.retorno_programado = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         processo_pi.tag = processos_recebidos[count].children[1].getElementsByTagName('a')[0].getAttribute('onmouseover')
#         pickle.dump(processo_pi, file_pi)


# Caso queira aproveitar o resto do código #

# def get_req(num):
# 	driver.find_element_by_id('txtPesquisaRapida').send_keys(num)
# 	driver.find_element_by_id('txtPesquisaRapida').submit()
# 	time.sleep(3)
# 	# TODO: Pegar data remetimento do requerimento
# 	driver.switch_to.frame(driver.find_element_by_name('ifrVisualizacao'))
# 	try:
# 		driver.switch_to.frame(driver.find_element_by_id('ifrArvoreHtml'))
# 	except selenium.common.exceptions.NoSuchElementException:
# 		time.sleep(7)
# 		driver.switch_to.frame(driver.find_element_by_id('ifrArvoreHtml'))
# 	elem = driver.find_element_by_id("conteudo")
# 	source_code = BeautifulSoup(elem.get_attribute("innerHTML"), "html.parser")
# 	text = source_code.get_text()
# 	return text

#Acessar o requerimento
# time.sleep(3)
# print('Acessando o requerimento...\n\n')
# text = get_req(q)
# driver.quit()
# # print(text)
# dados = re.split('\n\n|:\n\xa0\xa0|\n\xa0\xa0|\n', text)
# rmv = ['',
#        'DADOS DO DEPENDENTE:',
#        'DADOS DA CERTIDÃO NOVA (PREENCHER APENAS SE SUA CERTIDÃO FOR DO MODELO NOVO):',
#        'DADOS DA CERTIDÃO ANTIGA (PREENCHER APENAS SE SUA CERTIDÃO FOR DO MODELO ANTIGO):',
#        'DADOS DOS PAIS DO BENEFICIÁRIO:',
#        'REQUEIRO, na forma da Lei, o RECONHECIMENTO do dependente especificado neste documento  junto à Corporação, além da concessão dos benefícios a seguir:',
#        'DECLARAÇÕES (PREENCHIMENTO OBRIGATÓRIO):']
# result = list(filter(lambda x: not (x in rmv), dados))
# # print(result)
# dados_dict = {result[2 * n]: result[2 * n + 1] for n in range(int(len(result) // 2))}
#
# try:
# 	driver.find_element_by_xpath('titulos')
# except WebDriverException:
# 	print(False)