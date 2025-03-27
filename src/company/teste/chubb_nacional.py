import re

 # Dicionário de meses para conversão
meses = {
     "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
     "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
     "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
 }


def chubb_nacional(texto):
    """
    Extrai informações de uma fatura da Chubb para TRANSPORTE NACIONAL.

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

    print("Processando documento de TRANSPORTE NACIONAL")

    nome = None
    if len(texto) > 12:
        linha_nome = texto[12]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

    ramo = None
    if len(texto) > 18:
        linha_ramo = texto[18]
        linha_ramo = linha_ramo.strip()
        print(f"Ramo extraído: {linha_ramo}")

    apolice = None
    if len(texto) > 10:
        linha_apolice = texto[10]
        if "28." in linha_apolice:
            match = re.search(r'28\.\d+\.\d+\.\d+', linha_apolice)
            if match:
                apolice = match.group(0)
                partes = apolice.split('.')
                apolice = '.'.join(partes[:-1])
                print(f"Apólice extraída: {apolice}")

    endosso = None
    if len(texto) > 11:
        linha_endosso = texto[11]
        endosso = linha_endosso.strip()
        print(f"Endosso extraído: {endosso}")


    premio_liquido = None
    if len(texto) > 34:
        linha_premio = texto[34]
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
    if len(texto) > 53:
        linha_emissao = texto[53].lower()
        # Procurar data no formato "14DEFEVEREIRO DE2025"
        for mes_nome, mes_num in meses.items():
            if mes_nome in linha_emissao:
                # Extrair números do início da string (dia)
                dia_match = re.search(r'(\d{1,2})', linha_emissao)
                # Extrair números de 4 dígitos (ano)
                ano_match = re.search(r'de(\d{4})', linha_emissao, re.IGNORECASE)

                if dia_match and ano_match:
                    dia = dia_match.group(1).strip().zfill(2)
                    ano = ano_match.group(1).strip()
                    emissao = f"{dia}/{mes_num}/{ano}"
                    print(f"Emissão extraída: {emissao}")
                    break

    vencimento = None
    if len(texto) > 57:
        linha_vencimento = texto[57]
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