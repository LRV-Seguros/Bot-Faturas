"""
Módulo de processamento de faturas da Swiss Re

Este módulo contém funções para extrair informações de faturas da Swiss Re.

Autor: Lucelho Silva
"""
import calendar
import re
from src.utils.logging_config import setup_logging

logger = setup_logging()


# Dicionário para conversão de nomes de meses para números
meses = {
     "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
     "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
     "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
 }

def swiss(texto):
    """
    Extrai informações de uma fatura da Swiss Re a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    texto = texto.split('\n')

    # DEBUG: Imprimir as primeiras 90 linhas para análise
    for i in range(min(90, len(texto))):
        logger.debug(f"{i}: {texto[i]}")

    # Extrair nome do segurado
    nome = None
    if len(texto) > 13:
        linha_nome = texto[13]
        nome = linha_nome.strip()
        logger.info(f"Nome extraído: {nome}")

    # Extrair ramo
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
            logger.info(f"Ramo extraído: {ramo}")
            break
        cont = cont + 1

    # Extrair apólice e endosso
    cont = 0
    for linha in texto:
        if 'Carga' in linha:
            apolice = texto[cont + 1].strip()
            logger.info(f"Apólice extraída: {apolice}")
            endosso = texto[cont + 2].strip().lstrip('0')
            logger.info(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    # Extrair datas
    cont = 0
    for linha in texto:
        if 'Modalidade:' in linha:
            emissao = texto[cont + 2].split(' ')[0].strip()
            vigencia = texto[cont + 4].split('.')[0].strip()
            logger.info(f"Emissão extraída: {emissao}")
            data = vigencia
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            inicio_vigencia = f"01/{mes}/{ano}"
            logger.info(f"Início de vigência extraído: {inicio_vigencia}")
            fim_vigencia = f"{ultimo_dia}/{mes}/{ano}"
            logger.info(f"Fim de vigência extraído: {fim_vigencia}")
            break
        cont = cont + 1

    # Extrair prêmios
    cont = 0
    for linha in texto:
        if 'Prêmio Total (R$):' in linha:
            premio_liquido = texto[cont + 1].split(' ')[-1].strip()
            premio_bruto = texto[cont + 5].split(' ')[-1].strip()
            logger.info(f"Prêmio líquido extraído: {premio_liquido}")
            logger.info(f"Prêmio líquido bruto: {premio_bruto}")
            break
        cont = cont + 1

    # Extrair data de vencimento
    vencimento = None
    if len(texto) > 88:
        linha_vencimento = texto[88]
        if "/" in linha_vencimento:
            match = re.search(r'\d{2}/\d{2}/\d{4}', linha_vencimento)
            if match:
                vencimento = match.group(0)
                logger.info(f"Vencimento extraído: {vencimento}")

    # Montar array de dados na ordem esperada pelo sistema
    dados.append(apolice)              # [0] - Número da apólice
    dados.append(endosso)              # [1] - Número do endosso
    dados.append(inicio_vigencia)      # [2] - Data da proposta (usando início vigência)
    dados.append(inicio_vigencia)      # [3] - Data inicial de vigência
    dados.append(fim_vigencia)         # [4] - Data final de vigência
    dados.append(emissao)              # [5] - Data de emissão
    dados.append(premio_liquido)       # [6] - Prêmio líquido
    dados.append(vencimento)           # [7] - Data de vencimento
    dados.append(nome)                 # [8] - Nome do segurado

    logger.info(f"Dados SWISS extraídos: {dados}")
    return dados