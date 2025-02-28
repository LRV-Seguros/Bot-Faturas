import calendar

# Dicionário de meses para conversão
meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
    "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

def sura(texto):
    dados = []
    texto = texto.split('\n')
    cont = 0
    for linha in texto:
        if 'Ramo:' in linha:
            ramo = texto[cont]
            ramo = ramo.split(' ')[-1]
            print(ramo)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Apólice:' in linha:
            apolice = texto[cont]
            apolice = apolice.split(' ')[1]
            print(apolice)
            dados.append(apolice)
            break
        cont = cont + 1


    cont = 0
    for linha in texto:
        if 'Fatura:' in linha:
            fat = texto[cont]
            fatura = fat.split(' ')[1]
            data = fat.split(' ')[2]
            vencimento = fat.split(' ')[3]
            print(fatura)
            dados.append(fatura)
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            primeiro_dia = f"01/{mes}/{ano}"
            ultimo_dia_formatado = f"{ultimo_dia}/{mes}/{ano}"
            data_proposta = primeiro_dia
            dados.append(data_proposta)
            inicio_vig = primeiro_dia
            dados.append(inicio_vig)
            fim_vig = ultimo_dia_formatado
            dados.append(fim_vig)
            data_emissao = primeiro_dia
            dados.append(data_emissao)
            print(vencimento)
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Demonstrativo do Prêmio em R$' in linha:
            premio_liquido = texto[cont + 1].rstrip()
            #print(premio_liquido)
            premio_liquido = premio_liquido.split(' ')[-1]

            print(premio_liquido)
            dados.append(premio_liquido)
            break
        cont = cont + 1
    dados.append(vencimento)
    cont = 0
    for linha in texto:
        if 'Total a Pagar' in linha:
            premio_bruto = texto[cont].rstrip()
            premio_bruto = premio_bruto.split(' ')[-1]

            print(premio_bruto)
            break
        cont = cont + 1
    print(dados)

    # Garantir que os dados estejam na ordem esperada
    dados = [apolice, fatura, data_proposta, inicio_vig, fim_vig, data_emissao, premio_liquido, vencimento]
    return dados