def berkley(texto):
    """
    Extrai informações relevantes de uma fatura da Berkley a partir do texto do PDF.

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

    # Busca ramo e proposta
    for linha in texto:
        if 'Ramo' in linha:
            ramo = texto[cont + 1][3:].rstrip().split(' ')[1]
            proposta = texto[cont + 1][3:].rstrip().split(' ')[3]
            print(f"Ramo: {ramo}")
            print(f"Proposta: {proposta}")
            break
        cont = cont + 1

    # Extrai apólice, endosso e emissão
    apolice = texto[2].split(' ')[4]
    endosso = texto[2].split(' ')[5]
    emissao = texto[2].split(' ')[-1]
    print(f"Apólice: {apolice}")
    print(f"Endosso: {endosso}")
    print(f"Emissão: {emissao}")

    # Busca datas de vigência
    cont = 0
    for linha in texto:
        if 'VIGÊNCIA' in linha:
            inicio_vig = ''
            fim_vig = ''
            vig = texto[cont + 1].split(' ')
            for v in vig:
                if '/' in v:
                    if inicio_vig == '':
                        inicio_vig = v
                    else:
                        fim_vig = v
            print(f"Início vigência: {inicio_vig}")
            print(f"Fim vigência: {fim_vig}")
            break
        cont = cont + 1

    # Busca prêmio líquido
    for linha in texto:
        if 'Prêmio Líquido:' in linha:
            premio_liquido = linha.split(' ')[-1]
            print(f"Prêmio líquido: {premio_liquido}")
            break

    # Busca prêmio total (mantido para referência)
    for linha in texto:
        if 'Prêmio Total:' in linha:
            premio_total = linha.split(' ')[-1]
            print(f"Prêmio total: {premio_total}")
            break

    # Busca vencimento
    for linha in texto:
        if 'Vencimentos:' in linha:
            vencimento = linha.split(' ')[-1]
            print(f"Vencimento: {vencimento}")
            break

    dados.append(apolice)
    dados.append(endosso)
    dados.append(emissao)
    dados.append(inicio_vig)
    dados.append(fim_vig)
    dados.append(emissao)
    dados.append(premio_liquido)

    print(dados)
    return dados