import calendar

# Dicionário de meses para conversão
meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

def swiss(texto):
    """
    Extrai informações relevantes de uma fatura da Swiss a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF da fatura

    Returns:
        list: Lista contendo os seguintes dados na ordem:
            [0] - Número da apólice coletiva
            [1] - Número do endosso
            [2] - Data da proposta (usando data de emissão)
            [3] - Data inicial de vigência (primeiro dia do mês)
            [4] - Data inicial de vigência (duplicada)
            [5] - Data final de vigência (último dia do mês)
            [6] - Data de emissão
            [7] - Prêmio líquido
            [8] - Data de vencimento
    """
    dados = []
    texto = texto.split('\n')

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
            print(f"Ramo: {ramo}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Carga' in linha:
            apolice = texto[cont + 1].strip()
            endosso = texto[cont + 2].strip()
            # Mantido para referência, mas não usado
            n_proposta = texto[cont + 3].strip()
            break
        cont = cont + 1

    # Buscando datas de vigência e emissão
    cont = 0
    for linha in texto:
        if 'Modalidade:' in linha:
            emissao = texto[cont + 2].split(' ')[0].strip()
            vigencia = texto[cont + 4].split('.')[0].strip()
            print(f"Emissão: {emissao}")
            print(f"Vigencia: {vigencia}")

            # Processando a data de vigência
            data = vigencia
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            primeiro_dia = f"01/{mes}/{ano}"
            ultimo_dia_formatado = f"{ultimo_dia}/{mes}/{ano}"
            break
        cont = cont + 1

    # Buscando prêmio líquido
    cont = 0
    for linha in texto:
        if 'Prêmio Total (R$):' in linha:
            premio_liquido = texto[cont + 1].split(' ')[-1].strip()
            premio_bruto = texto[cont + 5].split(' ')[-1].strip()
            print(f"Prêmio líquido: {premio_liquido}")
            print(f"Prêmio bruto: {premio_bruto}")
            break
        cont = cont + 1

    # Buscando data de vencimento
    cont = 0
    for linha in texto:
        if 'CONDIÇÕES GERAIS' in linha:
            vencimento = texto[cont - 1].strip()
            print(f"Vencimento: {vencimento}")
            break
        cont = cont + 1

    dados.append(apolice)
    dados.append(endosso)
    dados.append(emissao)
    dados.append(primeiro_dia)
    dados.append(primeiro_dia)
    dados.append(ultimo_dia_formatado)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)

    return dados