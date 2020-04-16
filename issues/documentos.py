from gestorsei import main

class ProcessoHandlerUnique(main.Browser()):
    def abrir_processos(self,filepath):
        driver = super().login()
        #Entrar no processo
        driver.find_element_by_id('P30806216').find_element_by_xpath("//*[text()='00053-00022307/2020-52']").click()
        #Clica em gerar documento
        driver.find_element_by_id('divArvoreAcoes').find_elements_by_tag_name('a')[0].click()
        time.sleep(5)
        #Digita Memorando
        driver.find_element_by_id('txtFiltro').send_keys('Memorando')
        #Clica em memorando
        driver.find_elements_by_tag_name('tbody')[0].find_element_by_xpath("//*[text()='Memorando']").click()
        # Escreve a Descricao do Documento
        time.sleep(5)
        driver.find_element_by_id('txtDescricao').send_keys('Descricao do documento')
        #Clica em Restrito
        driver.find_element_by_id('optRestrito').click()
        #Escolhe a Hipótese Legal
        Select(driver.find_element_by_id('optRestrito')).select_by_value('35')
        driver.find_element_by_id('btnSalvar').click()
        time.sleep(5)
        # Abre a última janela aberta, a de edição do documento
        window_editar_documento = driver.window_handles[-1]
        # Muda para a janela de edição
        driver.switch_to.window(window_editar_documento)
        # Muda para frame de texto
        driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[2])
        # Limpar texto do frame
        driver.find_element_by_xpath('/html/body').clear()
        # Digitar o texto desejado
        driver.find_element_by_xpath('/html/body').send_keys('ESTE É UM DOCUMENTO TESTE',Keys.ENTER)
        # Voltar para o conteudo original
        driver.switch_to.default_content()
        # Salvar o escrito
        driver.execute_script('CKEDITOR.tools.callFunction(212, this);return false;')
        # Fechar janela
        time.sleep(5)
        driver.close()
        # Voltar para tela
        driver.switch_to.window(driver.window_handles[0])
