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
    print("Primeiras 90 linhas do documento:")
    for i in range(min(90, len(linhas))):
        print(f"{i}: {linhas[i]}")

    nome = None
    if len(linhas) > 34:
        linha_nome = linhas[34]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

    ramo = None
    if len(linhas) > 39:
        linha_ramo = linhas[39]
        linha_ramo = linha_ramo.strip()
        print(f"Ramo extraído: {linha_ramo}")

    apolice = None
    if len(linhas) > 32:
        linha_apolice = linhas[32]
        if "28." in linha_apolice:
            match = re.search(r'28\.\d+\.\d+\.\d+', linha_apolice)
            if match:
                apolice = match.group(0)
                partes = apolice.split('.')
                apolice = '.'.join(partes[:-1])
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
    for i in range(60, 64):
        if i < len(linhas):
            linha = linhas[i]
            datas = re.findall(r'\d{2}/\d{2}/\d{4}', linha)
            if len(datas) >= 2:  # Se encontrar pelo menos duas datas na linha
                inicio_vigencia = datas[0]
                fim_vigencia = datas[-1]
                print(f"Início de vigência extraído: {inicio_vigencia}")
                print(f"Fim de vigência extraído: {fim_vigencia}")
                break

    emissao = None
    if len(linhas) > 13:
        linha_emissao = linhas[13]
        if "/" in linha_emissao:
            match = re.search(r'\d{2}/\d{2}/\d{4}', linha_emissao)
            if match:
                emissao = match.group(0)
                print(f"Emissão extraída: {emissao}")

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
        dados.append(emissao)  # Data da proposta (usando data de emissão)
        dados.append(inicio_vigencia)
        dados.append(inicio_vigencia)
        dados.append(fim_vigencia)
        dados.append(emissao)
        dados.append(premio_liquido)
        dados.append(vencimento)

    print(f"Dados extraídos: {dados}")
    return dados