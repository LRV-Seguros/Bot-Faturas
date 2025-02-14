import os
import time
import re
from selenium.webdriver import Keys
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests
from PyPDF2 import PdfReader
import calendar
from datetime import datetime

lista_pdfs = []
lista_documentos = []
nome_arquivo = f"feitos.txt"

meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}



def quiver1(dados, arquivos):
    diretorio_corrente = os.getcwd()
    arquivos = [os.path.join(diretorio_corrente, nome) for nome in arquivos[1:]]
    driver = webdriver.Chrome()
    driver.maximize_window()
    link = 'https://www.corretor-online.com.br/default.aspx'
    while True:
        driver.get(link)
        corretora = 'lrv'
        login = 'Cadastro.FaturaTransporte'
        senha = 'Lrv@2025'
        while True:
            try:
                campo_corretora = driver.find_element(By.XPATH, '//*[@id="Corretor"]')
                campo_login = driver.find_element(By.XPATH, '//*[@id="Usuario"]')
                campo_senha = driver.find_element(By.XPATH, '//*[@id="Senha"]')
                campo_corretora.send_keys(corretora)
                campo_login.send_keys(login)
                campo_senha.send_keys(senha)
                botao_entrar = driver.find_element(By.XPATH, '//*[@id="btnEntrar"]')
                botao_entrar.click()
                time.sleep(5)
                break
            except:
                pass

        break

    while True:
        try:
            driver.switch_to.default_content()
            while True:
                try:
                    try:
                        driver.find_element(By.XPATH, '//*[@id="MenuTopo"]/header/div[1]/div[1]/div[1]/i').click()
                        time.sleep(2)
                    except:
                        pass
                    botao_operacional = driver.find_element(By.XPATH, '//*[@id="navSide"]/div[2]/a')

                    break
                except:
                    driver.refresh()
                    time.sleep(1)

            time.sleep(2)
            driver.switch_to.default_content()
            time.sleep(.2)
            botao_operacional.click()
            break
        except:
            pass
    time.sleep(3)
    if len(driver.find_elements(By.XPATH, '/html/body/div[3]/div')) == 0:
        print('entrei aqui')
        while True:
            try:
                driver.switch_to.frame("ZonaInterna")
                break
            except:
                pass

        botao_propostas = driver.find_element(By.XPATH,
                                              '//*[@id="card-conteudo-dados-OPERACIONAL_PRINCIPAL"]/ul/li[2]/div[1]/a')
        botao_propostas.click()

        while True:
            try:
                dropbox_fatura = driver.find_element(By.XPATH,
                                                     '//*[@id="DIVTipoConsulta2"]/div/span/span[1]/span/span[2]')
                dropbox_fatura.click()

                break
            except:
                pass
        time.sleep(1)
        elemento = driver.switch_to.active_element
        time.sleep(.2)
        elemento.send_keys('Nº da apólice')
        time.sleep(.2)
        elemento.send_keys(Keys.ARROW_DOWN)
        time.sleep(.2)
        elemento.send_keys(Keys.ENTER)
        time.sleep(.2)

        while True:
            try:
                campo_apolice = driver.find_element(By.XPATH, '//*[@id="NoApolice"]')
                break
            except:
                pass

        campo_apolice.send_keys(dados[0])
        time.sleep(.2)
        campo_apolice.send_keys(Keys.ENTER)
        time.sleep(2)
        while True:
            try:
                elemento = driver.find_element(By.XPATH, '//*[@id="BtEdiReg"]')
                driver.execute_script(
                    "var evt = new MouseEvent('dblclick', {bubbles: true, cancelable: true, view: window}); arguments[0].dispatchEvent(evt);",
                    elemento)
                break
            except:
                pass
        time.sleep(2)
        driver.switch_to.frame("ZonaInterna")
        while True:
            try:
                botao_plus = driver.find_element(By.XPATH, '//*[@id="trNovoEndosso"]/div[2]/div[1]/i')
                break
            except:
                pass
        botao_plus.click()

        while True:
            try:

                driver.switch_to.frame('Documento')
                time.sleep(1)
                campo_endosso = driver.find_element(By.XPATH, '//*[@id="Documento_Endosso"]')
                campo_endosso.send_keys(dados[1])

                break
            except:
                pass

        while True:
            try:
                dropbox_tipo_documento = driver.find_element(By.XPATH, '//*[@id="DIVDocumento_TipoDocumento"]/div/span')
                time.sleep(.2)
                dropbox_tipo_documento.click()
                time.sleep(.2)
                elemento = driver.switch_to.active_element
                elemento.send_keys('FATURA')
                time.sleep(.2)
                elemento.send_keys(Keys.ARROW_DOWN)
                time.sleep(.2)
                elemento.send_keys(Keys.ENTER)
                time.sleep(.2)

                break
            except:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        dropbox_sub_tipo = driver.find_element(By.XPATH, '//*[@id="select2-Documento_SubTipo-container"]')
        dropbox_sub_tipo.click()
        time.sleep(.2)
        elemento = driver.switch_to.active_element
        time.sleep(.2)
        elemento.send_keys('Averbação')
        time.sleep(.2)
        elemento.send_keys(Keys.ARROW_DOWN)
        time.sleep(.2)
        elemento.send_keys(Keys.ENTER)
        time.sleep(.2)
        campo_inicio_vigencia = driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]')
        campo_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_PropostaCia"]')
        campo_fim_vigencia = driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]')
        campo_data_emissao = driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]')
        campo_data_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]')
        botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
        time.sleep(.2)
        campo_data_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_data_proposta, dados[2])
        # driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]').send_keys(lista[2])
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="Documento_PropostaCia"]').clear()
        time.sleep(1)
        campo_inic_ivg = driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_inic_ivg, dados[4])
        # time.sleep(.2)
        # driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]').send_keys(Keys.BACKSPACE)
        time.sleep(1)
        # driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]').send_keys(lista[4])
        # time.sleep(1)
        campo_term_vig = driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_term_vig, dados[5])
        # time.sleep(.2)
        # driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]').send_keys(Keys.BACKSPACE)
        # time.sleep(1)
        # driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]').send_keys(lista[5])
        time.sleep(1)
        campo_data_emissao = driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_data_emissao, dados[6])
        # time.sleep(.2)
        # driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]').send_keys(Keys.BACKSPACE)
        time.sleep(1)
        campo_endosso.clear()
        time.sleep(.2)
        campo_endosso.send_keys(dados[1])
        time.sleep(.2)
        campo_proposta.clear()
        time.sleep(.2)
        campo_proposta.send_keys(dados[2])
        time.sleep(.2)


        botao_gravar.click()

        time.sleep(2)
        # driver.switch_to.frame("ZonaInterna")
        teste = driver.find_element(By.XPATH, '//*[@id="table_ff_sinistros"]')
        cont = 0
        while True:
            try:
                botao_premio = driver.find_element(By.XPATH, '//*[@id="icone-Premios"]')
                # actions = ActionChains(driver)
                # actions.double_click(botao_premio).perform()
                time.sleep(.2)
                botao_premio.click()
                break
            except:
                pass
            time.sleep(.2)
            if cont == 10:
                break
            cont = cont + 1

        while True:
            try:
                campo_meio_pag = driver.find_element(By.XPATH, '//*[@id="DIVDocumento_MeioPagto"]/div/span/span[1]')
                time.sleep(.2)
                campo_meio_pag.click()
                time.sleep(.2)
                elemento = driver.switch_to.active_element
                time.sleep(.2)
                elemento.send_keys('Boleto Bancario')
                time.sleep(.2)
                elemento.send_keys(Keys.ARROW_DOWN)
                time.sleep(.2)
                elemento.send_keys(Keys.ENTER)
                time.sleep(.2)
                campo_vencimento = driver.find_element(By.XPATH, '//*[@id="Documento_DataVencPrimeira"]')
                time.sleep(.2)
                campo_vencimento.clear()
                time.sleep(.2)
                campo_vencimento.send_keys(dados[-1])
                time.sleep(.2)
                campo_premio_liq = driver.find_element(By.XPATH, '//*[@id="Documento_PremioLiqDesc"]')
                time.sleep(.2)
                while campo_premio_liq.get_attribute("value") != '':
                    time.sleep(.2)
                    campo_premio_liq.send_keys(Keys.BACKSPACE)

                # time.sleep(.5)
                for char in dados[7].replace('.', ''):
                    campo_premio_liq.send_keys(char)
                    time.sleep(.2)
                campo_iof = driver.find_element(By.XPATH, '//*[@id="Documento_PercIof"]')
                campo_iof.clear()
                time.sleep(.2)
                driver.execute_script("arguments[0].value = arguments[1];", campo_iof, "7,38")
                time.sleep(.2)
                campo_iof.send_keys(Keys.TAB)
                break
            except:
                time.sleep(1)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                try:
                    botao_premio = driver.find_element(By.XPATH, '//*[@id="icone-Premios"]')
                    # actions = ActionChains(driver)
                    # actions.double_click(botao_premio).perform()
                    botao_premio.click()

                except:
                    pass

        botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
        botao_gravar.click()

        time.sleep(2)
        while True:
            try:
                botao_anexar = driver.find_element(By.XPATH, '//*[@id="BtAnexar"]')
                botao_anexar.click()
                break
            except:
                pass
        time.sleep(1)
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame("ScanImagem")
        time.sleep(1)
        botao_multiplos = driver.find_element(By.XPATH, '//*[@id="BtAbrirMultiplus"]')
        time.sleep(.2)
        botao_multiplos.click()
        time.sleep(1)
        driver.switch_to.frame("ScanImagem")
        time.sleep(1)
        teste = driver.find_element(By.XPATH, '//*[@id="files"]')
        time.sleep(1)
        teste.send_keys(arquivos[0])
        time.sleep(1)
        botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
        time.sleep(3)
        botao_voltar.click()

        time.sleep(5)

        arquivos = arquivos[1:]
        for arquivo in arquivos:
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            botao_incluir = driver.find_element(By.XPATH, '//*[@id="BtIncluir"]')
            botao_incluir.click()
            time.sleep(3)
            while True:
                try:
                    botao_multiplos = driver.find_element(By.XPATH, '//*[@id="BtAbrirMultiplus"]')
                    break
                except:
                    pass
            time.sleep(.2)
            botao_multiplos.click()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            time.sleep(1)
            teste = driver.find_element(By.XPATH, '//*[@id="files"]')
            teste.send_keys(arquivo)
            botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
            time.sleep(3)
            botao_voltar.click()
            time.sleep(3)
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
            time.sleep(3)

        """for arquivo in arquivos:
            time.sleep(1)
            input_upload = driver.find_element(By.XPATH, '//input[@type="file"]')
            time.sleep(.2)
            input_upload.send_keys(arquivo)
            time.sleep(3)
            try:
                os.remove(arquivo)
                print(f"O arquivo {arquivo} foi removido com sucesso.")
            except:
                print(f"O arquivo {arquivo} não foi encontrado.")"""
        time.sleep(2)
        botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
        time.sleep(3)
        botao_voltar.click()
        print('apertei o primeiro voltar')
        time.sleep(1)
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame("ScanImagem")
        time.sleep(1)
        botao_voltar2 = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
        time.sleep(.2)
        botao_voltar2.click()
        print('apertei o segundo voltar')
        time.sleep(1)
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame("ZonaInterna")
        time.sleep(1)
        driver.switch_to.frame("ZonaInterna")
        time.sleep(1)
        driver.switch_to.frame("Documento")
        time.sleep(1)
        botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
        time.sleep(1)
        botao_gravar.click()
        print('apertei o gravar')
        time.sleep(5)

    else:
        print('Número de usuarios excedido')

    driver.quit()


