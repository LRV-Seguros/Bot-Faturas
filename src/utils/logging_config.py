import logging
import os
from datetime import datetime

def setup_logging():
    """
    Configura o sistema de logging da aplicação.

    Returns:
        Um objeto logger configurado
    """
    # Garantir que o diretório de logs existe
    log_dir = "./src/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Definir o nome do arquivo de log com a data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"fatura_{data_atual}.log")

    # Configurar o formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )

    # Configurar o handler de arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Configurar o handler de console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Configurar o logger
    logger = logging.getLogger('fatura_bot')
    logger.setLevel(logging.INFO)

    # Adicionar os handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger