meses = {
     "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
     "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
     "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
 }

def axa(texto):
    dados = []
    texto = texto.split('\n')

    print("Primeiras 90 texto do documento:")
    for i in range(min(90, len(texto))):
        print(f"{i}: {texto[i]}")
    cont = 0

    nome = None
    if len(texto) > 39:
        linha_nome = texto[39]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        print(f"Nome extraído: {nome}")

    cont = 0
    for linha in texto:
        if 'Nomenclatura de Ramo e Produto' in linha:
            ramo = texto[cont + 1].split(' ')[-1]
            print(f"Ramo extraído: {ramo}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Nº pedido de endosso' in linha:
            endosso = ''
            end = texto[cont + 1].split(' ')[0]
            for char in end:
                if char.isdigit():
                    endosso = endosso + char
            print(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Início de Vigência:' in linha:
            end = texto[cont + 1].split(' ')
            for e in end:
                if '/' in e:
                    inicio_vigencia = e[:10]
            print(f"Início de vigência extraído: {inicio_vigencia}")
            end = texto[cont + 2].split(' ')
            for e in end:
                if '/' in e:
                    fim_vigencia = e[:10]
            print(f"Fim de vigência extraído: {fim_vigencia}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Data da Emissão' in linha:
            end = texto[cont + 1].find('Número da apólice')
            emissao = texto[cont + 1][:end]
            if 'de' in emissao:
                partes = emissao.split(" de ")
                dia = partes[0].split(' ')[-1]
                mes = meses[partes[1].lower()]
                ano = partes[2]
                emissao = f"{dia}/{mes}/{ano}"

            print(f"Emissão extraída: {emissao}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Nº Apólice averbação' in linha:
            end = texto[cont].find('Nº Apólice averbação')
            apolice = texto[cont][:end]
            print(f"Apólice extraída: {apolice}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Líquido' in linha:
            premio_liquido = texto[cont].split(' ')[-1]
            print(f"Prêmio líquido extraído: {premio_liquido}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Total' in linha:
            premio_bruto = texto[cont].split(' ')[-1]
            print(f"Prêmio bruto: {premio_bruto}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Vencimento:' in linha:
            vencimento = texto[cont + 1].split(' ')[1]
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

def axa_b(texto):
    """
     Extrai informações relevantes de uma fatura da AXA (formato alternativo) a partir do texto do PDF.

     Args:
         texto (str): texto completo extraído do PDF

     Returns:
         list: Lista contendo os dados formatados na ordem requerida para cadastro
    """
    dados = []
    texto = texto.split('\n')

    print("Primeiras 90 texto do documento:")
    for i in range(min(90, len(texto))):
        print(f"{i}: {texto[i]}")

    nome = None
    if len(texto) > 39:
        linha_nome = texto[39]
        nome = linha_nome.strip().replace(' MECNPJ', '')
        print(f"Nome extraído: {nome}")

    cont = 0
    for linha in texto:
        if 'Endosso:' in linha:
            endosso = texto[cont+1]
            print(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
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
                print(f"Início de vigência extraído: {inicio_vigencia}")
                print(f"Fim de vigência extraído: {fim_vigencia}")
            except:
                pass
            break
        cont = cont + 1

    cont = 0
    emissao = texto[0]
    partes = emissao.split(" ")
    dia = partes[0]
    mes = meses[partes[1].lower()]
    ano = partes[2]
    emissao = f"{dia}/{mes}/{ano}"
    print(f"Emissão extraída: {emissao}")

    cont = 0
    for linha in texto:
        if 'www.axa.com.brOuvidoriaApólice' in linha:
            apolice = texto[cont + 1]
            print(f"Apólice extraída: {apolice}")
            break
        cont = cont + 1
    cont = 0

    for linha in texto:
        if 'Pagamento:Moeda: R$' in linha:
            premio_liquido = texto[cont].split(' ')[-2]
            premio_liquido.replace('.', '')
            print(f"Prêmio líquido extraído: {premio_liquido}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'PRÊMIO TOTAL' in linha:
            venc = texto[cont + 1].split(' ')
            for v in venc:
                if '/' in v:
                    vencimento = v
                    break
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