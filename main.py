import os
from seleniumbase import Driver
from datetime import datetime

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
from src.utils.utils import ler_pdf_completo, registrar_fatura, remover_arquivos
from src.utils.logging_config import setup_logging

# Importando serviços
from src.services.email_handler import baixar_emails
from src.services.web_automation import quiver

# Configuração do logger
logger = setup_logging()

lista_pdfs = []
lista_documentos = []
nome_arquivo = LOG_FILE

# Inicialização
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

# Processamento de emails
lista_documentos, lista_pdfs = baixar_emails(driver, lista_documentos, lista_pdfs)
driver.quit()

if len(lista_documentos) > 0:
    for documento in lista_documentos:
        caminho = ''
        encontrado = 0
        for doc in documento:
            if doc.find('ndosso') > 0 and doc.find('pdf') > 0:
                caminho = doc
                encontrado = 1
                break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('esumo') > 0 and doc.find('pdf') > 0:
                        caminho = doc
                        encontrado = 1
                        break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('atura') > 0 and doc.find('pdf') > 0:
                        caminho = doc
                        encontrado = 1
                        break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('elação') > 0 and doc.find('pdf') > 0:
                        caminho = doc
                        encontrado = 1
                        break
            if encontrado == 0:
                for doc in documento:
                    if doc.find('oleto') == 0 and doc.find('pdf') > 0:
                        caminho = doc
                        encontrado = 1
                        break
        if caminho != '' and caminho not in listaFeitos:
            logger.info(f'Processando documento: {caminho}')
            texto = ''
            while len(texto) < 100:
                texto = ler_pdf_completo(caminho)
            teste = str(documento[0]).lower()

            # Swiss
            if teste.find('wiss') > 0:
                dados = None
                try:
                    dados = swiss(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['swiss'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento Swiss processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento Swiss: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

            # Fairfax
            elif teste.find('airfax') > 0:
                dados = None
                try:
                    dados = fairfax(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['fairfax'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento Fairfax processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento Fairfax: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

            # Sura
            elif teste.find('ura') > 0:
                dados = None
                try:
                    dados = sura(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['sura'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento Sura processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento Sura: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

            # Sompo
            elif teste.find('ompo') > 0:
                dados = None
                try:
                    dados = sompo(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['sompo'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento Sompo processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento Sompo: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

            # AXA
            elif teste.find('xa') > 0:
                dados = None
                try:
                    try:
                        dados = axa(texto)
                    except:
                        dados = axa_b(texto)

                    if dados:
                        quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['axa'])
                        listaFeitos.append(caminho)
                        logger.info(f"Documento AXA processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento AXA: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

            # AIG
            elif teste.find('ig') > 0:
                dados = None
                try:
                    dados = aig(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['aig'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento AIG processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento AIG: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

            # Berkley
            elif teste.find('erkley') > 0:
                dados = None
                try:
                    dados = berkley(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['berkley'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento Berkley processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento Berkley: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)
            # Chubb
            elif teste.find('hubb') > 0:
                dados = None
                try:
                    dados = chubb(texto)
                    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['chubb'])
                    listaFeitos.append(caminho)
                    logger.info(f"Documento Chubb processado com sucesso: {dados[0]}")
                except Exception as e:
                    logger.error(f"Erro ao processar documento Chubb: {e}", exc_info=True)

                registrar_fatura(nome_arquivo, dados)

# Remover os arquivos processados
remover_arquivos(lista_documentos)
logger.info("Processamento concluído")