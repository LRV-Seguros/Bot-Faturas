def fairfax(texto):
    """
    Extrai informações relevantes de uma fatura da Fairfax a partir do texto do PDF.

    Args:
        texto (str): Texto completo extraído do PDF da fatura

    Returns:
        list: Lista contendo os seguintes dados na ordem:
            [0] - Número da apólice
            [1] - Número do endosso
            [2] - Data da proposta (usando data de emissão)
            [3] - Data inicial de vigência
            [4] - Data inicial de vigência (duplicada)
            [5] - Data final de vigência
            [6] - Data de emissão
            [7] - Prêmio líquido
            [8] - Data de vencimento
    """
    dados = []
    texto = texto.split('\n')
    cont = 0

    # Busca e armazena o ramo (para referência)
    for linha in texto:
        if 'Ramo :' in linha:
            ramo = texto[cont]
            ramo = ramo.split('-')[-1]
            print(f"Ramo: {ramo}")
            break
        cont = cont + 1

    # Busca e armazena o número da apólice
    cont = 0
    for linha in texto:
        if 'Apólice Nº :' in linha:
            apolice = texto[cont]
            apolice = apolice.split(':')[-1].replace(' ', '')
            print(f"Apólice: {apolice}")
            break
        cont = cont + 1

    # Busca e armazena o número do endosso
    cont = 0
    for linha in texto:
        if 'Endosso Nº:' in linha:
            endosso = texto[cont]
            endosso = endosso.split(':')[-1].replace(' ', '')
            print(f"Endosso: {endosso}")
            break
        cont = cont + 1

    # Busca e armazena a data de emissão primeiro
    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            emissao = texto[cont]
            emissao = emissao.split(' ')[0]
            print(f"Data de Emissão: {emissao}")
            break
        cont = cont + 1

    # Busca e armazena as datas de vigência
    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            inicio_vig = texto[cont]
            inicio = inicio_vig.find('dia') + 4
            inicio_vigencia = inicio_vig[inicio:inicio + 10]
            inicio_vig = inicio_vig[inicio:]
            inicio = inicio_vig.find('dia') + 4
            fim_vigencia = inicio_vig[inicio:inicio + 10]
            print(f"Início Vigência: {inicio_vigencia}")
            print(f"Fim Vigência: {fim_vigencia}")
            break
        cont = cont + 1

    # Busca e armazena o prêmio líquido
    cont = 0
    for linha in texto:
        if 'Prêmio Líquido' in linha:
            premio = texto[cont + 1][5:]
            inicio = premio.find('R$') + 3
            premio = premio[inicio:]
            fim = premio.find('R$') - 1
            premio_liquido = premio[:fim]
            inicio = premio.rfind('R$') + 3
            premio_bruto = premio[inicio:]
            print(f"Prêmio Líquido: {premio_liquido}")

            break
        cont = cont + 1

    # Busca e armazena a data de vencimento
    cont = 0
    for linha in texto:
        if 'VENC.' in linha:
            vencimento = texto[cont + 1].rstrip()
            vencimento = vencimento.split(' ')[-1]
            print(f"Vencimento: {vencimento}")

            break
        cont = cont + 1

    dados.append(apolice)
    dados.append(endosso)
    dados.append(emissao)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(premio_liquido)
    dados.append(vencimento)

    print(dados)
    return dados