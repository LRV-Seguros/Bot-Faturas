def fairfax(texto):
    dados = []
    texto = texto.split('\n')

    print("Primeiras 90 linhas do documento:")
    for i in range(min(90, len(texto))):
        print(f"{i}: {texto[i]}")
    cont = 0

    nome = None
    if len(texto) > 1:
        linha_nome = texto[1]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

    cont = 0
    for linha in texto:
        if 'Ramo :' in linha:
            ramo = texto[cont]
            ramo = ramo.split('-')[-1]
            print(f"Ramo extraído: {ramo}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Apólice Nº :' in linha:
            apolice = texto[cont]
            apolice = apolice.split(':')[-1].replace(' ', '')
            print(f"Apólice extraída: {apolice}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Endosso Nº:' in linha:
            endosso = texto[cont]
            endosso = endosso.split(':')[-1].replace(' ', '')
            print(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            emissao = texto[cont]
            emissao = emissao.split(' ')[0]
            print(f"Emissão extraída: {emissao}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data de Emissão:' in linha:
            inicio_vig = texto[cont]
            inicio = inicio_vig.find('dia') + 4
            inicio_vigencia = inicio_vig[inicio:inicio + 10]
            inicio_vig = inicio_vig[inicio:]
            inicio = inicio_vig.find('dia') + 4
            fim_vigencia = inicio_vig[inicio:inicio + 10]
            print(f"Início de vigência extraído: {inicio_vigencia}")
            print(f"Fim de vigência extraído: {fim_vigencia}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Líquido' in linha:
            premio = texto[cont + 1][5:]
            inicio = premio.find('R$') + 3
            premio = premio[inicio:]
            fim = premio.find('R$') - 1
            premio_liquido = premio[:fim]
            inicio = premio.rfind('R$') + 3
            print(f"Prêmio líquido extraído: {premio_liquido}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'VENC.' in linha:
            vencimento = texto[cont + 1].rstrip()
            vencimento = vencimento.split(' ')[-1]
            print(f"Vencimento extraído: {vencimento}")
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