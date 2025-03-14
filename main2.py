import os
from seleniumbase import Driver
from datetime import datetime
import traceback

# Importando configurações
from src.config.settings import TIPO_SEGURADORA, LOG_FILE

# Importando as funções de processamento de cada companhia
from src.company.swiss import swiss
from src.company.fairfax import fairfax
from src.company.sura import sura
from src.company.sompo import sompo
from src.company.axa import axa, axa_b
from src.company.aig import aig
from src.company.berkley import berkley
from src.company.chubb import chubb

# Importando funções utilitárias
from src.utils.utils import ler_pdf_completo, registrar_fatura, remover_arquivos, registrar_error
from src.utils.logging_config import setup_logging
from src.utils.whatsapp_notifier import verificar_e_notificar_erros  # Nova importação

# Importando serviços
from src.services.email_handler import baixar_emails
from src.services.web_automation import quiver

# Configuração do logger
logger = setup_logging()

lista_pdfs = []
lista_documentos = []
nome_arquivo = LOG_FILE

# Arquivo para registrar documentos com erro
error_log = "src/logs/error_documents.txt"

# Inicialização
listaFeitos = []
listaErros = []

# Número de telefone para notificações de erro
TELEFONE_NOTIFICACAO = '553199443174'  # Número fixo para receber as notificações

