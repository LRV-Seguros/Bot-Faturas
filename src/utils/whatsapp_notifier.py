import os
import time
import traceback
from urllib.parse import quote
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

def notificar_erros_whatsapp(arquivo_erros='src/logs/error_documents.txt', numero_telefone='5531994431744'):
    """
    Lê o arquivo de erros, formata as informações e envia uma notificação pelo WhatsApp.

    Args:
        arquivo_erros: Caminho para o arquivo que contém os registros de erros
        numero_telefone: Número do WhatsApp que receberá a notificação

    Returns:
        bool: True se a mensagem foi enviada com sucesso, False caso contrário
    """
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_erros):
        print(f"Arquivo de erros {arquivo_erros} não encontrado.")
        return False

    # Ler os erros mais recentes do arquivo (últimos 5 registros)
    try:
        with open(arquivo_erros, 'r') as f:
            linhas = f.readlines()

        # Se não há erros, não há necessidade de enviar notificação
        if not linhas:
            print("Não há erros registrados para notificar.")
            return True

        # Obter os 5 erros mais recentes (ou menos, se houver menos de 5)
        erros_recentes = linhas[-5:] if len(linhas) > 5 else linhas

        # Formatar a mensagem de notificação
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mensagem = f"🚨 *ALERTA DE ERROS - {data_atual}* 🚨\n\n"
        mensagem += "Foram detectados os seguintes erros no processamento de documentos:\n\n"

        for i, linha in enumerate(erros_recentes, 1):
            partes = linha.strip().split("|")
            if len(partes) >= 3:
                documento = os.path.basename(partes[0])
                seguradora = partes[1]
                data = partes[2]
                erro = partes[3] if len(partes) > 3 else "Erro desconhecido"

                mensagem += f"*Erro {i}:*\n"
                mensagem += f"📄 Documento: {documento}\n"
                mensagem += f"🏢 Seguradora: {seguradora}\n"
                mensagem += f"📆 Data: {data}\n"
                mensagem += f"❌ Erro: {erro}\n\n"

        mensagem += "Por favor, verifique o log completo para mais detalhes."

        # Configurar o Chrome para usar WhatsApp Web
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Definir um perfil específico para evitar problemas de sessão
        user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_whatsapp_data")
        os.makedirs(user_dir, exist_ok=True)
        chrome_options.add_argument(f"--user-data-dir={user_dir}")

        # Iniciar o Chrome
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Construir URL para o WhatsApp Web
            link_whatsapp = f'https://web.whatsapp.com/send?phone={numero_telefone}&text={quote(mensagem)}'

            print(f"Abrindo WhatsApp Web para notificar erros...")
            driver.get(link_whatsapp)

            # Esperar a página carregar e o campo de mensagem aparecer
            wait = WebDriverWait(driver, 60)  # 60 segundos para garantir que a página carregue

            # Verificar se apareceu mensagem de telefone inválido
            try:
                invalid_phone = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'Telefone inválido.')]")
                ))
                print(f"WhatsApp indicou telefone inválido: {numero_telefone}")
                return False
            except:
                # Se não encontrou a mensagem de telefone inválido, continua
                pass

            # Tentar localizar o botão de enviar de várias maneiras
            try:
                # Primeiro seletor
                send_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Enviar' or @aria-label='Send']//span[@data-icon='send']/..")
                ))
            except:
                try:
                    # Segundo seletor
                    send_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@aria-label='Enviar' or @aria-label='Send']")
                    ))
                except:
                    try:
                        # Terceiro seletor
                        send_button = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, "//span[@data-icon='send']/ancestor::button")
                        ))
                    except:
                        # Último recurso
                        send_button = wait.until(EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button[aria-label='Enviar'], button[aria-label='Send']")
                        ))

            # Clicar no botão de enviar
            send_button.click()
            print("Notificação de erros enviada com sucesso via WhatsApp")

            # Aguardar um pouco para garantir que a mensagem foi enviada
            time.sleep(5)

            return True

        except Exception as e:
            print(f"Erro ao enviar notificação WhatsApp: {str(e)}")
            traceback.print_exc()
            return False

        finally:
            # Fechar o navegador
            driver.quit()

    except Exception as e:
        print(f"Erro ao processar arquivo de erros: {str(e)}")
        traceback.print_exc()
        return False


# Função para integrar a notificação ao processo principal
def verificar_e_notificar_erros(arquivo_erros='src/logs/error_documents.txt',
                               numero_telefone='553199443174',
                               intervalo_minimo=360):  # 6 horas em minutos
    """
    Verifica se há erros recentes e envia uma notificação se necessário.
    Evita enviar múltiplas notificações em um período curto.

    Args:
        arquivo_erros: Caminho para o arquivo de erros
        numero_telefone: Número para enviar a notificação
        intervalo_minimo: Intervalo mínimo entre notificações em minutos

    Returns:
        bool: True se a verificação foi realizada com sucesso
    """
    try:
        # Arquivo para rastrear a última notificação
        controle_arquivo = 'src/logs/ultima_notificacao.txt'

        # Verificar quando foi a última notificação
        ultima_notificacao = None
        if os.path.exists(controle_arquivo):
            with open(controle_arquivo, 'r') as f:
                try:
                    ultima_notificacao = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S")
                except:
                    ultima_notificacao = None

        # Verificar se o arquivo de erros foi modificado após a última notificação
        if not os.path.exists(arquivo_erros):
            return False

        data_modificacao = os.path.getmtime(arquivo_erros)
        data_mod = datetime.fromtimestamp(data_modificacao)

        agora = datetime.now()

        # Decidir se deve notificar:
        # 1. Se nunca notificou antes
        # 2. Se o arquivo foi modificado após a última notificação
        # 3. Se já passou o intervalo mínimo desde a última notificação
        deve_notificar = (
            ultima_notificacao is None or
            (data_mod > ultima_notificacao and
             (agora - ultima_notificacao).total_seconds() > (intervalo_minimo * 60))
        )

        if deve_notificar:
            print("Enviando notificação de erros via WhatsApp...")
            sucesso = notificar_erros_whatsapp(arquivo_erros, numero_telefone)

            if sucesso:
                # Registrar o momento da notificação
                with open(controle_arquivo, 'w') as f:
                    f.write(agora.strftime("%Y-%m-%d %H:%M:%S"))
                print(f"Notificação enviada e registrada: {agora}")

            return sucesso
        else:
            print("Nenhuma notificação necessária neste momento.")
            return True

    except Exception as e:
        print(f"Erro ao verificar e notificar erros: {str(e)}")
        traceback.print_exc()
        return False