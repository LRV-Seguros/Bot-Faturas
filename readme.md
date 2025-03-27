# Documentação do Sistema de Automação de Processamento de Faturas

## Sumário
1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Fluxo de Processamento](#fluxo-de-processamento)
5. [Componentes Principais](#componentes-principais)
   - [Módulo de Processamento de E-mails](#módulo-de-processamento-de-e-mails)
   - [Módulo de Extração de Dados de PDFs](#módulo-de-extração-de-dados-de-pdfs)
   - [Módulo de Automação Web](#módulo-de-automação-web)
   - [Módulo de Notificação de Erros](#módulo-de-notificação-de-erros)
6. [Configurações](#configurações)
7. [Segurança](#segurança)
8. [Logging](#logging)
9. [Tratamento de Erros](#tratamento-de-erros)
10. [Guia de Execução](#guia-de-execução)
11. [Manutenção e Suporte](#manutenção-e-suporte)
12. [Troubleshooting](#troubleshooting)
13. [Glossário](#glossário)

## Visão Geral

O Sistema de Automação de Processamento de Faturas é uma solução desenvolvida para automatizar o fluxo de processamento de faturas de seguradoras. O sistema realiza as seguintes operações:

1. Acessa um e-mail corporativo para baixar faturas enviadas por seguradoras
2. Extrai dados relevantes de documentos PDF (faturas, endossos, etc.)
3. Insere esses dados no sistema da corretora através de automação web
4. Anexa os documentos originais no sistema
5. Notifica erros e exceções via WhatsApp

O sistema suporta múltiplas seguradoras, incluindo Swiss, Fairfax, Sura, Sompo, AXA, AIG, Berkley e Chubb, cada uma com seu próprio formato de documento e regras de extração.

## Arquitetura

O sistema segue uma arquitetura modular baseada em componentes Python, com as seguintes camadas:

![Arquitetura do Sistema](./src/assets/img/arquitetura_sistema_automacao.svg "Arquitetura do Sistema")

1. **Camada de Entrada de Dados**: Responsável pela aquisição de dados através de e-mails.
2. **Camada de Processamento**: Contém a lógica de negócio para extração e transformação de dados dos PDFs.
3. **Camada de Automação**: Implementa a interação automatizada com sistemas web externos.
4. **Camada de Notificação**: Gerencia o envio de notificações e alertas.
5. **Camada de Utilitários**: Fornece funcionalidades compartilhadas como logging, manipulação de arquivos, etc.

## Estrutura do Projeto

```
├── downloaded_files                    # Diretório para arquivos temporários baixados
│   ├── driver_fixing.lock              # Arquivo de lock para evitar múltiplas instâncias do driver
│   └── pyautogui.lock                  # Arquivo de lock para operações do PyAutoGUI
├── error_log.txt                       # Registro centralizado de erros
├── executar_automacao.bat              # Script para execução no Windows
├── main.py                             # Ponto de entrada principal da aplicação
├── requirements.txt                    # Dependências do projeto
└── src                                 # Código-fonte da aplicação
    ├── .gitignore                      # Arquivos ignorados pelo controle de versão
    ├── assets                          # Recursos estáticos
    │   └── img                         # Imagens e diagramas
    │       └── arquitetura_sistema_automacao.svg  # Diagrama de arquitetura
    ├── company                         # Processadores específicos por seguradora
    │   ├── __init__.py                 # Torna o diretório um pacote Python
    │   ├── aig.py                      # Extração de dados da AIG
    │   ├── axa.py                      # Extração de dados da AXA
    │   ├── berkley.py                  # Extração de dados da Berkley
    │   ├── chubb.py                    # Extração de dados da Chubb
    │   ├── fairfax.py                  # Extração de dados da Fairfax
    │   ├── sompo.py                    # Extração de dados da Sompo
    │   ├── sura.py                     # Extração de dados da Sura
    │   ├── swiss.py                    # Extração de dados da Swiss
    │   └── teste                       # Subprocessadores para tipos específicos
    │       ├── __init__.py             # Torna o subdiretório um pacote Python
    │       ├── chubb_internacional.py  # Processador para Chubb Internacional
    │       ├── chubb_nacional.py       # Processador para Chubb Nacional
    │       ├── chubb_rcf.py            # Processador para Chubb RCF
    │       ├── chubb_rct.py            # Processador para Chubb RCT
    │       └── chubb_rctr.py           # Processador para Chubb RCTR-C
    ├── config                          # Configurações do sistema
    │   ├── __init__.py                 # Torna o diretório um pacote Python
    │   └── settings.py                 # Configurações e credenciais
    ├── logs                            # Diretório para armazenamento de logs
    │   └── .gitkeep                    # Mantém diretório vazio no Git
    ├── services                        # Serviços compartilhados
    │   ├── __init__.py                 # Torna o diretório um pacote Python
    │   ├── email_handler.py            # Serviço de acesso a e-mails
    │   ├── error_notification.py       # Serviço de notificação de erros
    │   └── web_automation.py           # Serviço de automação web
    └── utils                           # Utilitários compartilhados
        ├── __init__.py                 # Torna o diretório um pacote Python
        ├── logging_config.py           # Configuração de logs
        ├── utils.py                    # Funções utilitárias gerais
        └── whatsapp_notifier.py        # Utilitário de notificação WhatsApp
```

## Fluxo de Processamento

O fluxo completo de processamento segue estas etapas:

1. **Inicialização**:
   - Configuração de logs
   - Carregamento de faturas já processadas
   - Inicialização do driver de navegador

2. **Processamento de E-mails**:
   - Login no sistema de e-mail
   - Identificação de e-mails não lidos
   - Download de anexos
   - Armazenamento local dos anexos
   - Arquivamento dos e-mails processados

3. **Processamento de Documentos**:
   - Para cada documento baixado:
     - Identificação da seguradora
     - Extração de texto do PDF
     - Processamento do texto usando o módulo específico da seguradora
     - Extração de dados relevantes (apólice, endosso, datas, valores)

4. **Automação de Cadastro**:
   - Login no sistema da corretora (Corretor Online)
   - Navegação até a área de propostas
   - Busca por apólice
   - Preenchimento de formulário com dados extraídos
   - Anexação de documentos originais
   - Salvamento das alterações

5. **Finalização**:
   - Remoção de arquivos temporários
   - Verificação de erros
   - Envio de notificações se necessário

## Componentes Principais

### Módulo de Processamento de E-mails

Localizado em `src/services/email_handler.py`, este módulo:

- Realiza login na caixa de e-mail
- Processa e-mails não lidos
- Baixa anexos relevantes
- Arquiva e-mails após processamento

#### Funções principais:
- `baixar_emails()`: Função principal que coordena o acesso e processamento de e-mails
- `_arquivar_emails()`: Função interna que arquiva e-mails após processamento

### Módulo de Extração de Dados de PDFs

Localizado nos arquivos dentro de `src/company/`, este módulo contém processadores específicos para cada seguradora:

- Cada arquivo (swiss.py, fairfax.py, etc.) implementa a lógica de extração específica
- Os processadores extraem dados como número de apólice, endosso, datas e valores
- A extração utiliza expressões regulares e análise de texto estruturada

Exemplo de função de extração:
```python
def swiss(texto):
    # Extrai informações relevantes de uma fatura da Swiss
    dados = []
    # Processamento do texto
    # ...
    return dados  # Lista com os dados extraídos
```

### Módulo de Automação Web

Localizado em `src/services/web_automation.py`, este módulo:

- Acessa o sistema da corretora (Corretor Online)
- Navega entre telas
- Preenche formulários com dados extraídos
- Anexa documentos originais
- Implementa tratamento de timeout e exceções

#### Função principal:
- `quiver()`: Gerencia toda a automação web, desde login até o cadastro completo de faturas

### Módulo de Notificação de Erros

Localizado em `src/services/error_notification.py`, este módulo:

- Monitora erros ocorridos durante o processamento
- Formata mensagens de erro
- Envia notificações via WhatsApp usando Selenium
- Implementa lógica para evitar notificações duplicadas

#### Funções principais:
- `notificar_erros()`: Ponto de entrada para o processo de notificação
- `enviar_notificacoes_erros()`: Coordena o envio de múltiplas notificações
- `enviar_mensagem_whatsapp()`: Envia mensagens individuais via WhatsApp Web

## Configurações

As configurações do sistema estão centralizadas em `src/config/settings.py`:

```python
# Credenciais
CORRETOR_ONLINE = {
    'corretora': ' ',
    'login': ' ',
    'senha': ' '
}

EMAIL = {
    'url': ' ',
    'usuario': ' ',
    'senha': ' '
}

# URLs
CORRETOR_URL = ' '

# Configurações de processamento
TIPO_SEGURADORA = {
    'swiss': ,
    'fairfax': ,
    'berkley': ,
    'sura': ,
    'sompo': ,
    'axa': ,
    'aig': ,
    'chubb': 
}

# Configurações de arquivos
LOG_FILE = ' '
ERROR_LOG_FILE = ' '

# Configurações de notificação
ADMIN_PHONE = ' '  # Número do administrador para receber notificações de erro
```

## Logging

O sistema utiliza o módulo de logging do Python, configurado em `src/utils/logging_config.py`:

- Logs são gerados diariamente com nome `fatura_YYYY-MM-DD.log`
- Erros são registrados em `error_log.txt`
- Os logs incluem timestamp, nível de log, mensagem e, para erros, stacktrace
- Os logs são exibidos no console e salvos em arquivo

Exemplo de configuração:
```python
def setup_logging():
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

    # Configurar os handlers
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

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
```

## Tratamento de Erros

O sistema implementa tratamento de erros em múltiplas camadas:

1. **Try/Except**: Blocos de tratamento em cada etapa crítica do processo
2. **Timeout**: Mecanismo de timeout para operações demoradas
3. **Registro centralizado**: Erros são registrados em um arquivo central
4. **Notificação**: Erros críticos são notificados via WhatsApp
5. **Recuperação**: O sistema tenta continuar o processamento mesmo após falhas em documentos individuais

Exemplo de tratamento de erros:
```python
try:
    dados = swiss(texto)
    quiver(dados, documento, tipo_seguradora=TIPO_SEGURADORA['swiss'])
    listaFeitos.append(caminho)
    logger.info(f"Documento Swiss processado com sucesso: {dados[0]}")
except Exception as e:
    logger.error(f"Erro ao processar documento Swiss: {e}", exc_info=True)
```

## Guia de Execução

### Pré-requisitos

- Python 3.7 ou superior
- Chrome ou Chromium instalado
- Bibliotecas Python:
  - selenium
  - seleniumbase
  - PyPDF2
  - requests

### Instalação

1. Clone o repositório ou baixe os arquivos para sua máquina
2. Instale as dependências:
   ```
   pip install selenium seleniumbase PyPDF2 requests
   ```
3. Configure as credenciais em `src/config/settings.py`

### Execução Manual

1. Abra um terminal na pasta raiz do projeto
2. Execute o script Python principal:
   ```
   python main.py
   ```

### Execução Automática (Windows)

1. Execute o arquivo batch:
   ```
   executar_automacao.bat
   ```

### Execução Agendada

Para execução agendada, configure o Agendador de Tarefas (Windows) ou cron (Linux/Mac):

**Windows (Agendador de Tarefas)**:
1. Abra o Agendador de Tarefas
2. Crie uma nova tarefa
3. Configure o trigger (por exemplo, diariamente às 8:00)
4. Adicione uma ação para executar `executar_automacao.bat`

**Linux/Mac (cron)**:
1. Abra o crontab:
   ```
   crontab -e
   ```
2. Adicione uma linha:
   ```
   0 8 * * * cd /caminho/para/Bot-Faturas && python main.py
   ```

## Manutenção e Suporte

### Adição de Nova Seguradora

Para adicionar suporte a uma nova seguradora:

1. Crie um novo arquivo em `src/company/` (ex: `nova_seguradora.py`)
2. Implemente a função de extração seguindo o padrão existente
3. Adicione a seguradora no dicionário `TIPO_SEGURADORA` em `settings.py`
4. Importe e adicione a chamada da função no `main.py`

### Atualização de Layouts de Faturas

Se o layout de uma fatura for alterado:

1. Obtenha uma amostra do novo layout
2. Atualize as expressões regulares e lógica de extração no respectivo arquivo da seguradora
3. Teste com o novo layout antes de implantar em produção

### Verificação de Logs

Para verificar o funcionamento do sistema:

1. Consulte os logs diários em `src/logs/fatura_YYYY-MM-DD.log`
2. Verifique erros em `error_log.txt`
3. Consulte o registro de faturas processadas em `feitos.txt`

## Troubleshooting

### Problemas Comuns e Soluções

|           Problema           |           Possível Causa            |                            Solução                           |
|------------------------------|-------------------------------------|--------------------------------------------------------------|
| Erro de login no e-mail      | Credenciais incorretas ou alteradas | Verifique e atualize as credenciais em `settings.py`         |
| Erro ao extrair dados do PDF | Layout da fatura alterado           | Atualize o processador específico da seguradora              |
| Timeout na automação web     | Rede lenta ou sistema instável      | Aumente o valor de `MAX_TIMEOUT` em `web_automation.py`      |
| Falha ao enviar notificações | Problema com WhatsApp Web           | Verifique a conexão ou use método alternativo de notificação |
| Chrome não inicia            | Versão incompatível                 | Atualize o ChromeDriver ou o Chrome                          |

### Logs para Diagnóstico

Para diagnóstico avançado, aumente o nível de detalhe dos logs:

1. Modifique `logging_config.py`:
   ```python
   file_handler.setLevel(logging.DEBUG)
   console_handler.setLevel(logging.DEBUG)
   logger.setLevel(logging.DEBUG)
   ```

2. Execute o sistema e analise os logs detalhados

## Glossário

- **Apólice**: Documento que formaliza o contrato de seguro
- **Endosso**: Documento que registra alterações no contrato de seguro
- **Prêmio**: Valor pago pelo segurado à seguradora
- **Vigência**: Período de validade do seguro
- **RCF**: Responsabilidade Civil Facultativa
- **RCTR-C**: Responsabilidade Civil do Transportador Rodoviário - Carga
- **Corretor Online**: Sistema utilizado pela corretora para gerenciamento de seguros
- **Quiver**: Nome da função de automação que insere dados no sistema da corretora