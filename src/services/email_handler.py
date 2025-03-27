"""
Módulo para manipulação de e-mails do Bot de Faturas

Este módulo contém funções para acessar a caixa de e-mails da empresa,
baixar anexos e organizá-los para processamento posterior.

Autor: Lucelho Silva
"""
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from src.config.settings import EMAIL
from src.utils.utils import sanitize_filename
from src.utils.logging_config import setup_logging

logger = setup_logging()

def baixar_emails(driver, lista_documentos, lista_pdfs):
    """
    Acessa o e-mail da empresa, baixa anexos e os organiza para processamento.

    Args:
        driver: Instância do webdriver Selenium
        lista_documentos: Lista onde serão armazenados os documentos por seguradora
        lista_pdfs: Lista onde serão armazenados os caminhos de PDFs baixados

    Returns:
        tuple: Listas atualizadas com os documentos e PDFs
    """

    # Acessar a página de login do webmail
    link = EMAIL['url']
    driver.uc_open(fr'{link}')

    # Aguardar carregamento da página de login
    while True:
        try:
            campo_usuario = driver.find_element(By.ID, 'user')
            campo_senha = driver.find_element(By.ID, 'pass')
            botao_login = driver.find_element(By.ID, 'login_submit')
            break
        except:
            pass

    # Preencher credenciais e fazer login
    time.sleep(1)
    campo_usuario.send_keys(EMAIL['usuario'])
    time.sleep(1)
    campo_senha.send_keys(EMAIL['senha'])
    time.sleep(1)
    botao_login.click()

    # Aguardar carregamento da caixa de entrada
    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'button-inner')
            break
        except:
            pass

    time.sleep(2)

    # Obter e-mails não lidos
    emails = driver.find_elements(By.CSS_SELECTOR, ".message.unread")

    # Processar cada e-mail não lido
    while len(emails) > 0:
        time.sleep(1)
        logger.info(f'Encontrados {len(emails)} e-mails não lidos')

        for email in emails:
            # Abrir o e-mail
            actions = ActionChains(driver)
            actions.double_click(emails[0]).perform()

            # Aguardar carregamento completo do e-mail
            while True:
                try:
                    logger.debug('Procurando botão de voltar')
                    botao_voltar = driver.find_element(By.XPATH, '//*[@id="rcmbtn111"]')
                    break
                except:
                    pass

            # Extrair assunto do e-mail
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

            # Capturar screenshot do e-mail
            driver.save_screenshot(nome)

            # Obter cookies da sessão para download de anexos
            selenium_cookies = driver.get_cookies()
            cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

            # Baixar anexos do e-mail
            lista_anexos = driver.find_elements(By.XPATH, "//ul[@id='attachment-list']/li/a")
            for anexo in lista_anexos:
                link = anexo.get_attribute('href')
                if link:
                    if True:    # Sempre processa - pode ser modificado para filtrar tipos específicos
                        logger.info(f"Baixando anexo: {link}")
                        response = requests.get(link, cookies=cookies, stream=True)
                        if response.status_code == 200:
                            # Sanitizar e formatar nome do arquivo
                            filename = sanitize_filename(str(anexo.text).lower().split("\n")[0])
                            inicio = filename.find('-') + 2
                            fim = filename.rfind('-')
                            file_teste = filename[inicio:fim]

                            # Organizar documentos por seguradora
                            encontrado = 0
                            for documento in lista_documentos:
                                for doc in documento:
                                    if doc.find(file_teste)>0:
                                        documento.append(filename)
                                        encontrado = 1
                                        break

                            # Se não encontrou grupo existente, criar novo para a seguradora
                            if encontrado == 0:
                                lista_documentos.append([seguradora])
                                lista_documentos[-1].append(nome)
                                lista_documentos[-1].append(filename)

                            # Salvar o arquivo
                            with open(filename, "wb") as link:
                                link.write(response.content)
                            logger.info(f"Arquivo salvo como: {filename}")
                            lista_pdfs.append(filename)
                        else:
                            logger.error(f"Falha ao baixar {link}: {response.status_code}")

            # Voltar para a lista de e-mails
            botao_voltar.click()
            time.sleep(2)
            emails = driver.find_elements(By.CSS_SELECTOR, ".message.unread")

    # Arquivar emails processados
    _arquivar_emails(driver)

    return lista_documentos, lista_pdfs

def _arquivar_emails(driver):
    """
    Arquiva todos os emails abertos após processamento para manter a caixa organizada.

    Args:
        driver: Instância do webdriver Selenium
    """

    # Selecionar todos os e-mails
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

    # Acessar menu de mais opções
    while True:
        try:
            botao_mais = driver.find_element(By.XPATH, '//*[@id="messagemenulink"]')
            botao_mais.click()
            break
        except:
            pass
        time.sleep(.2)

    # Selecionar opção de mover e-mails
    while True:
        try:
            botao_mover = driver.find_element(By.XPATH, '//*[@id="rcmbtn126"]')
            botao_mover.click()
            break
        except:
            pass
        time.sleep(.2)

    # Selecionar pasta de arquivos
    while True:
        try:
            botao_arquivo = driver.find_element(By.XPATH, '//*[@id="folder-selector"]/ul/li[6]')
            botao_arquivo.click()
            break
        except:
            pass
        time.sleep(.2)

    logger.info("E-mails arquivados com sucesso")