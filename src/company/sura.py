import calendar

# Dicionário de meses para conversão
meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

def sura(texto):
    """
    Extrai informações relevantes de uma fatura da Sura a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF da fatura

    Returns:
        list: Lista contendo os seguintes dados na ordem:
            [0] - Número da apólice
            [1] - Número da fatura
            [2] - Data da proposta
            [3] - Data inicial de vigência (primeiro dia do mês)
            [4] - Data final de vigência (último dia do mês)
            [5] - Data de emissão
            [6] - Prêmio líquido
            [7] - Data de vencimento
    """
    dados = []
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Ramo:' in linha:
            ramo = texto[cont]
            ramo = ramo.split(' ')[-1]
            print(f"Ramo: {ramo}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Apólice:' in linha:
            apolice = texto[cont]
            apolice = apolice.split(' ')[1]
            print(f"Apólice: {apolice}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Fatura:' in linha:
            fat = texto[cont]
            fatura = fat.split(' ')[1]
            data = fat.split(' ')[2]
            vencimento = fat.split(' ')[3]
            print(f"Fatura: {fatura}")
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            primeiro_dia = f"01/{mes}/{ano}"
            ultimo_dia_formatado = f"{ultimo_dia}/{mes}/{ano}"
            data_proposta = primeiro_dia
            inicio_vig = primeiro_dia
            fim_vig = ultimo_dia_formatado
            data_emissao = primeiro_dia
            print(f"Vencimento: {vencimento}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Demonstrativo do Prêmio em R$' in linha:
            premio_liquido = texto[cont + 1].rstrip()
            premio_liquido = premio_liquido.split(' ')[-1]
            print(f"Prêmio líquido: {premio_liquido}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Total a Pagar' in linha:
            premio_bruto = texto[cont].rstrip()
            premio_bruto = premio_bruto.split(' ')[-1]
            print(f"Prêmio bruto: {premio_bruto}")
            break
        cont = cont + 1

    dados.append(apolice)
    dados.append(fatura)
    dados.append(data_proposta)
    dados.append(inicio_vig)
    dados.append(fim_vig)
    dados.append(data_emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados