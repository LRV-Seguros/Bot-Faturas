meses = {
     "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
     "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
     "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
 }

def axa(texto):
    dados = []
    linhas = texto.split('\n')

    print("Primeiras 90 linhas do documento:")
    for i in range(min(90, len(linhas))):
        print(f"{i}: {linhas[i]}")
    cont = 0

    nome = None
    if len(linhas) > 39:
        linha_nome = linhas[39]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        print(f"Nome extraído: {nome}")

    cont = 0
    for linha in linhas:
        if 'Nomenclatura de Ramo e Produto' in linha:
            ramo = linhas[cont + 1].split(' ')[-1]
            print(ramo)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Nº pedido de endosso' in linha:
            endosso = ''
            end = linhas[cont + 1].split(' ')[0]
            for char in end:
                if char.isdigit():
                    endosso = endosso + char
            print(endosso)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Início de Vigência:' in linha:
            end = linhas[cont + 1].split(' ')
            for e in end:
                if '/' in e:
                    inicio_vigencia = e[:10]
            print(inicio_vigencia)
            end = linhas[cont + 2].split(' ')
            for e in end:
                if '/' in e:
                    fim_vigencia = e[:10]
            print(fim_vigencia)
            break
        cont = cont + 1

    cont = 0
    for linha in linhas:
        if 'Data da Emissão' in linha:
            end = linhas[cont + 1].find('Número da apólice')
            emissao = linhas[cont + 1][:end]
            if 'de' in emissao:
                partes = emissao.split(" de ")
                dia = partes[0].split(' ')[-1]
                mes = meses[partes[1].lower()]  # Converter o mês para minúsculo para evitar problemas
                ano = partes[2]
                emissao = f"{dia}/{mes}/{ano}"

            print(emissao)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Nº Apólice averbação' in linha:
            end = linhas[cont].find('Nº Apólice averbação')
            apolice = linhas[cont][:end]
            print(apolice)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Prêmio Líquido' in linha:
            premio_liquido = linhas[cont].split(' ')[-1]
            print(premio_liquido)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Prêmio Total' in linha:
            premio_bruto = linhas[cont].split(' ')[-1]
            print(premio_bruto)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Vencimento:' in linha:
            vencimento = linhas[cont + 1].split(' ')[1]
            print(vencimento)
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

def axa_b(texto):
    """
     Extrai informações relevantes de uma fatura da AXA (formato alternativo) a partir do linhas do PDF.

     Args:
         linhas (str): linhas completo extraído do PDF

     Returns:
         list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    linhas = texto.split('\n')

    print("Primeiras 90 linhas do documento:")
    for i in range(min(90, len(linhas))):
        print(f"{i}: {linhas[i]}")

    nome = None
    if len(linhas) > 39:
        linha_nome = linhas[39]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        print(f"Nome extraído: {nome}")

    cont = 0
    for linha in linhas:
        if 'Endosso:' in linha:
            endosso = linhas[cont+1]
            print(endosso)
            break
        cont = cont + 1
    cont = 0
    for linha in linhas:
        if 'Endosso:' in linha:
            vig = linha.split(' ')
            for v in vig:
                if '/' in v:
                    inicio_vigencia = v
                    break
            for v in vig:
                if '/' in v and 'Fim' in v:
                    fim = v.find('Fim')
                    fim_vigencia = v[:fim]
                    break

            try:
                print(inicio_vigencia)
                print(fim_vigencia)
            except:
                pass
            break
        cont = cont + 1

    cont = 0
    emissao = linhas[0]
    partes = emissao.split(" ")
    dia = partes[0]
    mes = meses[partes[1].lower()]
    ano = partes[2]
    emissao = f"{dia}/{mes}/{ano}"
    print(emissao)

    cont = 0
    for linha in linhas:
        if 'www.axa.com.brOuvidoriaApólice' in linha:
            apolice = linhas[cont + 1]
            print(apolice)
            break
        cont = cont + 1
    cont = 0

    for linha in linhas:
        if 'Pagamento:Moeda: R$' in linha:
            premio_liquido = linhas[cont].split(' ')[-2]
            premio_liquido.replace('.', '')
            print(premio_liquido)
            break
        cont = cont + 1

    cont = 0
    for linha in linhas:
        if 'PRÊMIO TOTAL' in linha:
            venc = linhas[cont + 1].split(' ')
            for v in venc:
                if '/' in v:
                    vencimento = v
                    break
            print(vencimento)
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