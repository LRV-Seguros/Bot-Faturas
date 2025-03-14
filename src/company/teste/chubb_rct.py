import re

def chubb_rct(texto):
    """
    Extrai informações de uma fatura da Chubb para RCT-VIAGEM INTERN.CARGA.

    Args:
        texto (str): Texto completo extraído do PDF

    Returns:
        list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    # Divide o texto em texto para iterar corretamente
    texto = texto.split('\n')
    print("Primeiras 90 texto do documento:")
    for i in range(min(90, len(texto))):
        print(f"{i}: {texto[i]}")

    print("Processando documento de RCT-VIAGEM INTERN.CARGA")

    nome = None
    if len(texto) > 30:
        linha_nome = texto[30]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

    ramo = None
    if len(texto) > 35:
        linha_ramo = texto[35]
        linha_ramo = linha_ramo.strip()
        print(f"Ramo extraído: {linha_ramo}")

    apolice = None
    # Procurando especificamente por 28.32 para RCT
    for i in range(25, 40):
        if i < len(texto):
            linha = texto[i]
            if "28.32" in linha or "28.3" in linha:
                match = re.search(r'28\.\d+\.\d+\.\d+', linha)
                if match:
                    apolice = match.group(0)
                    partes = apolice.split('.')
                    apolice = '.'.join(partes[:-1])
                    print(f"Apólice extraída: {apolice}")
                    break

    endosso = None
    if len(texto) > 29:
        linha_endosso = texto[29]
        endosso = linha_endosso.strip()
        print(f"Endosso extraído: {endosso}")

    premio_liquido = None
    if len(texto) > 82:
        linha_premio = texto[82]
        premio_liquido = linha_premio.strip()
        print(f"Prêmio líquido extraído: {premio_liquido}")

    inicio_vigencia = None
    fim_vigencia = None
    for i in range(0, 70):
        if i < len(texto):
            linha = texto[i]
            datas = re.findall(r'\d{2}/\d{2}/\d{4}', linha)
            if len(datas) >= 2:  # Se encontrar pelo menos duas datas na linha
                inicio_vigencia = datas[0]
                fim_vigencia = datas[-1]
                print(f"Início de vigência extraído: {inicio_vigencia}")
                print(f"Fim de vigência extraído: {fim_vigencia}")
                break

    emissao = None
    if len(texto) > 11:
        linha_emissao = texto[11]
        if "/" in linha_emissao:
            match = re.search(r'\d{2}/\d{2}/\d{4}', linha_emissao)
            if match:
                emissao = match.group(0)
                print(f"Emissão extraída: {emissao}")

    vencimento = None
    if len(texto) > 10:
        linha_vencimento = texto[10]
        if "/" in linha_vencimento:
            match = re.search(r'\d{2}/\d{2}/\d{4}', linha_vencimento)
            if match:
                vencimento = match.group(0)
                print(f"Vencimento extraído: {vencimento}")

    # Montar array de dados - removido da condição para garantir o retorno
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