def quiver2(dados, arquivos):
    diretorio_corrente = os.getcwd()
    arquivos = [os.path.join(diretorio_corrente, nome) for nome in arquivos[1:]]
    print(arquivos)
    driver = webdriver.Chrome()
    driver.maximize_window()
    link = 'https://www.corretor-online.com.br/default.aspx'
    while True:
        driver.get(link)
        corretora = 'lrv'
        login = 'Cadastro.FaturaTransporte'
        senha = 'Lrv@2025'
        while True:
            try:
                campo_corretora = driver.find_element(By.XPATH, '//*[@id="Corretor"]')
                campo_login = driver.find_element(By.XPATH, '//*[@id="Usuario"]')
                campo_senha = driver.find_element(By.XPATH, '//*[@id="Senha"]')
                campo_corretora.send_keys(corretora)
                campo_login.send_keys(login)
                campo_senha.send_keys(senha)
                botao_entrar = driver.find_element(By.XPATH, '//*[@id="btnEntrar"]')
                botao_entrar.click()
                time.sleep(5)
                break
            except:
                pass

        break

    while True:
        try:
            driver.switch_to.default_content()
            while True:
                try:
                    try:
                        driver.find_element(By.XPATH, '//*[@id="MenuTopo"]/header/div[1]/div[1]/div[1]/i').click()
                        time.sleep(2)
                    except:
                        pass
                    botao_operacional = driver.find_element(By.XPATH, '//*[@id="navSide"]/div[2]/a')

                    break
                except:
                    driver.refresh()
                    time.sleep(1)

            time.sleep(2)
            driver.switch_to.default_content()
            time.sleep(.2)
            botao_operacional.click()
            break
        except:
            pass
    time.sleep(3)
    if len(driver.find_elements(By.XPATH, '/html/body/div[3]/div')) == 0:
        print('entrei aqui')
        while True:
            try:
                driver.switch_to.frame("ZonaInterna")
                break
            except:
                pass

        botao_propostas = driver.find_element(By.XPATH,
                                              '//*[@id="card-conteudo-dados-OPERACIONAL_PRINCIPAL"]/ul/li[2]/div[1]/a')
        time.sleep(.2)
        botao_propostas.click()

        while True:
            try:
                dropbox_fatura = driver.find_element(By.XPATH,
                                                     '//*[@id="DIVTipoConsulta2"]/div/span/span[1]/span/span[2]')
                time.sleep(.2)
                dropbox_fatura.click()

                break
            except:
                pass
        time.sleep(1)
        elemento = driver.switch_to.active_element
        time.sleep(.2)
        elemento.send_keys('Nº da apólice')
        time.sleep(.2)
        elemento.send_keys(Keys.ARROW_DOWN)
        time.sleep(.2)
        elemento.send_keys(Keys.ENTER)
        time.sleep(.2)
        while True:
            try:
                campo_apolice = driver.find_element(By.XPATH, '//*[@id="NoApolice"]')
                break
            except:
                pass

        campo_apolice.send_keys(dados[0])
        time.sleep(.2)
        campo_apolice.send_keys(Keys.ENTER)
        time.sleep(2)
        while True:
            try:
                elemento = driver.find_element(By.XPATH, '//*[@id="BtEdiReg"]')
                driver.execute_script(
                    "var evt = new MouseEvent('dblclick', {bubbles: true, cancelable: true, view: window}); arguments[0].dispatchEvent(evt);",
                    elemento)
                break
            except:
                pass
        time.sleep(2)
        driver.switch_to.frame("ZonaInterna")
        time.sleep(1)
        while True:
            try:
                botao_plus = driver.find_element(By.XPATH, '//*[@id="trNovoEndosso"]/div[2]/div[1]/i')
                break
            except:
                pass
            time.sleep(.2)
        botao_plus.click()
        time.sleep(1)
        while True:
            try:
                driver.switch_to.frame('Documento')
                time.sleep(1)
                campo_endosso = driver.find_element(By.XPATH, '//*[@id="Documento_Endosso"]')
                campo_endosso.send_keys(dados[1])

                break
            except:
                pass
            time.sleep(.2)

        while True:
            try:
                dropbox_tipo_documento = driver.find_element(By.XPATH, '//*[@id="DIVDocumento_TipoDocumento"]/div/span')
                time.sleep(.2)
                dropbox_tipo_documento.click()
                time.sleep(.2)
                elemento = driver.switch_to.active_element
                time.sleep(.2)
                elemento.send_keys('FATURA')
                time.sleep(.2)
                elemento.send_keys(Keys.ARROW_DOWN)
                time.sleep(.2)
                elemento.send_keys(Keys.ENTER)
                time.sleep(.2)

                break
            except:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(.2)
        dropbox_sub_tipo = driver.find_element(By.XPATH, '//*[@id="select2-Documento_SubTipo-container"]')
        time.sleep(.2)
        dropbox_sub_tipo.click()
        time.sleep(.2)
        elemento = driver.switch_to.active_element
        time.sleep(.2)
        elemento.send_keys('Averbação')
        time.sleep(.2)
        elemento.send_keys(Keys.ARROW_DOWN)
        time.sleep(.2)
        elemento.send_keys(Keys.ENTER)
        time.sleep(.2)
        campo_inicio_vigencia = driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]')
        campo_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_PropostaCia"]')
        campo_fim_vigencia = driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]')
        campo_data_emissao = driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]')
        campo_data_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]')
        botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
        time.sleep(.2)
        campo_data_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_data_proposta, dados[2])
        # driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]').send_keys(lista[2])
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="Documento_PropostaCia"]').clear()
        time.sleep(1)
        campo_inic_ivg = driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_inic_ivg, dados[3])
        # time.sleep(.2)
        # driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]').send_keys(Keys.BACKSPACE)
        time.sleep(1)
        # driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]').send_keys(lista[4])
        # time.sleep(1)
        campo_term_vig = driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_term_vig, dados[4])
        # time.sleep(.2)
        # driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]').send_keys(Keys.BACKSPACE)
        # time.sleep(1)
        # driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]').send_keys(lista[5])
        time.sleep(1)
        campo_data_emissao = driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]')
        driver.execute_script("arguments[0].value = arguments[1];", campo_data_emissao, dados[5])
        # time.sleep(.2)
        # driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]').send_keys(Keys.BACKSPACE)
        time.sleep(1)
        campo_endosso.clear()
        time.sleep(.2)
        campo_endosso.send_keys(dados[1])
        time.sleep(.2)
        campo_proposta.clear()
        time.sleep(.2)
        campo_proposta.send_keys(dados[2])
        time.sleep(.2)

        botao_gravar.click()

        time.sleep(2)
        # driver.switch_to.frame("ZonaInterna")
        teste = driver.find_element(By.XPATH, '//*[@id="table_ff_sinistros"]')
        cont = 0
        while True:
            try:
                botao_premio = driver.find_element(By.XPATH, '//*[@id="icone-Premios"]')
                # actions = ActionChains(driver)
                # actions.double_click(botao_premio).perform()
                time.sleep(.2)
                botao_premio.click()
                break
            except:
                pass
            time.sleep(.2)
            if cont == 10:
                break
            cont = cont + 1
            time.sleep(.2)

        while True:
            try:
                campo_meio_pag = driver.find_element(By.XPATH, '//*[@id="DIVDocumento_MeioPagto"]/div/span/span[1]')
                time.sleep(.2)
                campo_meio_pag.click()
                time.sleep(.2)
                elemento = driver.switch_to.active_element
                time.sleep(.2)
                elemento.send_keys('Boleto Bancario')
                time.sleep(.2)
                elemento.send_keys(Keys.ARROW_DOWN)
                time.sleep(.2)
                elemento.send_keys(Keys.ENTER)
                time.sleep(.2)
                campo_vencimento = driver.find_element(By.XPATH, '//*[@id="Documento_DataVencPrimeira"]')
                time.sleep(.2)
                campo_vencimento.clear()
                time.sleep(.2)
                campo_vencimento.send_keys(dados[-1])
                time.sleep(.2)
                campo_premio_liq = driver.find_element(By.XPATH, '//*[@id="Documento_PremioLiqDesc"]')
                time.sleep(.2)
                while campo_premio_liq.get_attribute("value") != '':
                    campo_premio_liq.send_keys(Keys.BACKSPACE)
                    time.sleep(.2)

                # time.sleep(.5)
                for char in dados[6].replace('.', ''):
                    campo_premio_liq.send_keys(char)
                    time.sleep(.2)
                campo_iof = driver.find_element(By.XPATH, '//*[@id="Documento_PercIof"]')
                campo_iof.clear()
                time.sleep(.2)
                driver.execute_script("arguments[0].value = arguments[1];", campo_iof, "7,38")
                time.sleep(.2)
                campo_iof.send_keys(Keys.TAB)

                break
            except:
                time.sleep(1)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                try:
                    botao_premio = driver.find_element(By.XPATH, '//*[@id="icone-Premios"]')
                    # actions = ActionChains(driver)
                    # actions.double_click(botao_premio).perform()
                    time.sleep(.2)
                    botao_premio.click()

                except:
                    pass
            time.sleep(.2)
        botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
        botao_gravar.click()
        time.sleep(2)
        while True:
            try:
                botao_anexar = driver.find_element(By.XPATH, '//*[@id="BtAnexar"]')
                botao_anexar.click()
                break
            except:
                pass
        time.sleep(1)
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame("ScanImagem")
        time.sleep(1)
        botao_multiplos = driver.find_element(By.XPATH, '//*[@id="BtAbrirMultiplus"]')
        time.sleep(.2)
        botao_multiplos.click()
        time.sleep(1)
        driver.switch_to.frame("ScanImagem")
        time.sleep(1)
        teste = driver.find_element(By.XPATH, '//*[@id="files"]')
        time.sleep(1)
        teste.send_keys(arquivos[0])
        time.sleep(1)
        botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
        time.sleep(3)
        botao_voltar.click()


        time.sleep(5)

        arquivos = arquivos[1:]
        for arquivo in arquivos:
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            botao_incluir = driver.find_element(By.XPATH, '//*[@id="BtIncluir"]')
            botao_incluir.click()
            time.sleep(3)
            while True:
                try:
                    botao_multiplos = driver.find_element(By.XPATH, '//*[@id="BtAbrirMultiplus"]')
                    break
                except:
                    pass
            time.sleep(.2)
            botao_multiplos.click()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            time.sleep(1)
            teste = driver.find_element(By.XPATH, '//*[@id="files"]')
            teste.send_keys(arquivo)
            botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
            time.sleep(3)
            botao_voltar.click()
            time.sleep(3)
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
            time.sleep(3)

        """for arquivo in arquivos:
            time.sleep(1)
            input_upload = driver.find_element(By.XPATH, '//input[@type="file"]')
            time.sleep(.2)
            input_upload.send_keys(arquivo)
            time.sleep(3)
            try:
                os.remove(arquivo)
                print(f"O arquivo {arquivo} foi removido com sucesso.")
            except:
                print(f"O arquivo {arquivo} não foi encontrado.")"""
        time.sleep(2)
        botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
        time.sleep(3)
        botao_voltar.click()
        print('apertei o primeiro voltar')
        time.sleep(1)
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame("ScanImagem")
        time.sleep(1)
        botao_voltar2 = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
        time.sleep(.2)
        botao_voltar2.click()
        print('apertei o segundo voltar')
        time.sleep(1)
        driver.switch_to.default_content()
        time.sleep(1)
        driver.switch_to.frame("ZonaInterna")
        time.sleep(1)
        driver.switch_to.frame("ZonaInterna")
        time.sleep(1)
        driver.switch_to.frame("Documento")
        time.sleep(1)
        botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
        time.sleep(1)
        botao_gravar.click()
        print('apertei o gravar')
        time.sleep(5)

    else:
        print('Número de usuarios excedido')

    driver.quit()


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def email_baixar_pdf():

    #palavras = ['resumo', 'endosso', 'fatura']
    link = 'https://lrvseguros.com.br:2096/cpsess5607446155/3rdparty/roundcube/?_task=mail&_mbox=INBOX'
    driver.uc_open(fr'{link}')

    while True:
        try:
            campo_usuario = driver.find_element(By.ID, 'user')
            campo_senha = driver.find_element(By.ID, 'pass')
            botao_login = driver.find_element(By.ID, 'login_submit')
            break
        except:
            pass
    time.sleep(1)
    campo_usuario.send_keys('cadastrofaturatransportes@lrvseguros.com.br')
    time.sleep(1)
    campo_senha.send_keys('Cadastro@2024#')
    time.sleep(1)
    botao_login.click()

    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'button-inner')
            break
        except:
            pass

    time.sleep(2)

    emails = driver.find_elements(By.CSS_SELECTOR, ".message.unread")

    while len(emails) > 0:
        time.sleep(1)
        print(fr'Tem {len(emails)} não lidos')

        for email in emails:
            actions = ActionChains(driver)
            actions.double_click(emails[0]).perform()
            while True:
                try:
                    print('procurando o botao')
                    botao_voltar = driver.find_element(By.XPATH, '//*[@id="rcmbtn111"]')
                    break
                except:
                    pass

            while True:
                try:
                    nome = driver.find_element(By.XPATH, '//*[@id="messageheader"]/h2').text
                    break
                except:
                    pass
                time.sleep(.5)
            nome = nome.split('\n')[1]
            nome = fr'{nome}.png'
            nome = sanitize_filename(nome)
            seguradora = nome.split(' - ')[-1].split('.')[0]
            #lista_documentos.append([seguradora])
            driver.save_screenshot(nome)
            selenium_cookies = driver.get_cookies()
            cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
            lista_anexos = driver.find_elements(By.XPATH, "//ul[@id='attachment-list']/li/a")
            for anexo in lista_anexos:
                link = anexo.get_attribute('href')
                if link:
                    if True:
                        print(f"Baixando: {link}")
                        response = requests.get(link, cookies=cookies, stream=True)
                        if response.status_code == 200:
                            filename = sanitize_filename(str(anexo.text).lower().split("\n")[0])
                            inicio = filename.find('-') + 2
                            fim = filename.rfind('-')
                            print(inicio)
                            print(fim)
                            file_teste = filename[inicio:fim]
                            print(file_teste)
                            encontrado = 0
                            for documento in lista_documentos:
                                for doc in documento:
                                    print(doc)
                                    if doc.find(file_teste)>0:
                                        documento.append(filename)
                                        encontrado = 1
                                        break

                            if encontrado == 0:
                                lista_documentos.append([seguradora])
                                lista_documentos[-1].append(nome)
                                lista_documentos[-1].append(filename)
                            with open(filename, "wb") as link:
                                link.write(response.content)
                            print(f"Arguivo salvo como {filename}")
                            lista_pdfs.append(filename)
                        else:
                            print(f"Falha ao baixar {link}: {response.status_code}")


            botao_voltar.click()
            time.sleep(2)
            emails = driver.find_elements(By.CSS_SELECTOR, ".message.unread")

    while True:
        try:
            botao_selecionar = driver.find_element(By.XPATH, '//*[@id="listselectmenulink"]')
            botao_selecionar.click()
            break
        except:
            pass
        time.sleep(.2)
    while True:
        try:
            botao_todas = driver.find_element(By.XPATH, '//*[@id="rcmbtn144"]')
            botao_todas.click()
            break
        except:
            pass
        time.sleep(.2)
    while True:
        try:
            botao_mais = driver.find_element(By.XPATH, '//*[@id="messagemenulink"]')
            botao_mais.click()
            break
        except:
            pass
        time.sleep(.2)
    while True:
        try:
            botao_mover = driver.find_element(By.XPATH, '//*[@id="rcmbtn126"]')
            botao_mover.click()
            break
        except:
            pass
        time.sleep(.2)
    while True:
        try:
            botao_arquivo = driver.find_element(By.XPATH, '//*[@id="folder-selector"]/ul/li[6]')
            botao_arquivo.click()
            break
        except:
            pass
        time.sleep(.2)


