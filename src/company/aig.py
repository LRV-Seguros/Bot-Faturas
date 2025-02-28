def aig(texto):

    texto = texto.split('\n')
    cont = 0

    for linha in texto:
        if 'Nº Apólice' in linha:
            apolice = texto[cont + 1].split('Nº Endosso')[0]
            endosso = texto[cont + 2].split()[0]
            print(apolice)
            print(endosso)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Vigência' in linha:
            inicio_vigencia = texto[cont + 1].split()[5]
            fim_vigencia = texto[cont + 1].split()[-1]
            print(inicio_vigencia)
            print(fim_vigencia)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data de Emissão' in linha:
            emissao = texto[cont + 1].split()[0].replace(' ', '')
            print(emissao)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Total' in linha:
            premio_liquido = texto[cont + 1].split()[-1].replace('.', '')
            print(premio_liquido)
            break
        cont = cont + 1
    cont = 0
    for linha in texto:
        if 'Valor' in linha:
            vencimento = texto[cont + 1].split()[0].replace(' ', '')
            print(vencimento)
            break
        cont = cont + 1
    dados = []
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