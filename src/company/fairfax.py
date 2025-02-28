def fairfax(texto):
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
            dados.append(apolice)  # dados[0] - número da apólice
            break
        cont = cont + 1

    # Busca e armazena o número do endosso
    cont = 0
    for linha in texto:
        if 'Endosso Nº:' in linha:
            endosso = texto[cont]
            endosso = endosso.split(':')[-1].replace(' ', '')
            print(f"Endosso: {endosso}")
            dados.append(endosso)  # dados[1] - número do endosso
            break
        cont = cont + 1

    # Busca e armazena a data de emissão primeiro
    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            emissao = texto[cont]
            emissao = emissao.split(' ')[0]
            print(f"Data de Emissão: {emissao}")
            dados.append(emissao)  # dados[2] - data da proposta (usando data de emissão)
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
            dados.append(inicio_vigencia)  # dados[3] - data inicial vigência
            dados.append(inicio_vigencia)  # dados[4] - data inicial vigência (duplicada)
            dados.append(fim_vigencia)     # dados[5] - data final vigência
            dados.append(emissao)          # dados[6] - data emissão
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
            dados.append(premio_liquido)  # dados[7] - prêmio líquido
            break
        cont = cont + 1

    # Busca e armazena a data de vencimento
    cont = 0
    for linha in texto:
        if 'VENC.' in linha:
            vencimento = texto[cont + 1].rstrip()
            vencimento = vencimento.split(' ')[-1]
            print(f"Vencimento: {vencimento}")
            dados.append(vencimento)  # dados[8] - data vencimento
            break
        cont = cont + 1

    print(dados)
    return dados