# Integração Python com Google Sheets — Sheets API v4 + Service Account

## Visão geral

Integração com Python usando a Sheets API v4 diretamente, sem abstrações de terceiros,
com autenticação via Service Account. Oferece controle total sobre os parâmetros e
endpoints da API.

Documentação oficial: https://developers.google.com/sheets/api/reference/rest

## Requisitos

- Python 3.10+
- Conta do Google com acesso ao Google Cloud Console
- Uma planilha no Google Sheets

## Configuração do Google Cloud

1. Acesse o Google Cloud Console (https://console.cloud.google.com) e selecione o projeto
2. Ative a **Google Sheets API** em APIs e serviços
3. Em **IAM e administrador > Contas de serviço**, crie uma conta com qualquer nome
4. Na conta criada, vá em **Chaves > Adicionar chave > JSON** e baixe o arquivo
5. Renomeie o arquivo para `service_account.json` e coloque na raiz do projeto
6. Abra sua planilha no Google Sheets, clique em **Compartilhar** e adicione o e-mail
   do Service Account como Editor

## Estrutura do projeto

```text
projeto/
├── .env                  # ID da planilha e caminho do service account
├── .gitignore            # Ignora credenciais e .env
├── service_account.json  # Credenciais do service account (não subir para o git)
├── data/
│   └── metrics.csv       # Dados mockados
└── src/
    ├── auth_api.py       # Autenticação e criação do serviço da Sheets API
    ├── sheets_api.py     # Leitura do CSV e escrita na planilha
    └── main_api.py       # Ponto de entrada
```

## Bibliotecas utilizadas

| Biblioteca | Função |
|---|---|
| `google-api-python-client` | SDK oficial do Google — constrói o cliente para qualquer API Google via `build()` |
| `google-auth` | Gerencia a autenticação com as APIs do Google usando o service account |
| `python-dotenv` | Lê o arquivo `.env` e injeta as variáveis no ambiente |

Instalar:

```bash
pip install google-api-python-client google-auth python-dotenv
```

## Como funciona o código

### auth_api.py

Responsável pela autenticação. Lê o `service_account.json`, declara o scope
`spreadsheets` e usa `build("sheets", "v4", credentials=creds)` para retornar
um objeto que representa a Sheets API v4 com todos os endpoints disponíveis.

### sheets_api.py

Contém duas funções:
- `load_csv` — lê o arquivo CSV e retorna uma lista de listas
- `clear_and_write` — acessa o recurso `spreadsheets().values()` e faz duas
  chamadas explícitas à API:
  - `.clear()` — limpa o intervalo `A1:Z1000`
  - `.update()` — escreve os dados a partir de A1 com `valueInputOption="RAW"`

Cada chamada termina com `.execute()`, que é quando o request HTTP é de fato enviado.

### main_api.py

Ponto de entrada. Lê as variáveis do `.env` e orquestra as chamadas na ordem correta:

1. Cria o serviço da Sheets API
2. Lê o CSV
3. Limpa e escreve na planilha

## Como executar

1. Configure o `.env` com o ID da sua planilha:

```text
SPREADSHEET_ID=seu_id_aqui
SERVICE_ACCOUNT_PATH=service_account.json
```

2. Execute:

```bash
cd src
python main_api.py
```

## Quando usar essa abordagem

**Use a API direta quando:**
- Precisar de operações avançadas não cobertas pelo `gspread`
- Quiser depender apenas de bibliotecas oficiais do Google
- Precisar de controle total sobre os parâmetros dos requests
- O projeto já usa `google-api-python-client` para outras APIs Google

**Evite quando:**
- Quiser produtividade em operações simples de leitura e escrita
- Está prototipando ou construindo scripts internos rápidos