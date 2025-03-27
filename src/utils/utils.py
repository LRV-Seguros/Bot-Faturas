"""
Módulo de utilidades gerais para o Bot de Automação de Faturas

Este módulo contém funções utilitárias para manipulação de arquivos,
leitura de PDFs e registro de logs utilizados em todo o sistema.

Autor: Lucelho Silva
"""
import os
import re
from PyPDF2 import PdfReader
from datetime import datetime

def remover_arquivos(lista_documentos):
    """
    Remove todos os arquivos listados na lista de documentos após processamento.

    Args:
        lista_documentos (list): Lista contendo listas de caminhos de arquivos a serem removidos
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
    Remove caracteres inválidos de nomes de arquivos para evitar problemas no sistema de arquivos.

    Args:
        filename (str): Nome do arquivo a ser sanitizado

    Returns:
        str: String com o nome do arquivo sanitizado
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def ler_pdf_completo(nome_arquivo):
    """
    Lê o conteúdo completo de um arquivo PDF e extrai o texto.

    Args:
        nome_arquivo (str): Caminho para o arquivo PDF

    Returns:
        str: String com o texto completo extraído do PDF
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
    Registra a inserção de uma fatura no arquivo de log principal.

    Args:
        nome_arquivo (str): Nome do arquivo de log
        dados (list): Dados da fatura processada
    """
    with open(nome_arquivo, "a") as arquivo:
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        if dados:
            arquivo.write(fr'Inserida a fatura da apolice {dados[0]} no dia {data_formatada}' + "\n")

def registrar_error(nome_arquivo, seguradora, apolice, endosso, nome=None, erro="Erro desconhecido"):
    """
    Registra um erro no arquivo de log centralizado para posterior notificação.

    Args:
        nome_arquivo (str): Nome do arquivo de log centralizado
        seguradora (str): Nome da seguradora
        apolice (str): Número da apólice
        endosso (str): Número do endosso
        nome (str, optional): Nome do segurado
        erro (str, optional): Mensagem de erro. Padrão é "Erro desconhecido".
    """
    with open(nome_arquivo, "a") as arquivo:
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S")

        msg = f"[{data_formatada}] ERRO - "

        if nome:
            msg += f"Nome: {nome} - "

        msg += f"Seguradora: {seguradora} - Apolice: {apolice} - Endosso: {endosso} - Erro: {erro}\n"

        arquivo.write(msg)