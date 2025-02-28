import calendar

# Dicionário de meses para conversão
meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

def swiss(texto):
    dados = []
    texto = texto.split('\n')

    # Buscando o ramo (não usado no preenchimento, mas mantido para debug)
    cont = 0
    for linha in texto:
        if 'Nº da Proposta:' in linha:
            ramo = ''
            ram = ''
            teste = texto[cont + 1] + ' ' + texto[cont + 2]
            for t in teste.split(' '):
                if t[0].isalpha():
                    ram = ram + t[0]
            for r in ram:
                if r.isupper():
                    ramo = ramo + r
            print(ramo)
            break
        cont = cont + 1

    # Buscando número da apólice, endosso e proposta
    cont = 0
    for linha in texto:
        if 'Carga' in linha:
            apolice = texto[cont + 1].strip()
            endosso = texto[cont + 2].strip()
            # Mantido para referência, mas não usado
            n_proposta = texto[cont + 3].strip()
            dados.append(apolice)  # dados[0] - N° apólice coletiva
            dados.append(endosso)  # dados[1] - N° endosso
            break
        cont = cont + 1

    # Buscando datas de vigência e emissão
    cont = 0
    for linha in texto:
        if 'Modalidade:' in linha:
            emissao = texto[cont + 2].split(' ')[0].strip()
            vigencia = texto[cont + 4].split('.')[0].strip()
            print(emissao)
            print(vigencia)

            # Processando a data de vigência
            data = vigencia
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            primeiro_dia = f"01/{mes}/{ano}"
            ultimo_dia_formatado = f"{ultimo_dia}/{mes}/{ano}"

            # Adicionando as datas na ordem correta
            # dados[2] - Data da proposta (usando data de emissão)
            dados.append(emissao)
            dados.append(primeiro_dia)  # dados[3] - Data inicial vigência
            # dados[4] - Data inicial vigência (duplicada)
            dados.append(primeiro_dia)
            # dados[5] - Data final vigência
            dados.append(ultimo_dia_formatado)
            dados.append(emissao)  # dados[6] - Data emissão
            break
        cont = cont + 1

    # Buscando prêmio líquido
    cont = 0
    for linha in texto:
        if 'Prêmio Total (R$):' in linha:
            premio_liquido = texto[cont + 1].split(' ')[-1].strip()
            premio_bruto = texto[cont + 5].split(' ')[-1].strip()
            print(premio_liquido)
            dados.append(premio_liquido)  # dados[7] - Prêmio líquido
            print(premio_bruto)
            break
        cont = cont + 1

    # Buscando data de vencimento
    cont = 0
    for linha in texto:
        if 'CONDIÇÕES GERAIS' in linha:
            vencimento = texto[cont - 1].strip()
            print(vencimento)
            dados.append(vencimento)  # dados[8] - Data vencimento
            break
        cont = cont + 1

    print(dados)

    return dados