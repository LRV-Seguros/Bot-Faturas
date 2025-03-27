"""
Módulo de processamento de faturas da Chubb

Este módulo identifica o tipo de apólice Chubb e direciona para o
processador específico adequado ao formato do documento.

Autor: Lucelho Silva
"""
import re
from src.company.variants.chubb_internacional import chubb_internacional
from src.company.variants.chubb_nacional import chubb_nacional
from src.company.variants.chubb_rct import chubb_rct
from src.company.variants.chubb_rctr import chubb_rctr
from src.company.variants.chubb_rcf import chubb_rcf
from src.utils.logging_config import setup_logging

logger = setup_logging()

def chubb(texto):
    """
    Função principal para extração de dados de faturas da Chubb.
    Identifica o tipo de apólice e direciona para a função específica.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    linhas = texto.split('\n')

    logger.info("Processando documento Chubb - Identificando tipo de apólice")

    # Identificar tipo de apólice
    apolice = None
    for i in range(10, 50):
        if i < len(linhas):
            linha = linhas[i]
            if "28." in linha or "24." in linha:
                match = re.search(r'(28|24)\.\d+\.\d+\.\d+', linha)
                if match:
                    apolice_completa = match.group(0)
                    partes = apolice_completa.split('.')
                    if len(partes) >= 3:
                        tipo_apolice = f"{partes[0]}.{partes[1]}"
                        print(f"Tipo de apólice identificado: {tipo_apolice}")
                        break

    # Chamada da função específica com base no tipo de apólice
    if tipo_apolice == "28.22":
        print("Processando endosso de TRANSP.INTERNACIONAL")
        return chubb_internacional(texto)
    elif tipo_apolice == "28.21":
        print("Processando endosso de TRANSP. NACIONAL")
        return chubb_nacional(texto)
    elif tipo_apolice == "28.32":
        print("Processando endosso de RCT-VIAGEM INTERN.CARGA")
        return chubb_rct(texto)
    elif tipo_apolice == "28.54":
        print("Processando endosso de RCTR-C")
        return chubb_rctr(texto)
    elif tipo_apolice == "28.55":
        print("Processando endosso de RCF")
        return chubb_rcf(texto)
    else:
        logger.warning(f"Tipo de apólice não identificado: {tipo_apolice}, usando RCF como fallback")
        return chubb_rcf(texto)