# Carregar os arquivos já processados
if os.path.exists(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        listaFeitos = [linha.strip() for linha in arquivo.readlines()]
else:
    with open(nome_arquivo, "w") as arquivo:
        pass

# Carregar os arquivos com erro para evitar loops infinitos de tentativas
if os.path.exists(error_log):
    with open(error_log, "r") as arquivo:
        listaErros = [linha.split("|")[0].strip() for linha in arquivo.readlines()]
else:
    with open(error_log, "w") as arquivo:
        pass

def registrar_erro(caminho, seguradora, erro):
    """
    Registra um documento que falhou no processamento

    Args:
        caminho: Caminho do arquivo que falhou
        seguradora: Nome da seguradora
        erro: Mensagem de erro
    """
    with open(error_log, "a") as arquivo:
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        arquivo.write(f"{caminho}|{seguradora}|{data_atual}|{erro}\n")
    logger.error(f"Documento adicionado à lista de erros: {caminho}")

    # Também registrar no formato antigo para compatibilidade
    erro_resumido = str(erro).split('\n')[0][:100]  # Pegar apenas a primeira linha e limitar tamanho
    registrar_error("src/logs/erros_processamento.txt", seguradora, caminho, erro_resumido)

# Função para processar um documento individual com tratamento de erros
def processar_documento(documento, seguradora_nome, processador_func, tipo_seguradora):
    """
    Processa um documento com tratamento de erros robusto

    Args:
        documento: Lista com informações do documento
        seguradora_nome: Nome da seguradora
        processador_func: Função para processar o documento
        tipo_seguradora: Tipo da seguradora (1 ou 2)

    Returns:
        bool: True se processado com sucesso, False caso contrário
    """
    caminho = documento[0] if len(documento) > 0 else "desconhecido"

    try:
        # Encontrar o documento PDF principal
        caminho = ''
        for doc in documento:
            if any(term in doc.lower() for term in ['ndosso', 'esumo', 'atura', 'elação', 'oleto']) and '.pdf' in doc.lower():
                caminho = doc
                break

        if not caminho:
            logger.warning(f"Nenhum documento PDF encontrado para {seguradora_nome}")
            return False

        if caminho in listaFeitos:
            logger.info(f"Documento já processado anteriormente: {caminho}")
            return True

        if caminho in listaErros:
            logger.info(f"Documento com erro anterior, pulando: {caminho}")
            return False

        # Ler conteúdo do PDF
        texto = ''
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                texto = ler_pdf_completo(caminho)
                if len(texto) >= 100:
                    break
                logger.warning(f"Tentativa {attempt+1}: Texto extraído muito curto ({len(texto)} caracteres)")
            except Exception as e:
                logger.warning(f"Tentativa {attempt+1}: Erro ao ler PDF: {str(e)}")
                if attempt == max_attempts - 1:
                    raise

        if len(texto) < 100:
            raise ValueError(f"Conteúdo do PDF muito pequeno: {len(texto)} caracteres")

        # Processar dados da seguradora
        logger.info(f"Processando documento {seguradora_nome}: {caminho}")
        dados = processador_func(texto)

        if dados is None or len(dados) < 8:
            raise ValueError(f"Dados extraídos insuficientes ou inválidos: {dados}")

        # Automatizar inserção no sistema
        try:
            quiver(dados, documento, tipo_seguradora=tipo_seguradora)
        except Exception as e:
            logger.error(f"Erro na automação web (quiver): {str(e)}")
            stack_trace = traceback.format_exc()
            logger.debug(f"Stack trace: {stack_trace}")
            raise Exception(f"Falha na automação web: {str(e)}")

        # Registrar sucesso
        listaFeitos.append(caminho)
        registrar_fatura(nome_arquivo, dados)
        logger.info(f"Documento {seguradora_nome} processado com sucesso: {dados[0]}")
        return True

    except Exception as e:
        stack_trace = traceback.format_exc()
        error_msg = f"Erro ao processar documento {seguradora_nome}: {str(e)}"
        logger.error(error_msg)
        logger.debug(f"Stack trace: {stack_trace}")
        registrar_erro(caminho, seguradora_nome, str(e))

        # Incrementar contador de erros para determinar se notificação é necessária
        global contador_erros
        contador_erros += 1

        return False

# Bloco principal
try:
    # Contador para acompanhar erros nesta execução
    contador_erros = 0

    # Iniciar driver e baixar emails
    driver = Driver(uc=True, headless=False)
    driver.maximize_window()

    try:
        logger.info("Iniciando download de emails")
        lista_documentos, lista_pdfs = baixar_emails(driver, lista_documentos, lista_pdfs)
        logger.info(f"Download concluído: {len(lista_documentos)} documentos encontrados")
    except Exception as e:
        logger.error(f"Erro ao baixar emails: {str(e)}")
        stack_trace = traceback.format_exc()
        logger.debug(f"Stack trace: {stack_trace}")
        registrar_erro("download_emails", "sistema", str(e))
        contador_erros += 1
    finally:
        driver.quit()

    # Processar documentos
    if len(lista_documentos) > 0:
        logger.info(f"Iniciando processamento de {len(lista_documentos)} documentos")

        for documento in lista_documentos:
            if len(documento) < 1:
                logger.warning("Documento vazio encontrado, pulando")
                continue

            teste = str(documento[0]).lower()

            # Determinar a seguradora e processar o documento
            if 'wiss' in teste:
                processar_documento(documento, "Swiss", swiss, TIPO_SEGURADORA['swiss'])
            elif 'airfax' in teste:
                processar_documento(documento, "Fairfax", fairfax, TIPO_SEGURADORA['fairfax'])
            elif 'ura' in teste:
                processar_documento(documento, "Sura", sura, TIPO_SEGURADORA['sura'])
            elif 'ompo' in teste:
                processar_documento(documento, "Sompo", sompo, TIPO_SEGURADORA['sompo'])
            elif 'xa' in teste:
                # Caso especial da AXA com duas funções diferentes
                def process_axa(texto):
                    try:
                        return axa(texto)
                    except:
                        return axa_b(texto)
                processar_documento(documento, "AXA", process_axa, TIPO_SEGURADORA['axa'])
            elif 'ig' in teste:
                processar_documento(documento, "AIG", aig, TIPO_SEGURADORA['aig'])
            elif 'erkley' in teste:
                processar_documento(documento, "Berkley", berkley, TIPO_SEGURADORA['berkley'])
            elif 'hubb' in teste:
                processar_documento(documento, "Chubb", chubb, TIPO_SEGURADORA['chubb'])
            else:
                logger.warning(f"Seguradora não identificada para o documento: {documento[0]}")
    else:
        logger.info("Nenhum documento para processar")

    # Enviar notificação se houver erros registrados
    if contador_erros > 0:
        logger.info(f"Foram detectados {contador_erros} erros nesta execução. Verificando necessidade de notificação.")
        verificar_e_notificar_erros(error_log, TELEFONE_NOTIFICACAO)
    else:
        logger.info("Nenhum erro detectado nesta execução.")

except Exception as e:
    logger.critical(f"Erro crítico no programa principal: {str(e)}")
    stack_trace = traceback.format_exc()
    logger.debug(f"Stack trace: {stack_trace}")
    registrar_erro("programa_principal", "sistema", str(e))

    # Tentar notificar sobre erro crítico
    try:
        verificar_e_notificar_erros(error_log, TELEFONE_NOTIFICACAO, intervalo_minimo=0)  # Forçar notificação para erros críticos
    except:
        logger.error("Falha ao enviar notificação sobre erro crítico")

finally:
    # Limpeza final - remover os arquivos processados
    try:
        remover_arquivos(lista_documentos)
        logger.info("Arquivos temporários removidos")
    except Exception as e:
        logger.error(f"Erro ao remover arquivos: {str(e)}")

    logger.info("Processamento concluído")