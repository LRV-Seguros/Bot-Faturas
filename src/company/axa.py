"""
Módulo de processamento de faturas da AXA

Este módulo contém funções para extrair informações de faturas da AXA
em seus diferentes formatos.

Autor: Lucelho Silva
"""

import re
from src.utils.logging_config import setup_logging

logger = setup_logging()

# Dicionário para conversão de nomes de meses para números
meses = {
     "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
     "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
     "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
 }

def axa(texto):
    """
    Extrai informações de uma fatura da AXA (formato padrão) a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    texto = texto.split('\n')

    logger.info("Processando documento AXA (formato padrão)")

    # DEBUG: Imprimir as primeiras 90 linhas para análise
    for i in range(min(90, len(texto))):
        logger.debug(f"{i}: {texto[i]}")

    # Extrair nome do segurado
    nome = None
    if len(texto) > 39:
        linha_nome = texto[39]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        logger.info(f"Nome extraído: {nome}")

    # Extrair ramo
    cont = 0
    for linha in texto:
        if 'Nomenclatura de Ramo e Produto' in linha:
            ramo = texto[cont + 1].split(' ')[-1]
            logger.info(f"Ramo extraído: {ramo}")
            break
        cont = cont + 1

    # Extrair número do endosso
    cont = 0
    for linha in texto:
        if 'Nº pedido de endosso' in linha:
            endosso = ''
            end = texto[cont + 1].split(' ')[0]
            for char in end:
                if char.isdigit():
                    endosso = endosso + char
            logger.info(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    # Extrair datas de vigência
    cont = 0
    for linha in texto:
        if 'Início de Vigência:' in linha:
            end = texto[cont + 1].split(' ')
            for e in end:
                if '/' in e:
                    inicio_vigencia = e[:10]
            logger.info(f"Início de vigência extraído: {inicio_vigencia}")
            end = texto[cont + 2].split(' ')
            for e in end:
                if '/' in e:
                    fim_vigencia = e[:10]
            logger.info(f"Fim de vigência extraído: {fim_vigencia}")
            break
        cont = cont + 1

    # Extrair data de emissão
    cont = 0
    for linha in texto:
        if 'Data da Emissão' in linha:
            end = texto[cont + 1].find('Número da apólice')
            emissao = texto[cont + 1][:end]

            # Converter data escrita por extenso para formato DD/MM/AAAA
            if 'de' in emissao:
                partes = emissao.split(" de ")
                dia = partes[0].split(' ')[-1]
                mes = meses[partes[1].lower()]
                ano = partes[2]
                emissao = f"{dia}/{mes}/{ano}"

            logger.info(f"Emissão extraída: {emissao}")
            break
        cont = cont + 1

    # Extrair número da apólice
    cont = 0
    for linha in texto:
        if 'Nº Apólice averbação' in linha:
            end = texto[cont].find('Nº Apólice averbação')
            apolice = texto[cont][:end]
            logger.info(f"Apólice extraída: {apolice}")
            break
        cont = cont + 1

    # Extrair prêmios
    cont = 0
    for linha in texto:
        if 'Prêmio Líquido' in linha:
            premio_liquido = texto[cont].split(' ')[-1]
            logger.info(f"Prêmio líquido extraído: {premio_liquido}")
            break
        cont = cont + 1

    # Extrair prêmio bruto
    cont = 0
    for linha in texto:
        if 'Prêmio Total' in linha:
            premio_bruto = texto[cont].split(' ')[-1]
            logger.info(f"Prêmio bruto: {premio_bruto}")
            break
        cont = cont + 1

    # Extrair data de vencimento
    cont = 0
    for linha in texto:
        if 'Vencimento:' in linha:
            vencimento = texto[cont + 1].split(' ')[1]
            logger.info(f"Vencimento extraído: {vencimento}")
            break
        cont = cont + 1

    # Montar array de dados na ordem esperada pelo sistema
    dados.append(apolice)               # [0] - Número da apólice
    dados.append(endosso)               # [1] - Número do endosso
    dados.append(inicio_vigencia)       # [2] - Data da proposta (usando início vigência)
    dados.append(inicio_vigencia)       # [3] - Data de início da vigência
    dados.append(fim_vigencia)          # [4] - Data de fim da vigência
    dados.append(emissao)               # [5] - Data de emissão
    dados.append(premio_liquido)        # [6] - Prêmio líquido
    dados.append(vencimento)            # [7] - Data de vencimento
    dados.append(nome)                  # [8] - Nome do segurado

    logger.info(f"Dados AXA extraídos: {dados}")
    return dados

def axa_b(texto):
    """
    Extrai informações de uma fatura da AXA (formato alternativo) a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """

    dados = []
    texto = texto.split('\n')

    logger.info("Processando documento AXA (formato alternativo)")

    # DEBUG: Imprimir as primeiras 90 linhas para análise
    for i in range(min(90, len(texto))):
        logger.info(f"{i}: {texto[i]}")

    # Extrair nome do segurado
    nome = None
    if len(texto) > 39:
        linha_nome = texto[39]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        logger.debug(f"Nome extraído: {nome}")

    # Extrair número do endosso
    cont = 0
    for linha in texto:
        if 'Endosso:' in linha:
            endosso = texto[cont+1]
            logger.info(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    # Extrair datas de vigência
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
                logger.info(f"Início de vigência extraído: {inicio_vigencia}")
                logger.info(f"Fim de vigência extraído: {fim_vigencia}")
            except:
                logger.warning("Datas de vigência não encontradas no formato esperado")
            break
        cont = cont + 1

    # Extrair data de emissão (do cabeçalho)
    cont = 0
    emissao = texto[0]
    partes = emissao.split(" ")
    dia = partes[0]
    mes = meses[partes[1].lower()]
    ano = partes[2]
    emissao = f"{dia}/{mes}/{ano}"
    logger.info(f"Emissão extraída: {emissao}")

    # Extrair número da apólice
    cont = 0
    for linha in texto:
        if 'www.axa.com.brOuvidoriaApólice' in linha:
            apolice = texto[cont + 1]
            logger.info(f"Apólice extraída: {apolice}")
            break
        cont = cont + 1
    cont = 0

    # Extrair prêmio líquido
    for linha in texto:
        if 'Pagamento:Moeda: R$' in linha:
            premio_liquido = texto[cont].split(' ')[-2]
            premio_liquido.replace('.', '')
            logger.info(f"Prêmio líquido extraído: {premio_liquido}")
            break
        cont = cont + 1

    # Extrair data de vencimento
    cont = 0
    for linha in texto:
        if 'PRÊMIO TOTAL' in linha:
            venc = texto[cont + 1].split(' ')
            for v in venc:
                if '/' in v:
                    vencimento = v
                    break
            logger.info(f"Vencimento extraído: {vencimento}")
            break
        cont = cont + 1

    # Montar array de dados na ordem esperada pelo sistema
    dados.append(apolice)               # [0] - Número da apólice
    dados.append(endosso)               # [1] - Número do endosso
    dados.append(inicio_vigencia)       # [2] - Data da proposta (usando início vigência)
    dados.append(inicio_vigencia)       # [3] - Data de início da vigência
    dados.append(fim_vigencia)          # [4] - Data de fim da vigência
    dados.append(emissao)               # [5] - Data de emissão
    dados.append(premio_liquido)        # [6] - Prêmio líquido
    dados.append(vencimento)            # [7] - Data de vencimento
    dados.append(nome)                  # [8] - Nome do segurado

    logger.info(f"Dados AXA (formato alternativo) extraídos: {dados}")
    return dados