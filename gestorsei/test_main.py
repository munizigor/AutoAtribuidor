import unittest
from . import main

#todo: pegar do video do Corey (https://www.youtube.com/watch?v=6tNS--WetLI) em 28m30s esquema pra criar um html-source pre-salvo pra testes
class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls): #Funcao pra rodar no inicio geral
        pass
    @classmethod
    def tearDownClass(cls): #Funcao pra rodar no fim geral
        pass
    def setUp(self): #Funcao pra rodar no inicio de cada teste
        pass
        # self.processo_1 = main.Processo('002-2000/2020')
        # self.processo_2 = main.Processo('003-5265/2020')
        # self.servidor_1 = main.Servidor('1577665')
        # self.servidor_2 = main.Servidor('1577661')
    def tearDown(self): #Funcao pra rodar no fim de cada teste
        pass
    def test_Processo_str(self):
        teste = main.Processo('002-2000/2020')
        teste.descricao = ('Processo Teste')
        self.assertEqual(teste.__str__(),'002-2000/2020 - Processo Teste')
    def test_Servidor_str(self):
        teste = main.Servidor('1577665')
        self.assertEqual(teste.__str__(),'1577665')
    def test_Operador_str(self):
        teste = main.Operador('1577661','Dependentes')
        self.assertEqual(teste.__str__(),'1577661 - Dependentes')
    def test_entre_parenteses(self):
        self.assertEqual(main.limpa_parenteses('Nome do Proc (Serviço Administrativo)'), 'Serviço Administrativo')
        self.assertEqual(main.limpa_parenteses('Nome do Proc (Serviço Administrativo(Pessoal))'),
                         'Serviço Administrativo(Pessoal)')
        self.assertEqual(main.limpa_parenteses('Nome do Proc (Serviço Administrativo)(Pessoal(Texto))'),
                         'Serviço Administrativo)(Pessoal(Texto)')
        self.assertEqual(main.limpa_parenteses(
            "return infraTooltipMostrar('Informação sobre uso de uniforme -EPI - BG 230/2019','CBMDF - Serviço Administrativo Diário');"),
            "'Informação sobre uso de uniforme -EPI - BG 230/2019','CBMDF - Serviço Administrativo Diário'")
    def test_strings(self):
        self.assertEqual(main.limpa_str('Oboé miçanga àêáéíóû'), 'Oboe micanga aeaeiou')
        self.assertEqual(main.limpa_str('OF.SN.2020 TRT -  10ªREG  VT GAMA'), 'OF SN 2020 TRT 10aREG VT GAMA')
        self.assertEqual(main.limpa_str('CBMDF - Serviço Administrativo Diário'), 'CBMDF Servico Administrativo Diario')
        self.assertEqual(main.limpa_str('.OF.20.2020 SEJUSP SUINT SSP MG '), 'OF 20 2020 SEJUSP SUINT SSP MG')
        self.assertEqual(main.limpa_str_parenteses(
            "return infraTooltipMostrar('.OF. 20.2020 SEJUSP SUINT SSP MG','Pessoal: Viagem a Serviço (Diárias, Passagens e Relatório)');"),
                                       "'of 20 2020 sejusp suint ssp mg','pessoal viagem a servico diarias, passagens e relatorio'")
    def test_tooltip_to_list(self):
        self.assertEqual(main.tooltip_string_to_list(

if __name__ == '__main__':
    unittest.main()