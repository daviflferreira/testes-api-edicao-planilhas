# Integração Python com Google Sheets — gspread + Service Account

## Visão geral

Integração entre Python e Google Sheets usando a biblioteca `gspread` com autenticação
via Service Account. Por não exigir login humano, funciona bem em automações e pipelines
que rodam sem interação do usuário.

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
├── .env                  # ID da planilha e caminho do service account
├── .gitignore            # Ignora credenciais e .env
├── service_account.json  # Credenciais do service account (não subir para o git)
├── data/
│   └── metrics.csv       # Dados mockados
└── src/
    ├── auth.py           # Autenticação com o service account
    ├── sheets.py         # Leitura do CSV e escrita na planilha
    └── main.py           # Ponto de entrada
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

## Como funciona o código

### auth.py

Responsável pela autenticação. Lê o `service_account.json`, declara os escopos
de acesso e retorna um cliente `gspread` pronto para uso.

Os escopos definem quais APIs o service account pode acessar:
- `spreadsheets` — leitura e escrita em planilhas compartilhadas
- `drive.file` — acesso a arquivos criados pelo próprio service account

### sheets.py

Contém duas funções:
- `load_csv` — lê o arquivo CSV e retorna uma lista de listas, que é o formato
  esperado pelo `gspread` para escrever na planilha
- `clear_and_write` — abre a planilha pelo ID, limpa o conteúdo atual e escreve
  os novos dados a partir da célula A1 em um único request

### main.py

Ponto de entrada. Lê as variáveis do `.env`, orquestra as chamadas na ordem correta
e confirma a execução:

1. Autentica com o service account
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
python main.py
```

## Quando usar essa abordagem

**Use `gspread` quando:**
- Quiser produtividade — menos código para operações comuns
- O projeto não exige controle fino sobre os requests HTTP
- Está prototipando ou construindo scripts internos

**Evite quando:**
- Precisar de operações avançadas que o `gspread` não abstrai
- Quiser depender apenas de bibliotecas oficiais do Google
- Precisar de controle total sobre os parâmetros da API