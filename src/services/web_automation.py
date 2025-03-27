import os
import time
import threading
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from src.config.settings import CORRETOR_ONLINE, CORRETOR_URL
from src.utils.logging_config import setup_logging
from src.utils.utils import registrar_error

# Configurações
MAX_TIMEOUT = 300  # Timeout máximo em segundos (3 minutos)
ERROR_LOG_FILE = "error_log.txt"  # Arquivo central para registro de erros

logger = setup_logging()

class TimeoutError(Exception):
    """Erro para indicar que uma operação excedeu o tempo limite"""
    pass

def timeout_handler():
    """Função que será chamada quando o timeout for atingido"""
    raise TimeoutError("Operação excedeu o tempo limite")

def quiver(dados, arquivos, tipo_seguradora=1):
    """
    Função unificada para automatização do preenchimento no sistema com timeout.

    Args:
        dados: Lista com os dados extraídos do PDF
        arquivos: Lista com os caminhos dos arquivos a serem anexados
        tipo_seguradora: 1 para Swiss, Fairfax, Berkley; 2 para Sura, Sompo, AXA, AIG
    """
    diretorio_corrente = os.getcwd()
    arquivos = [os.path.join(diretorio_corrente, nome) for nome in arquivos[1:]]
    driver = None

    # Extrair informações para o log de erros
    apolice = dados[0] if dados and len(dados) > 0 else "N/A"
    endosso = dados[1] if dados and len(dados) > 1 else "N/A"
    nome = dados[-1] if dados and len(dados) > 8 else None
    seguradora = arquivos[0].split('/')[-1].split(' - ')[-1].split('.')[0] if arquivos else "N/A"

    # Timer para timeout
    timer = threading.Timer(MAX_TIMEOUT, timeout_handler)

    try:
        timer.start()
        driver = webdriver.Chrome()
        driver.maximize_window()
        link = CORRETOR_URL

        # Login no sistema
        while True:
            driver.get(link)
            corretora = CORRETOR_ONLINE['corretora']
            login = CORRETOR_ONLINE['login']
            senha = CORRETOR_ONLINE['senha']
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
                except Exception as e:
                    if timer.is_alive():
                        continue
                    else:
                        raise TimeoutError("Tempo excedido durante login")
            break

        # Navegação para a área operacional
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
                        if not timer.is_alive():
                            raise TimeoutError("Tempo excedido durante navegação")

                time.sleep(2)
                driver.switch_to.default_content()
                time.sleep(.2)
                botao_operacional.click()
                break
            except Exception as e:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido durante navegação para área operacional")

        time.sleep(3)
        # Verificação de excedência de usuários
        if len(driver.find_elements(By.XPATH, '/html/body/div[3]/div')) == 0:
            logger.info('Iniciando processo de automação')

            # Alternar para o frame interno
            while True:
                try:
                    driver.switch_to.frame("ZonaInterna")
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao alternar para o frame")

            # Clicar em propostas
            botao_propostas = driver.find_element(By.XPATH,
                                                '//*[@id="card-conteudo-dados-OPERACIONAL_PRINCIPAL"]/ul/li[2]/div[1]/a')
            botao_propostas.click()

            # Selecionar "Nº da apólice" no dropdown
            while True:
                try:
                    dropbox_fatura = driver.find_element(By.XPATH,
                                                        '//*[@id="DIVTipoConsulta2"]/div/span/span[1]/span/span[2]')
                    dropbox_fatura.click()
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao selecionar dropdown")

            time.sleep(1)
            elemento = driver.switch_to.active_element
            time.sleep(.2)
            elemento.send_keys('Nº da apólice')
            time.sleep(.2)
            elemento.send_keys(Keys.ARROW_DOWN)
            time.sleep(.2)
            elemento.send_keys(Keys.ENTER)
            time.sleep(.2)

            # Preencher o número da apólice
            while True:
                try:
                    campo_apolice = driver.find_element(By.XPATH, '//*[@id="NoApolice"]')
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao localizar campo de apólice")

            campo_apolice.send_keys(dados[0])
            time.sleep(.2)
            campo_apolice.send_keys(Keys.ENTER)
            time.sleep(2)

            # Editar o registro
            while True:
                try:
                    elemento = driver.find_element(By.XPATH, '//*[@id="BtEdiReg"]')
                    driver.execute_script(
                        "var evt = new MouseEvent('dblclick', {bubbles: true, cancelable: true, view: window}); arguments[0].dispatchEvent(evt);",
                        elemento)
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao editar registro")

            time.sleep(2)
            driver.switch_to.frame("ZonaInterna")

            # Adicionar novo endosso
            while True:
                try:
                    botao_plus = driver.find_element(By.XPATH, '//*[@id="trNovoEndosso"]/div[2]/div[1]/i')
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao localizar botão de novo endosso")

            botao_plus.click()

            # Preencher o número do endosso
            while True:
                try:
                    driver.switch_to.frame('Documento')
                    time.sleep(1)
                    campo_endosso = driver.find_element(By.XPATH, '//*[@id="Documento_Endosso"]')
                    campo_endosso.send_keys(dados[1])
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao preencher número do endosso")

            # Selecionar tipo de documento como "FATURA"
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
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao selecionar tipo de documento")

            # Selecionar subtipo "Averbação"
            try:
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
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao selecionar subtipo")

            # Encontrar campos do formulário
            try:
                campo_inicio_vigencia = driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]')
                campo_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_PropostaCia"]')
                campo_fim_vigencia = driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]')
                campo_data_emissao = driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]')
                campo_data_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]')
                botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao localizar campos do formulário")

            # Definir índices com base no tipo de seguradora
            inicio_vigencia_idx = 4 if tipo_seguradora == 1 else 3
            fim_vigencia_idx = 5 if tipo_seguradora == 1 else 4
            data_emissao_idx = 6 if tipo_seguradora == 1 else 5
            premio_idx = 7 if tipo_seguradora == 1 else 6

            # Preencher campos do formulário
            try:
                time.sleep(.2)
                campo_data_proposta = driver.find_element(By.XPATH, '//*[@id="Documento_DataProposta"]')
                driver.execute_script("arguments[0].value = arguments[1];", campo_data_proposta, dados[2])
                time.sleep(1)

                driver.find_element(By.XPATH, '//*[@id="Documento_PropostaCia"]').clear()
                time.sleep(1)

                campo_inic_ivg = driver.find_element(By.XPATH, '//*[@id="Documento_InicioVigencia"]')
                driver.execute_script("arguments[0].value = arguments[1];", campo_inic_ivg, dados[inicio_vigencia_idx])
                time.sleep(1)

                campo_term_vig = driver.find_element(By.XPATH, '//*[@id="Documento_TerminoVigencia"]')
                driver.execute_script("arguments[0].value = arguments[1];", campo_term_vig, dados[fim_vigencia_idx])
                time.sleep(1)

                campo_data_emissao = driver.find_element(By.XPATH, '//*[@id="Documento_DataEmissao"]')
                driver.execute_script("arguments[0].value = arguments[1];", campo_data_emissao, dados[data_emissao_idx])
                time.sleep(1)

                campo_endosso.clear()
                time.sleep(.2)
                campo_endosso.send_keys(dados[1])
                time.sleep(.2)

                campo_proposta.clear()
                time.sleep(.2)
                campo_proposta.send_keys(dados[2])
                time.sleep(.2)
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao preencher campos do formulário")

            # Gravar as alterações
            botao_gravar.click()
            time.sleep(2)

            # Acessar a seção de prêmios
            try:
                teste = driver.find_element(By.XPATH, '//*[@id="table_ff_sinistros"]')
                cont = 0
                while True:
                    try:
                        botao_premio = driver.find_element(By.XPATH, '//*[@id="icone-Premios"]')
                        time.sleep(.2)
                        botao_premio.click()
                        break
                    except:
                        pass
                    time.sleep(.2)
                    if cont == 10 or not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao acessar seção de prêmios")
                    cont = cont + 1
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao localizar tabela de sinistros")

            # Preencher informações de pagamento
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

                    # Preencher o prêmio líquido
                    for char in dados[premio_idx].replace('.', ''):
                        campo_premio_liq.send_keys(char)
                        time.sleep(.2)

                    campo_iof = driver.find_element(By.XPATH, '//*[@id="Documento_PercIof"]')
                    campo_iof.clear()
                    time.sleep(.2)
                    driver.execute_script("arguments[0].value = arguments[1];", campo_iof, "7,38")
                    time.sleep(.2)
                    campo_iof.send_keys(Keys.TAB)
                    time.sleep(.2)
                    break
                except:
                    time.sleep(1)
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                    try:
                        botao_premio = driver.find_element(By.XPATH, '//*[@id="icone-Premios"]')
                        botao_premio.click()
                    except:
                        pass

                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao preencher informações de pagamento")

            # Gravar as alterações
            try:
                botao_gravar = driver.find_element(By.XPATH, '//*[@id="BtGravar"]')
                botao_gravar.click()
                time.sleep(2)
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao gravar alterações")

            # Anexar documentos
            while True:
                try:
                    botao_anexar = driver.find_element(By.XPATH, '//*[@id="BtAnexar"]')
                    botao_anexar.click()
                    break
                except:
                    if not timer.is_alive():
                        raise TimeoutError("Tempo excedido ao clicar em anexar")

            time.sleep(1)
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame("ScanImagem")
            time.sleep(1)

            try:
                botao_multiplos = driver.find_element(By.XPATH, '//*[@id="BtAbrirMultiplus"]')
                time.sleep(.2)
                botao_multiplos.click()
                time.sleep(1)
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao clicar em múltiplos")

            driver.switch_to.frame("ScanImagem")
            time.sleep(1)

            try:
                teste = driver.find_element(By.XPATH, '//*[@id="files"]')
                time.sleep(1)
                teste.send_keys(arquivos[0])
                time.sleep(1)
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao anexar arquivo")

            try:
                botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
                time.sleep(3)
                botao_voltar.click()
                time.sleep(5)
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao voltar")

            # Anexar arquivos adicionais
            arquivos = arquivos[1:]
            for arquivo in arquivos:
                try:
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
                            if not timer.is_alive():
                                raise TimeoutError("Tempo excedido ao localizar botão múltiplos")

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
                except:
                    if not timer.is_alive():
                        raise TimeoutError(f"Tempo excedido ao anexar arquivo adicional: {arquivo}")

            # Finalizar o processo
            try:
                time.sleep(2)
                botao_voltar = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
                time.sleep(3)
                botao_voltar.click()
                logger.info('Botão voltar #1 acionado')

                time.sleep(1)
                driver.switch_to.default_content()
                time.sleep(1)
                driver.switch_to.frame("ScanImagem")
                time.sleep(1)

                botao_voltar2 = driver.find_element(By.XPATH, '//*[@id="BtVoltar"]')
                time.sleep(.2)
                botao_voltar2.click()
                logger.info('Botão voltar #2 acionado')

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
                logger.info('Dados gravados com sucesso')
                time.sleep(5)
            except:
                if not timer.is_alive():
                    raise TimeoutError("Tempo excedido ao finalizar processo")

        else:
            logger.warning('Número de usuários excedido')
            registrar_error(ERROR_LOG_FILE, seguradora, apolice, endosso, nome, "Número de usuários excedido")

    except TimeoutError as e:
        logger.error(f"Timeout em operação: {str(e)}")
        registrar_error(ERROR_LOG_FILE, seguradora, apolice, endosso, nome, f"Timeout: {str(e)}")
    except Exception as e:
        logger.error(f"Erro durante o processamento: {str(e)}", exc_info=True)
        registrar_error(ERROR_LOG_FILE, seguradora, apolice, endosso, nome, f"Erro: {str(e)}")
    finally:
        # Cancelar o timer se ainda estiver ativo
        if timer.is_alive():
            timer.cancel()

        # Fechar o navegador
        if driver:
            try:
                driver.quit()
            except:
                pass