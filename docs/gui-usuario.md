# Guia do Usuário - Bot Faturas

## Iniciando o Bot

Para iniciar o processamento de faturas, execute o script principal:

```bash
python cadastro_fatura2.py
```

## Fluxo de Trabalho

1. Download de Emails:

O bot acessará automaticamente o email configurado
Baixará todos os anexos de emails não lidos
Arquivará os emails processados


2. Processamento de Faturas:

Cada anexo será analisado para identificar a seguradora
Os dados relevantes serão extraídos conforme a formatação específica
Faturas já processadas anteriormente serão ignoradas


3. Cadastro no Sistema:

Os dados extraídos serão inseridos automaticamente no Corretor Online
Os documentos originais serão anexados
O processo completo será registrado nos logs

## Monitoramento e Logs

- Os logs são armazenados em src/logs/fatura_[DATA].log
- O arquivo feitos.txt mantém o registro de faturas já processadas
- Consulte os logs para verificar o status de processamento

## Manutenção

- Execute o bot periodicamente para processar novos emails
- Verifique regularmente o arquivo de log para identificar possíveis erros
- O bot limpará automaticamente os arquivos temporários após o processamento

## Recuperação de Erros
Se o processamento falhar:

1. Verifique os logs para identificar o erro
2. Corrija o problema (credenciais, conexão, etc.)
3. Execute novamente o script - faturas já processadas não serão duplicadas