def ler_pdf_completo(nome_arquivo):

    with open(nome_arquivo, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        texto_completo = ""

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            texto_completo += page.extract_text()


    return texto_completo

def sompo(texto):
    dados = []
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Apólice' in linha:
            apolice = texto[cont + 1]
            dados.append(apolice)
            print(apolice)
            break
        cont = cont + 1
    inicio = texto[cont + 2].find('/') + 5
    fim = texto[cont + 2].find('CONTA')
    fatura = texto[cont + 2][inicio:fim]
    dados.append(fatura)
    print(fatura)
    data = texto[cont + 2][:inicio]
    mes, ano = map(int, data.split("/"))
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    data_proposta = fr'01/{data}'
    inicio_vig = data_proposta
    fim_vig = fr'{ultimo_dia}/{data}'
    dados.append(data_proposta)
    dados.append(inicio_vig)
    dados.append(fim_vig)

    print(data_proposta + '\n' + inicio_vig + '\n' + fim_vig)
    cont = 0
    for linha in texto:
        if 'Local e Data' in linha:
            data = texto[cont - 2]
            print(data)
            inicio = data.find(',') + 2
            data = data[inicio:]
            #data = data.split(' ')[0]
            partes = data.split(" de ")
            dia = partes[0].split(' ')[-1]
            mes = meses[partes[1].lower()]  # Converter o mês para minúsculo para evitar problemas
            ano = partes[2]
            data_emissao = f"{dia}/{mes}/{ano}"
            dados.append(data_emissao)
            print(data_emissao)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'PRÊMIO LÍQUIDO' in linha:
            premio_liquido = texto[cont + 3].split(' ')[1]
            ramo = texto[cont + 1]
            print(ramo)
            fim = premio_liquido.find(',') + 3
            premio_liquido = premio_liquido[:fim].replace('.', '')
            print(premio_liquido)
            dados.append(premio_liquido)
            break
        cont = cont + 1

    premio_bruto = texto[cont + 3].split(' ')[0]
    print(premio_bruto)
    cont = 0
    for linha in texto:
        if 'LIMITE PAGTO' in linha:
            data_limite = texto[cont + 1]
            fim = data_limite.find('/') + 8
            data_limite = data_limite[:fim]
            print(data_limite)
            dados.append(data_limite)
            break
        cont = cont + 1

    print(dados)
    return dados




def fairfax(texto):
    dados = []
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Ramo :' in linha:
            ramo = texto[cont]
            ramo = ramo.split('-')[-1]
            print(ramo)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Apólice Nº :' in linha:
            apolice = texto[cont]
            apolice = apolice.split(':')[-1].replace(' ', '')
            print(apolice)
            dados.append(apolice)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Endosso Nº:' in linha:
            endosso = texto[cont]
            endosso = endosso.split(':')[-1].replace(' ', '')
            print(endosso)
            dados.append(endosso)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Proposta Nº' in linha:
            fatura = texto[cont]
            fatura = fatura.split(':')[-1].replace(' ', '')
            print(fatura)
            dados.append(fatura)
            break
        cont = cont + 1





    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            inicio_vig = texto[cont]
            inicio = inicio_vig.find('dia') + 4
            inicio_vigencia = inicio_vig[inicio:inicio + 10]
            inicio_vig = inicio_vig[inicio:]
            inicio = inicio_vig.find('dia') + 4
            fim_vigencia = inicio_vig[inicio:inicio + 10]
            # inicio_vigencia = emissao.split(' ')[0]
            print(inicio_vigencia)
            print(fim_vigencia)
            dados.append(inicio_vigencia)
            dados.append(inicio_vigencia)
            dados.append(fim_vigencia)

            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            emissao = texto[cont]
            emissao = emissao.split(' ')[0]
            print(emissao)
            dados.append(emissao)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Prêmio Líquido' in linha:
            premio = texto[cont + 1][5:]
            inicio = premio.find('R$') + 3
            premio = premio[inicio:]
            fim = premio.find('R$') - 1
            premio_liquido = premio[:fim]
            inicio = premio.rfind('R$') + 3
            premio_bruto = premio[inicio:]
            print(premio_liquido)
            print(premio_bruto)
            dados.append(premio_liquido)

            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'VENC.' in linha:
            vencimento = texto[cont + 1].rstrip()
            vencimento = vencimento.split(' ')[-1]
            print(vencimento)
            dados.append(vencimento)
            break
        cont = cont + 1
    print(dados)
    return dados


def sura(texto):
    dados = []
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Ramo:' in linha:
            ramo = texto[cont]
            ramo = ramo.split(' ')[-1]
            print(ramo)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Apólice:' in linha:
            apolice = texto[cont]
            apolice = apolice.split(' ')[1]
            print(apolice)
            dados.append(apolice)
            break
        cont = cont + 1


    cont = 0
    for linha in texto:
        if 'Fatura:' in linha:
            fat = texto[cont]
            fatura = fat.split(' ')[1]
            data = fat.split(' ')[2]
            vencimento = fat.split(' ')[3]
            print(fatura)
            dados.append(fatura)
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            primeiro_dia = f"01/{mes}/{ano}"
            ultimo_dia_formatado = f"{ultimo_dia}/{mes}/{ano}"
            data_proposta = primeiro_dia
            dados.append(data_proposta)
            inicio_vig = primeiro_dia
            dados.append(inicio_vig)
            fim_vig = ultimo_dia_formatado
            dados.append(fim_vig)
            data_emissao = primeiro_dia
            dados.append(data_emissao)
            print(vencimento)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Demonstrativo do Prêmio em R$' in linha:
            premio_liquido = texto[cont + 1].rstrip()
            #print(premio_liquido)
            premio_liquido = premio_liquido.split(' ')[-1]

            print(premio_liquido)
            dados.append(premio_liquido)
            break
        cont = cont + 1
    dados.append(vencimento)
    cont = 0
    for linha in texto:
        if 'Total a Pagar' in linha:
            premio_bruto = texto[cont].rstrip()
            premio_bruto = premio_bruto.split(' ')[-1]

            print(premio_bruto)
            break
        cont = cont + 1
    print(dados)
    dados = [apolice, fatura, data_proposta, inicio_vig, fim_vig, data_emissao, premio_liquido, vencimento]
    return dados

def berkley(texto):
    dados = []
    texto =  texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Ramo' in linha:
            ramo = texto[cont + 1][3:].rstrip().split(' ')[1]
            proposta = texto[cont + 1][3:].rstrip().split(' ')[3]
            print(ramo)
            print(proposta)
            break
        cont = cont + 1

    apolice = texto[2].split(' ')[4]
    endosso = texto[2].split(' ')[5]
    emissao = texto[2].split(' ')[-1]
    print(emissao)
    cont = 0
    for linha in texto:
        if 'VIGÊNCIA' in linha:
            inicio_vig = ''
            fim_vig = ''
            vig = texto[cont + 1].split(' ')
            for v in vig:
                if '/' in v:
                    if inicio_vig == '':
                        inicio_vig = v
                    else:
                        fim_vig = v
            print(inicio_vig)
            print(fim_vig)
            break
        cont = cont + 1
    dados.append(inicio_vig)
    dados.append(inicio_vig)
    dados.append(fim_vig)
    dados.append(emissao)
    for linha in texto:
        if 'Prêmio Líquido:' in linha:
            premio_liquido = linha.split(' ')[-1]
            print(premio_liquido)
            dados.append(premio_liquido)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Prêmio Total:' in linha:
            premio_total = linha.split(' ')[-1]
            print(premio_total)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Vencimentos:' in linha:
            vencimento = linha.split(' ')[-1]
            print(vencimento)
            dados.append(vencimento)
            break

    print(dados)
    return dados

def axa(texto):
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Nomenclatura de Ramo e Produto' in linha:
            ramo = texto[cont + 1].split(' ')[-1]
            print(ramo)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Nº pedido de endosso' in linha:
            endosso = ''
            end = texto[cont + 1].split(' ')[0]
            for char in end:
                if char.isdigit():
                    endosso = endosso + char
            print(endosso)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Início de Vigência:' in linha:
            end = texto[cont + 1].split(' ')
            for e in end:
                if '/' in e:
                    inicio_vigencia = e[:10]
            print(inicio_vigencia)
            end = texto[cont + 2].split(' ')
            for e in end:
                if '/' in e:
                    fim_vigencia = e[:10]
            print(fim_vigencia)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data da Emissão' in linha:
            end = texto[cont + 1].find('Número da apólice')
            emissao = texto[cont + 1][:end]
            if 'de' in emissao:
                partes = emissao.split(" de ")
                dia = partes[0].split(' ')[-1]
                mes = meses[partes[1].lower()]  # Converter o mês para minúsculo para evitar problemas
                ano = partes[2]
                emissao = f"{dia}/{mes}/{ano}"

            print(emissao)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Nº Apólice averbação' in linha:
            end = texto[cont].find('Nº Apólice averbação')
            apolice = texto[cont][:end]
            print(apolice)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Prêmio Líquido' in linha:
            premio_liquido = texto[cont].split(' ')[-1]
            print(premio_liquido)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Prêmio Total' in linha:
            premio_bruto = texto[cont].split(' ')[-1]
            print(premio_bruto)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Vencimento:' in linha:
            vencimento = texto[cont + 1].split(' ')[1]
            print(vencimento)
            break
        cont = cont + 1
    dados = []
    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados

def aig(texto):
    texto = texto.split('\n')
    cont = 0

    for linha in texto:
        if 'Nº Apólice' in linha:
            apolice = texto[cont + 1].split('Nº Endosso')[0]
            endosso = texto[cont + 2].split()[0]
            print(apolice)
            print(endosso)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Vigência' in linha:
            inicio_vigencia = texto[cont + 1].split()[5]
            fim_vigencia = texto[cont + 1].split()[-1]
            print(inicio_vigencia)
            print(fim_vigencia)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data de Emissão' in linha:
            emissao = texto[cont + 1].split()[0].replace(' ', '')
            print(emissao)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Total' in linha:
            premio_liquido = texto[cont + 1].split()[-1].replace('.', '')
            print(premio_liquido)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Valor' in linha:
            vencimento = texto[cont + 1].split()[0].replace(' ', '')
            print(vencimento)
            break
        cont = cont + 1
    dados = []
    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados



def axa_b(texto):
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Endosso:' in linha:
            endosso = texto[cont+1]
            print(endosso)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Endosso:' in linha:
            vig = linha.split(' ')
            for v in vig:
                if '/' in v:
                    inicio_vigencia = v
                    break
            for v in vig:
                if '/' in v and 'Fim' in v:
                    fim = v.find('Fim')
                    fim_vigencia = v[:fim]
                    break

            try:
                print(inicio_vigencia)
                print(fim_vigencia)
            except:
                pass
            break
        cont = cont + 1

    cont = 0
    emissao = texto[0]
    partes = emissao.split(" ")
    dia = partes[0]
    mes = meses[partes[1].lower()]
    ano = partes[2]
    emissao = f"{dia}/{mes}/{ano}"
    print(emissao)

    cont = 0
    for linha in texto:
        if 'www.axa.com.brOuvidoriaApólice' in linha:
            apolice = texto[cont + 1]
            print(apolice)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Pagamento:Moeda: R$' in linha:
            premio_liquido = texto[cont].split(' ')[-2]
            premio_liquido.replace('.', '')
            print(premio_liquido)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'PRÊMIO TOTAL' in linha:
            venc = texto[cont + 1].split(' ')
            for v in venc:
                if '/' in v:
                    vencimento = v
                    break
            print(vencimento)
            break
        cont = cont + 1
    dados = []
    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados


def swiss(texto):
    dados = []
    texto = texto.split('\n')

    # Buscando o ramo (não usado no preenchimento, mas mantido para debug)
    cont = 0
    for linha in texto:
        if 'Nº da Proposta:' in linha:
            ramo = ''
            ram = ''
            teste = texto[cont + 1] + ' ' + texto[cont + 2]
            for t in teste.split(' '):
                if t[0].isalpha():
                    ram = ram + t[0]
            for r in ram:
                if r.isupper():
                    ramo = ramo + r
            print(ramo)
            break
        cont = cont + 1

    # Buscando número da apólice, endosso e proposta
    cont = 0
    for linha in texto:
        if 'Carga' in linha:
            apolice = texto[cont + 1].strip()
            endosso = texto[cont + 2].strip()
            # Mantido para referência, mas não usado
            n_proposta = texto[cont + 3].strip()
            dados.append(apolice)  # dados[0] - N° apólice coletiva
            dados.append(endosso)  # dados[1] - N° endosso
            break
        cont = cont + 1

    # Buscando datas de vigência e emissão
    cont = 0
    for linha in texto:
        if 'Modalidade:' in linha:
            emissao = texto[cont + 2].split(' ')[0].strip()
            vigencia = texto[cont + 4].split('.')[0].strip()
            print(emissao)
            print(vigencia)

            # Processando a data de vigência
            data = vigencia
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            primeiro_dia = f"01/{mes}/{ano}"
            ultimo_dia_formatado = f"{ultimo_dia}/{mes}/{ano}"

            # Adicionando as datas na ordem correta
            # dados[2] - Data da proposta (usando data de emissão)
            dados.append(emissao)
            dados.append(primeiro_dia)  # dados[3] - Data inicial vigência
            # dados[4] - Data inicial vigência (duplicada)
            dados.append(primeiro_dia)
            # dados[5] - Data final vigência
            dados.append(ultimo_dia_formatado)
            dados.append(emissao)  # dados[6] - Data emissão
            break
        cont = cont + 1

    # Buscando prêmio líquido
    cont = 0
    for linha in texto:
        if 'Prêmio Total (R$):' in linha:
            premio_liquido = texto[cont + 1].split(' ')[-1].strip()
            premio_bruto = texto[cont + 5].split(' ')[-1].strip()
            print(premio_liquido)
            dados.append(premio_liquido)  # dados[7] - Prêmio líquido
            print(premio_bruto)
            break
        cont = cont + 1

    # Buscando data de vencimento
    cont = 0
    for linha in texto:
        if 'CONDIÇÕES GERAIS' in linha:
            vencimento = texto[cont - 1].strip()
            print(vencimento)
            dados.append(vencimento)  # dados[8] - Data vencimento
            break
        cont = cont + 1

    print(dados)

    return dados

listaFeitos = []

if os.path.exists(nome_arquivo):
    # Carregar os links já feitos para a listaFeitos
    with open(nome_arquivo, "r") as arquivo:
        listaFeitos = [linha.strip() for linha in arquivo.readlines()]
else:
    # Criar o arquivo vazio
    with open(nome_arquivo, "w") as arquivo:
        pass


driver = Driver(uc=True, headless=False)
driver.maximize_window()

email_baixar_pdf()
driver.quit()

if len(lista_documentos) > 0:

    for documento in lista_documentos:
        caminho = ''
        encontrado = 0
        for doc in documento:
            if doc.find('ndosso') > 0 and doc.find('pdf') > 0:
                caminho = doc
                print(caminho)
                encontrado = 1
                break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('esumo') > 0 and doc.find('pdf') > 0:
                        caminho = doc
                        print(caminho)
                        encontrado = 1
                        break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('atura') > 0 and doc.find('pdf') > 0:
                        print(caminho)
                        caminho = doc
                        encontrado = 1
                        break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('elação') > 0 and doc.find('pdf') > 0:
                        print(caminho)
                        caminho = doc
                        encontrado = 1
                        break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('oleto') == 0 and doc.find('pdf') > 0:
                        print(caminho)
                        caminho = doc
                        encontrado = 1
                        break
        if caminho != '' and caminho not in listaFeitos:
            print(fr'Fazendo o documento {caminho}')
            texto = ''
            while len(texto) < 100:
                texto = ler_pdf_completo(caminho)
                print(texto)
            teste = str(documento[0]).lower()
            if teste.find('wiss') > 0:
                try:
                    dados = swiss(texto)
                    quiver1(dados, documento)
                    listaFeitos.append(caminho)

                except Exception as e:
                    print(e)
                with open(nome_arquivo, "a") as arquivo:
                    with open(nome_arquivo, "a") as arquivo:
                        data_atual = datetime.now()
                        data_formatada = data_atual.strftime("%d/%m/%Y")
                        if dados:
                            arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")
            elif teste.find('airfax') > 0:
                try:
                    dados = fairfax(texto)
                    quiver1(dados, documento)
                    listaFeitos.append(caminho)

                except Exception as e:
                    print(e)
                with open(nome_arquivo, "a") as arquivo:
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%d/%m/%Y")
                    if dados:
                        arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")
            elif teste.find('ura') > 0:
                try:
                    dados = sura(texto)
                    quiver2(dados, documento)
                    listaFeitos.append(caminho)

                except Exception as e:
                    print(e)
                with open(nome_arquivo, "a") as arquivo:
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%d/%m/%Y")
                    if dados:
                        arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")
            elif teste.find('ompo') > 0:
                try:
                    dados = sompo(texto)
                    quiver2(dados, documento)
                    listaFeitos.append(caminho)

                except Exception as e:
                    print(e)
                with open(nome_arquivo, "a") as arquivo:
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%d/%m/%Y")
                    if dados:
                        arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")
            elif teste.find('xa') > 0:
                try:
                    dados = None  # Inicializa a variável dados
                    try:
                        dados = axa(texto)
                    except:
                        dados = axa_b(texto)

                    if dados:  # Verifica se dados foi preenchido com sucesso
                        quiver2(dados, documento)
                        listaFeitos.append(caminho)

                except Exception as e:
                    print(e)

                with open(nome_arquivo, "a") as arquivo:
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%d/%m/%Y")
                    if dados:  # Só escreve no arquivo se dados existir
                        arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")
            elif teste.find('ig') > 0:
                try:
                    try:
                        dados = aig(texto)
                        quiver2(dados, documento)
                        listaFeitos.append(caminho)
                    except:
                        pass


                except Exception as e:
                    print(e)
                with open(nome_arquivo, "a") as arquivo:
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%d/%m/%Y")
                    if dados:
                        arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")
            elif teste.find('erkley') > 0:
                try:
                    dados = berkley(texto)
                    quiver1(dados, documento)
                    listaFeitos.append(caminho)

                except Exception as e:
                    print(e)
                with open(nome_arquivo, "a") as arquivo:
                    data_atual = datetime.now()
                    data_formatada = data_atual.strftime("%d/%m/%Y")
                    if dados:
                        arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")


for documento in lista_documentos:
    for doc in documento:
        try:
            os.remove(doc)
            print(f"O arquivo {doc} foi removido com sucesso.")
        except:
            print(f"O arquivo {doc} não foi localizado para remoção")
