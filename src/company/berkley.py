def berkley(texto):
    dados = []
    texto = texto.split('\n')
    cont = 0

    for i in range(min(90, len(texto))):
        print(f"{i}: {texto[i]}")

    nome = None
    if len(texto) > 30:
        linha_nome = texto[30]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

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

    # Adiciona apólice e endosso
    dados.append(apolice)      # dados[0] - número da apólice
    dados.append(endosso)      # dados[1] - número do endosso
    dados.append(emissao)      # dados[2] - data da proposta (usando data de emissão)

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

    # Adiciona vigências e emissão
    dados.append(inicio_vig)   # dados[3] - data inicial vigência
    dados.append(inicio_vig)   # dados[4] - data inicial vigência (duplicada)
    dados.append(fim_vig)      # dados[5] - data final vigência
    dados.append(emissao)      # dados[6] - data emissão

    # Busca prêmio líquido
    for linha in texto:
        if 'Prêmio Líquido:' in linha:
            premio_liquido = linha.split(' ')[-1]
            print(f"Prêmio líquido: {premio_liquido}")
            dados.append(premio_liquido)  # dados[7] - prêmio líquido
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
            dados.append(vencimento)  # dados[8] - data vencimento
            break

    dados.append(nome)

    print("Dados compilados:", dados)
    return dados