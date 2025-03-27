"""
Módulo de notificação de erros via WhatsApp

Este módulo contém funções para enviar notificações de erro via WhatsApp
para os administradores do sistema.

Autor: Lucelho Silva
"""
import os
import re
from urllib.parse import quote
from time import sleep
from datetime import datetime
from selenium import webdriver
from src.config.settings import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do Selenium
def configurar_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    for path in CHORME_PATHS:
        if os.path.exists(path):
            chrome_options.binary_location = path
            break

    # Define um caminho específico para o profile para evitar problemas
    user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_user_data")
    os.makedirs(user_dir, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={user_dir}")

    return chrome_options

def ler_arquivo_erros(error_log_file):
    """
    Lê o arquivo de log de erros e extrai as informações relevantes.

    Args:
        error_log_file: Caminho para o arquivo de log de erros

    Returns:
        Uma lista de dicionários, cada um contendo informações de um erro
    """
    if not os.path.exists(error_log_file):
        print(f"Arquivo de log de erros não encontrado: {error_log_file}")
        return []

    with open(error_log_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Dividir o conteúdo do arquivo por registros (cada linha é um registro)
    lines = content.strip().split('\n')
    erros = []

    for line in lines:
        erro = {}

        # Extrair a data/hora
        date_match = re.search(r'\[(.*?)\]', line)
        if date_match:
            erro['data_hora'] = date_match.group(1)

        # Extrair o nome se presente
        nome_match = re.search(r'Nome: (.*?) -', line)
        if nome_match:
            erro['nome'] = nome_match.group(1)
        else:
            erro['nome'] = "Não informado"

        # Extrair a seguradora
        seguradora_match = re.search(r'Seguradora: (.*?) -', line)
        if seguradora_match:
            erro['seguradora'] = seguradora_match.group(1)
        else:
            erro['seguradora'] = "Não informada"

        # Extrair a apólice
        apolice_match = re.search(r'Apolice: (.*?) -', line)
        if apolice_match:
            erro['apolice'] = apolice_match.group(1)
        else:
            erro['apolice'] = "Não informada"

        # Extrair o endosso
        endosso_match = re.search(r'Endosso: (.*?) -', line)
        if endosso_match:
            erro['endosso'] = endosso_match.group(1).split(' -')[0]
        else:
            erro['endosso'] = "Não informado"

        # Extrair a mensagem de erro
        erro_match = re.search(r'Erro: (.*?)$', line)
        if erro_match:
            erro['mensagem'] = erro_match.group(1)
        else:
            erro['mensagem'] = "Erro não especificado"

        erros.append(erro)

    return erros

def formatar_mensagem_erro(erro):
    """
    Formata uma mensagem de erro para envio via WhatsApp.

    Args:
        erro: Dicionário contendo informações do erro

    Returns:
        String formatada com a mensagem
    """
    mensagem = "🚨 *Fatura não cadastrada* 🚨\n\n"
    mensagem += f"*ERRO*: {erro['mensagem']}\n"
    mensagem += f"*NOME*: {erro['nome']}\n"
    mensagem += f"*SEGURADORA*: {erro['seguradora']}\n"
    mensagem += f"*APÓLICE*: {erro['apolice']}\n"
    mensagem += f"*ENDOSSO*: {erro['endosso']}\n\n"
    mensagem += f"Ocorrido em: {erro['data_hora']}"

    return mensagem

def enviar_mensagem_whatsapp(driver, telefone, mensagem, identificacao=""):
    """
    Envia uma mensagem via WhatsApp Web.

    Args:
        driver: WebDriver do Selenium
        telefone: Número de telefone para envio (formato: 553199443174)
        mensagem: Mensagem a ser enviada
        identificacao: Identificação para registro no log

    Returns:
        Boolean indicando sucesso ou falha
    """
    try:
        # Construir URL para o WhatsApp Web
        link_mensagem_whatsapp = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'

        print(f"Abrindo WhatsApp Web para enviar notificação de erro {identificacao}")
        # Abrir WhatsApp Web
        driver.get(link_mensagem_whatsapp)

        # Esperar para a página carregar e o campo de mensagem aparecer
        wait = WebDriverWait(driver, 60)  # Tempo maior para garantir que a página carregue

        try:
            # Verificar se apareceu a mensagem de "telefone inválido"
            invalid_phone = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Telefone inválido.')]")))
            print(f"WhatsApp indicou telefone inválido: {telefone}")
            return False
        except:
            # Se não encontrou a mensagem de telefone inválido, continua normalmente
            pass

        # Esperar o botão de enviar aparecer - usando múltiplos seletores para maior chance de sucesso
        print(f"Aguardando botão de enviar...")
        try:
            # Tenta o seletor SVG primeiro
            send_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='Enviar' or @aria-label='Send']//span[@data-icon='send']/ancestor::button")))
        except:
            try:
                # Tenta o botão diretamente
                send_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Enviar' or @aria-label='Send']")))
            except:
                try:
                    # Tenta o span
                    send_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//span[@data-icon='send']/ancestor::button")))
                except:
                    # Último recurso
                    send_button = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button[aria-label='Enviar'], button[aria-label='Send']")))

        # Clicar no botão de enviar
        send_button.click()
        print(f"Mensagem de erro enviada com sucesso para {telefone}")

        # Espera entre mensagens (5 segundos)
        sleep(5)

        return True
    except Exception as e:
        print(f"Erro ao enviar mensagem para {telefone}: {str(e)}")
        return False

def enviar_notificacoes_erros(error_log_file, telefone_admin="553199443174"):
    """
    Lê o arquivo de erros e envia notificações via WhatsApp.

    Args:
        error_log_file: Caminho para o arquivo de log de erros
        telefone_admin: Número de telefone do administrador para receber as notificações
    """
    # Ler os erros do arquivo
    erros = ler_arquivo_erros(error_log_file)

    if not erros:
        print("Nenhum erro encontrado para notificar.")
        return

    print(f"Encontrados {len(erros)} erros para notificar.")

    # Iniciar o driver
    try:
        chrome_options = configurar_chrome()
        driver = webdriver.Chrome(options=chrome_options)
        print("Chrome inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o Chrome: {e}")
        return

    try:
        # Processar cada erro
        for i, erro in enumerate(erros):
            mensagem = formatar_mensagem_erro(erro)
            identificacao = f"{i+1}/{len(erros)} - {erro['seguradora']} - {erro['apolice']}"

            resultado = enviar_mensagem_whatsapp(driver, telefone_admin, mensagem, identificacao)

            if resultado:
                print(f"Notificação {identificacao} enviada com sucesso.")
            else:
                print(f"Falha ao enviar notificação {identificacao}.")

            # Pequena pausa entre envios para evitar bloqueios
            sleep(3)

        print("Todas as notificações de erro foram processadas.")

        # Após enviar todas as notificações, limpar o arquivo de log ou renomeá-lo
        backup_filename = f"{error_log_file}.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        os.rename(error_log_file, backup_filename)
        print(f"Arquivo de log renomeado para {backup_filename}")

        # Criar um novo arquivo vazio
        with open(error_log_file, 'w') as f:
            pass
        print(f"Novo arquivo de log criado: {error_log_file}")

    except Exception as e:
        print(f"Erro durante o envio de notificações: {e}")
    finally:
        # Fechar o driver
        driver.quit()
        print("Driver do Chrome fechado.")

# Função principal para ser chamada externamente
def notificar_erros():
    error_log_file = "error_log.txt"  # Nome do arquivo conforme definido no módulo web_automation
    enviar_notificacoes_erros(error_log_file)

if __name__ == "__main__":
    notificar_erros()