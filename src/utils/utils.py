import os
import re
from PyPDF2 import PdfReader
from datetime import datetime


def remover_arquivos(lista_documentos):
    """
    Remove todos os arquivos listados na lista de documentos.

    Args:
        lista_documentos: Lista contendo listas de caminhos de arquivos a serem removidos
    """
    for documento in lista_documentos:
        for doc in documento:
            try:
                os.remove(doc)
                print(f"O arquivo {doc} foi removido com sucesso.")
            except:
                print(f"O arquivo {doc} não foi localizado para remoção")

def sanitize_filename(filename):
    """
    Remove caracteres inválidos de nomes de arquivos.

    Args:
        filename: Nome do arquivo a ser sanitizado

    Returns:
        String com o nome do arquivo sanitizado
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def ler_pdf_completo(nome_arquivo):
    """
    Lê o conteúdo completo de um arquivo PDF.

    Args:
        nome_arquivo: Caminho para o arquivo PDF

    Returns:
        String com o texto completo extraído do PDF
    """
    with open(nome_arquivo, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        texto_completo = ""

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            texto_completo += page.extract_text()

    return texto_completo

def registrar_fatura(nome_arquivo, dados):
    """
    Registra a inserção de uma fatura no arquivo de log.

    Args:
        nome_arquivo: Nome do arquivo de log
        dados: Dados da fatura processada
    """
    with open(nome_arquivo, "a") as arquivo:
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        if dados:
            arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")