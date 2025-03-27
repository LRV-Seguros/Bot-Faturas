
"""
Módulo de processamento de faturas da AIG

Este módulo contém funções para extrair informações relevantes
de documentos PDF da seguradora AIG.

Autor: Lucelho Silva
"""
from src.utils.logging_config import setup_logging

logger = setup_logging()

def aig(texto):
    """
    Função principal para extração de dados de faturas da AIG.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    linhas = texto.split('\n')

    logger.info("Processando documento AIG")

    # DEBUG: Imprimir as primeiras 90 linhas para análise
    for i in range(min(90, len(linhas))):
        logger.debug(f"{i}: {linhas[i]}")
    cont = 0

    # Extrair nome do segurado
    nome = None
    if len(linhas) > 41:
        linha_nome = linhas[41]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        logger.info(f"Nome extraído: {nome}")

    # Extrair número da apólice e endosso
    for linha in linhas:
        if 'Nº Apólice' in linha:
            apolice = linhas[cont + 1].split('Nº Endosso')[0]
            endosso = linhas[cont + 2].split()[0]
            logger.info(f"Apolice: {apolice}")
            logger.info(f"Endosso: {endosso}")
            break
        cont = cont + 1

    # Extrair datas de vigência
    cont = 0
    for linha in linhas:
        if 'Vigência' in linha:
            inicio_vigencia = linhas[cont + 1].split()[5]
            fim_vigencia = linhas[cont + 1].split()[-1]
            logger.info(f"Início Vigência: {inicio_vigencia}")
            logger.info(f"Fim Vigência: {fim_vigencia}")
            break
        cont = cont + 1

    # Extrair data de emissão
    cont = 0
    for linha in linhas:
        if 'Data de Emissão' in linha:
            emissao = linhas[cont + 1].split()[0].replace(' ', '')
            logger.info(f"Data de Emissão: {emissao}")
            break
        cont = cont + 1

    # Extrair prêmio líquido
    cont = 0
    for linha in linhas:
        if 'Prêmio Total' in linha:
            premio_liquido = linhas[cont + 1].split()[-1].replace('.', '')
            logger.info(f"Prêmio Líquido: {premio_liquido}")
            break
        cont = cont + 1

    # Extrair data de vencimento
    cont = 0
    for linha in linhas:
        if 'Valor' in linha:
            vencimento = linhas[cont + 1].split()[0].replace(' ', '')
            logger.info(f"Vencimento: {vencimento}")
            break
        cont = cont + 1

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

    logger.info(f"Dados AIG extraídos: {dados}")
    return dados