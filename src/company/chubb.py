import re

def chubb(texto):
    """
    Extrai informações de uma fatura da Chubb a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    # Divide o texto em linhas para iterar corretamente
    linhas = texto.split('\n')

    # Imprime algumas linhas para debug
    # print("Primeiras 90 linhas do documento:")
    # for i in range(min(90, len(linhas))):
    #     print(f"{i}: {linhas[i]}")

    ramo = None
    if len(linhas) > 40:
        linha_ramo = linhas[40]
        linha_ramo = linha_ramo.strip()
        print(f"Ramo extraído: {linha_ramo}")

    apolice = None
    if len(linhas) > 32:
        linha_apolice = linhas[32]
        if "28.54." in linha_apolice:
            match = re.search(r'28\.\d+\.\d+\.\d+', linha_apolice)
            if match:
                apolice = match.group(0)
                print(f"Apólice extraída: {apolice}")

    endosso = None
    if len(linhas) > 33:
        linha_endosso = linhas[33]
        endosso = linha_endosso.strip()
        print(f"Endosso extraído: {endosso}")

    premio_liquido = None
    if len(linhas) > 87:
        linha_premio = linhas[87]
        premio_liquido = linha_premio.strip()
        print(f"Prêmio líquido extraído: {premio_liquido}")

    inicio_vigencia = None
    fim_vigencia = None
    if len(linhas) > 62:
        linha_vigencia = linhas[62]
        if "dodia" in linha_vigencia and "às" in linha_vigencia:
            # Extrair data inicial (formato DD/MM/AAAA)
            inicio_match = re.search(r'dodia(\d{2}/\d{2}/\d{4})', linha_vigencia)
            if inicio_match:
                inicio_vigencia = inicio_match.group(1)
                print(f"Início de vigência extraído: {inicio_vigencia}")

            # Extrair data final (formato DD/MM/AAAA)
            fim_match = re.search(r'dodia(\d{2}/\d{2}/\d{4})$', linha_vigencia)
            if fim_match:
                fim_vigencia = fim_match.group(1)
                print(f"Fim de vigência extraído: {fim_vigencia}")

    vencimento = None
    if len(linhas) > 17:
        linha_vencimento = linhas[17]
        if "/" in linha_vencimento:
            match = re.search(r'\d{2}/\d{2}/\d{4}', linha_vencimento)
            if match:
                vencimento = match.group(0)
                print(f"Vencimento extraído: {vencimento}")

    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    # dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(f"Dados extraídos: {dados}")
    return dados