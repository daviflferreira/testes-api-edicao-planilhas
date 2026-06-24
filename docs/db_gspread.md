# Integração Python com Google Sheets — JSON (mock DB) + gspread

## Visão geral

Variante que simula o retorno de uma query em banco de dados usando um JSON mockado
como fonte de dados, em vez de um CSV. A escrita na planilha usa o `gspread` com
autenticação via Service Account.

O objetivo é mostrar como trocar a origem dos dados sem alterar a lógica de autenticação
ou de escrita — apenas o módulo de leitura muda.

Documentação oficial do gspread: https://docs.gspread.org/en/latest/

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
    ├── auth.py               # Autenticação com o service account
    ├── sheets.py             # Escrita na planilha via gspread
    ├── data_source.py        # Leitura do JSON e conversão para list[list[str]]
    └── main_db_gspread.py    # Ponto de entrada
```

## Bibliotecas utilizadas

| Biblioteca | Função |
|---|---|
| `gspread` | Interface de alto nível para o Google Sheets — abstrai os requests HTTP |
| `google-auth` | Gerencia a autenticação com as APIs do Google usando o service account |
| `python-dotenv` | Lê o arquivo `.env` e injeta as variáveis no ambiente |

Instalar:

```bash
pip install gspread google-auth python-dotenv
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

Isso garante que `clear_and_write` do `sheets.py` funcione sem nenhuma alteração.

### auth.py

Reutilizado sem alteração. Lê o `service_account.json`, declara os escopos de acesso
e retorna um cliente `gspread` pronto para uso.

### sheets.py

Reutilizado sem alteração. Recebe `list[list[str]]`, limpa a planilha e escreve os
dados a partir de A1.

### main_db_gspread.py

Ponto de entrada. Orquestra as chamadas na ordem correta:

1. Autentica com o service account
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
python main_db_gspread.py
```

## Quando usar essa abordagem

**Use quando:**
- Os dados vêm de uma query em banco ou de uma API que retorna JSON
- Quer manter a simplicidade do `gspread` para a escrita
- O script roda de forma automatizada (cron, pipeline)

**Evite quando:**
- Os dados já estão em CSV — as variantes 1 e 2 são mais diretas
- Precisa de controle total sobre os parâmetros da API do Google — use a variante 6