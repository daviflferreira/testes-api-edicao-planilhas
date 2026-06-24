# Integração Python com Google Sheets — JSON (mock DB) + Sheets API v4

## Visão geral

Variante que simula o retorno de uma query em banco de dados usando um JSON mockado
como fonte de dados, com a escrita na planilha feita via Sheets API v4 diretamente,
sem abstrações de terceiros. Autenticação via Service Account.

Documentação oficial da Sheets API: https://developers.google.com/sheets/api/reference/rest

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
├── .env                      # ID da planilha e caminho do service account
├── .gitignore                # Ignora credenciais e .env
├── service_account.json      # Credenciais do service account (não subir para o git)
├── data/
│   └── metrics.json          # Dados mockados no formato de retorno de banco
└── src/
    ├── auth_api.py           # Autenticação e criação do serviço da Sheets API
    ├── sheets_api.py         # Escrita na planilha via API direta
    ├── data_source.py        # Leitura do JSON e conversão para list[list[str]]
    └── main_db_api.py        # Ponto de entrada
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

## Formato do JSON mockado

O arquivo `data/metrics.json` simula o retorno de uma query em banco, no formato:

```json
{
  "rows": [
    {"date": "2026-06-01", "pageviews": 4320, "sessions": 2100, "bounce_rate": 0.52}
  ],
  "rowcount": 1
}
```

O campo `rows` é um array de objetos, onde cada objeto representa uma linha e as chaves
representam as colunas. O campo `rowcount` é informativo e não é utilizado na escrita.

## Como funciona o código

### data_source.py

Módulo compartilhado entre as variantes com fonte JSON. Contém a função `load_json`:

1. Abre e parseia o arquivo JSON
2. Extrai as chaves do primeiro objeto como cabeçalhos da planilha
3. Converte cada objeto em uma lista de strings, na mesma ordem dos cabeçalhos
4. Retorna `list[list[str]]` — o mesmo formato que `load_csv` já entregava

Isso garante que `clear_and_write` do `sheets_api.py` funcione sem nenhuma alteração.

### auth_api.py

Reutilizado sem alteração. Lê o `service_account.json`, declara o scope `spreadsheets`
e usa `build("sheets", "v4", credentials=creds)` para retornar o objeto da Sheets API v4.

### sheets_api.py

Reutilizado sem alteração. Recebe `list[list[str]]` e faz duas chamadas explícitas à API:
- `.clear()` — limpa o intervalo `A1:Z1000`
- `.update()` — escreve os dados a partir de A1 com `valueInputOption="RAW"`

Cada chamada termina com `.execute()`, que é quando o request HTTP é de fato enviado.

### main_db_api.py

Ponto de entrada. Orquestra as chamadas na ordem correta:

1. Cria o serviço da Sheets API
2. Lê o JSON e converte para `list[list[str]]`
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
python main_db_api.py
```

## Quando usar essa abordagem

**Use quando:**
- Os dados vêm de uma query em banco ou de uma API que retorna JSON
- Quer depender apenas de bibliotecas oficiais do Google
- Precisa de controle total sobre os parâmetros dos requests
- O script roda de forma automatizada (cron, pipeline)

**Evite quando:**
- Os dados já estão em CSV — as variantes 1 e 2 são mais diretas
- Quer simplicidade na escrita — use a variante 5 com `gspread`