def aig(texto):
    '''
    Extrai informações relevantes de uma fatura da AIG a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF da fatura.

    Returns:
        list: Lista contendo os seguintes dados na ordem:
            [0] - Número da apólice
            [1] - Número do endosso
            [2] - Data inicial de vigência
            [3] - Data inicial de vigência (duplicada)
            [4] - Data final de vigência
            [5] - Data de emissão
            [6] - Prêmio líquido
            [7] - Data de vencimento
    '''
    dados = []
    texto = texto.split('\n')
    cont = 0

    for linha in texto:
        if 'Nº Apólice' in linha:
            apolice = texto[cont + 1].split('Nº Endosso')[0]
            endosso = texto[cont + 2].split()[0]
            print(f"Apolice: {apolice}")
            print(f"Endosso: {endosso}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Vigência' in linha:
            inicio_vigencia = texto[cont + 1].split()[5]
            fim_vigencia = texto[cont + 1].split()[-1]
            print(f"Início Vigência: {inicio_vigencia}")
            print(f"Fim Vigência: {fim_vigencia}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data de Emissão' in linha:
            emissao = texto[cont + 1].split()[0].replace(' ', '')
            print(f"Data de Emissão: {emissao}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Total' in linha:
            premio_liquido = texto[cont + 1].split()[-1].replace('.', '')
            print(f"Prêmio Líquido: {premio_liquido}")
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Valor' in linha:
            vencimento = texto[cont + 1].split()[0].replace(' ', '')
            print(f"Vencimento: {vencimento}")
            break
        cont = cont + 1

    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados