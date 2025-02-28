import calendar

# Dicionário de meses para conversão
meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

def sompo(texto):
    dados = []
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Apólice' in linha:
            apolice = texto[cont + 1]
            dados.append(apolice)
            print(apolice)
            break
        cont = cont + 1
    inicio = texto[cont + 2].find('/') + 5
    fim = texto[cont + 2].find('CONTA')
    fatura = texto[cont + 2][inicio:fim]
    dados.append(fatura)
    print(fatura)
    data = texto[cont + 2][:inicio]
    mes, ano = map(int, data.split("/"))
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    data_proposta = fr'01/{data}'
    inicio_vig = data_proposta
    fim_vig = fr'{ultimo_dia}/{data}'
    dados.append(data_proposta)
    dados.append(inicio_vig)
    dados.append(fim_vig)

    print(data_proposta + '\n' + inicio_vig + '\n' + fim_vig)
    cont = 0
    for linha in texto:
        if 'Local e Data' in linha:
            data = texto[cont - 2]
            print(data)
            inicio = data.find(',') + 2
            data = data[inicio:]
            #data = data.split(' ')[0]
            partes = data.split(" de ")
            dia = partes[0].split(' ')[-1]
            mes = meses[partes[1].lower()]  # Converter o mês para minúsculo para evitar problemas
            ano = partes[2]
            data_emissao = f"{dia}/{mes}/{ano}"
            dados.append(data_emissao)
            print(data_emissao)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'PRÊMIO LÍQUIDO' in linha:
            premio_liquido = texto[cont + 3].split(' ')[1]
            ramo = texto[cont + 1]
            print(ramo)
            fim = premio_liquido.find(',') + 3
            premio_liquido = premio_liquido[:fim].replace('.', '')
            print(premio_liquido)
            dados.append(premio_liquido)
            break
        cont = cont + 1

    premio_bruto = texto[cont + 3].split(' ')[0]
    print(premio_bruto)
    cont = 0
    for linha in texto:
        if 'LIMITE PAGTO' in linha:
            data_limite = texto[cont + 1]
            fim = data_limite.find('/') + 8
            data_limite = data_limite[:fim]
            print(data_limite)
            dados.append(data_limite)
            break
        cont = cont + 1

    print(dados)
    return dados