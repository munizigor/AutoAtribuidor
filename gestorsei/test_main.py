import unittest
import main

#todo: pegar do video do Corey (https://www.youtube.com/watch?v=6tNS--WetLI) em 28m30s esquema pra criar um html-source pre-salvo pra testes
class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls): #Funcao pra rodar no inicio geral
        pass
    @classmethod
    def tearDownClass(cls): #Funcao pra rodar no fim geral
        pass
    def setUp(self): #Funcao pra rodar no inicio de cada teste
        self.processo_1 = main.Processo('002-2000/2020')
        self.processo_2 = main.Processo('003-5265/2020')
        self.servidor_1 = main.Servidor('1577665')
        self.servidor_2 = main.Servidor('1577661')
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
        self.assertEqual(main.entre_parenteses('Nome do Proc (Serviço Administrativo)'),'Serviço Administrativo')
        self.assertEqual(main.entre_parenteses('Nome do Proc (Serviço Administrativo(Pessoal))'),
                         'Serviço Administrativo(Pessoal)')
        self.assertEqual(main.entre_parenteses('Nome do Proc (Serviço Administrativo)(Pessoal(Texto))'),
                         'Serviço Administrativo)(Pessoal(Texto)')
    def test_limpastr(self):
        self.assertEqual(main.limpastr('Oboé miçanga àêáéíóû'),'Oboe micanga aeaeiou')
if __name__ == '__main__':
    unittest.main()