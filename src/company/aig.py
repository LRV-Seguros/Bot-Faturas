def aig(texto):
    '''
    Extrai informações relevantes de uma fatura da AIG a partir do linhas do PDF.

    Args:
        linhas (str): linhas completo extraído do PDF da fatura.

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
    linhas = texto.split('\n')
    print("Primeiras 90 linhas do documento:")
    for i in range(min(90, len(linhas))):
        print(f"{i}: {linhas[i]}")
    cont = 0

    nome = None
    if len(linhas) > 30:
        linha_nome = linhas[30]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

    for linha in linhas:
        if 'Nº Apólice' in linha:
            apolice = linhas[cont + 1].split('Nº Endosso')[0]
            endosso = linhas[cont + 2].split()[0]
            print(f"Apolice: {apolice}")
            print(f"Endosso: {endosso}")
            break
        cont = cont + 1

    cont = 0
    for linha in linhas:
        if 'Vigência' in linha:
            inicio_vigencia = linhas[cont + 1].split()[5]
            fim_vigencia = linhas[cont + 1].split()[-1]
            print(f"Início Vigência: {inicio_vigencia}")
            print(f"Fim Vigência: {fim_vigencia}")
            break
        cont = cont + 1

    cont = 0
    for linha in linhas:
        if 'Data de Emissão' in linha:
            emissao = linhas[cont + 1].split()[0].replace(' ', '')
            print(f"Data de Emissão: {emissao}")
            break
        cont = cont + 1

    cont = 0
    for linha in linhas:
        if 'Prêmio Total' in linha:
            premio_liquido = linhas[cont + 1].split()[-1].replace('.', '')
            print(f"Prêmio Líquido: {premio_liquido}")
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Valor' in linha:
            vencimento = linhas[cont + 1].split()[0].replace(' ', '')
            print(f"Vencimento: {vencimento}")
            break
        cont = cont + 1

    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados