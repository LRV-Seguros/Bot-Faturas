import calendar
import re

 # Dicionário de meses para conversão
meses = {
     "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04",
     "maio": "05", "junho": "06", "julho": "07", "agosto": "08",
     "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
 }

def swiss(texto):
    dados = []
    texto = texto.split('\n')

    print("Primeiras 90 linhas do documento:")
    for i in range(min(90, len(texto))):
        print(f"{i}: {texto[i]}")
    cont = 0

    nome = None
    if len(texto) > 13:
        linha_nome = texto[13]
        nome = linha_nome.strip()
        print(f"Nome extraído: {nome}")

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
            print(f"Ramo extraído: {ramo}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Carga' in linha:
            apolice = texto[cont + 1].strip()
            print(f"Apólice extraída: {apolice}")
            endosso = texto[cont + 2].strip().lstrip('0')
            print(f"Endosso extraído: {endosso}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Modalidade:' in linha:
            emissao = texto[cont + 2].split(' ')[0].strip()
            vigencia = texto[cont + 4].split('.')[0].strip()
            print(f"Emissão extraída: {emissao}")
            data = vigencia
            mes_texto, ano = data.split("/")
            mes = meses[mes_texto.lower()]
            ultimo_dia = calendar.monthrange(int(ano), int(mes))[1]
            inicio_vigencia = f"01/{mes}/{ano}"
            print(f"Início de vigência extraído: {inicio_vigencia}")
            fim_vigencia = f"{ultimo_dia}/{mes}/{ano}"
            print(f"Fim de vigência extraído: {fim_vigencia}")
            break
        cont = cont + 1

    cont = 0
    for linha in texto:
        if 'Prêmio Total (R$):' in linha:
            premio_liquido = texto[cont + 1].split(' ')[-1].strip()
            premio_bruto = texto[cont + 5].split(' ')[-1].strip()
            print(f"Prêmio líquido extraído: {premio_liquido}")
            print(f"Prêmio líquido bruto: {premio_bruto}")
            break
        cont = cont + 1

    vencimento = None
    if len(texto) > 88:
        linha_vencimento = texto[88]
        if "/" in linha_vencimento:
            match = re.search(r'\d{2}/\d{2}/\d{4}', linha_vencimento)
            if match:
                vencimento = match.group(0)
                print(f"Vencimento extraído: {vencimento}")

    dados.append(apolice)
    dados.append(endosso)
    dados.append(inicio_vigencia)
    dados.append(inicio_vigencia)
    dados.append(fim_vigencia)
    dados.append(emissao)
    dados.append(premio_liquido)
    dados.append(vencimento)
    dados.append(nome)

    print(dados)
    return dados