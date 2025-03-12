# Gui de Instalação - Bot Faturas

## Requisitos do Sistema

- Python 3.9 ou superior.
- Google Chrome instalado.
- Acesso ao sistema Corretor-Online.
- Acesso ao webmail da empresa.

## Dependências

Instale as dependências necessárias com:

```bash
pip install -r requirements.txt
```

## Configuração inicial

1. Configuração de credenciais:

Edite o arquivo src/config/settings.py com as credenciais corretas
Não compartilhe este arquivo com as credenciais reais


2. Configuração do WebDriver:

O Chrome WebDriver será automaticamente gerenciado pelo SeleniumBase
Certifique-se que a versão do Chrome está atualizada


3. Configuração de diretórios:

O sistema criará automaticamente a pasta src/logs para armazenar registros
Verifique se o usuário tem permissão de escrita no diretório de execução