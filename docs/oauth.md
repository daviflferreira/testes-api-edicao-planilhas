# Integração Python + Google Sheets com OAuth

## Visão geral

Integração entre Python e Google Sheets usando autenticação OAuth 2.0 com login
do usuário no navegador. Ao contrário do Service Account, o acesso é feito em nome
de uma conta Google real.

Docs oficiais: https://developers.google.com/identity/protocols/oauth2

## Pré-requisitos

- Python 3.10+
- Conta Google com acesso ao [Google Cloud Console](https://console.cloud.google.com)
- Uma planilha no Google Sheets

## Configuração do Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com) e selecione seu projeto
2. Ative a **Google Sheets API** em APIs e serviços
3. Em **APIs e serviços > Credenciais**, clique em **"+ Criar credenciais"** → **"ID do cliente OAuth"**
4. Configure a tela de consentimento se solicitado:
   - Tipo: **Externo**
   - Preencha o nome do app e e-mail de contato
5. Em **"Tipo de aplicativo"** selecione **"App para computador"**
6. Baixe o JSON gerado e renomeie para `credentials.json` na raiz do projeto
7. Em **"Tela de consentimento OAuth"** → **"Usuários de teste"**, adicione os e-mails
   que poderão autorizar o app enquanto ele não for verificado pelo Google

## Estrutura do projeto

```text
projeto/
├── .env                  # ID da planilha
├── .gitignore            # Ignora credenciais, token e .env
├── credentials.json      # Credenciais OAuth (não subir para o git)
├── token.json            # Token gerado após o primeiro login (não subir para o git)
├── data/
│   └── metrics.csv       # Dados mockados
└── src/
    ├── auth_oauth.py          # OAuth + gspread
    ├── auth_api_oauth.py      # OAuth + API direta
    ├── sheets.py              # Escrita via gspread
    ├── sheets_api.py          # Escrita via API direta
    ├── main_oauth.py          # Ponto de entrada — gspread
    └── main_api_oauth.py      # Ponto de entrada — API direta
```

## Bibliotecas utilizadas

| Biblioteca | Função |
|---|---|
| `gspread` | Interface de alto nível para o Google Sheets (variante gspread) |
| `google-api-python-client` | SDK oficial do Google (variante API direta) |
| `google-auth` | Gerencia as credenciais e renovação automática do token |
| `google-auth-oauthlib` | Implementa o fluxo OAuth — abre o navegador e captura a autorização |
| `python-dotenv` | Lê o arquivo `.env` e injeta as variáveis no ambiente |

Instalar:

```bash
pip install gspread google-auth google-auth-oauthlib google-api-python-client python-dotenv
```

## Como funciona o fluxo OAuth

```text
1ª execução:
  Python → abre o navegador → usuário faz login no Google
  → Google devolve um token → salvo em token.json

2ª execução em diante:
  Python → lê o token.json → usa direto (sem abrir navegador)
  → se expirado, renova automaticamente com o refresh_token
```

## Como funciona o código

### auth_oauth.py / auth_api_oauth.py

A lógica de autenticação é idêntica nos dois arquivos — a única diferença é o que
retornam ao final:

- `auth_oauth.py` → retorna `gspread.authorize(creds)`
- `auth_api_oauth.py` → retorna `build("sheets", "v4", credentials=creds)`

O fluxo interno segue três etapas:

1. **Token existente e válido** → usa direto, sem abrir navegador
2. **Token expirado com refresh_token** → renova silenciosamente via `creds.refresh()`
3. **Sem token** → abre o navegador com `flow.run_local_server()`, usuário autoriza,
   token é salvo em `token.json`

### sheets.py / sheets_api.py

Reutilizados sem alteração das versões com Service Account — a lógica de leitura
e escrita na planilha não muda, apenas a origem das credenciais.

### main_oauth.py / main_api_oauth.py

Ponto de entrada. Lê as variáveis do `.env` e orquestra na ordem:

1. Autentica com OAuth (abre navegador se necessário)
2. Lê o CSV
3. Limpa e escreve na planilha

## Como executar

1. Configure o `.env` com o ID da sua planilha:

```text
SPREADSHEET_ID=seu_id_aqui
```

2. Execute a variante desejada:

```bash
cd src

# com gspread
python main_oauth.py

# com API direta
python main_api_oauth.py
```

Na primeira execução o navegador vai abrir pedindo autorização. Se o app ainda não
foi verificado pelo Google, clique em **"Avançado"** → **"Acessar (não seguro)"**.

## Quando usar essa abordagem

**Use OAuth quando:**
- A planilha precisa ser acessada em nome de um usuário específico
- O projeto terá uma interface onde o usuário clica em "Conectar com Google"
- Não é possível ou desejável criar um Service Account

**Evite quando:**
- O script roda de forma automatizada sem interação humana
- É um processo agendado (cron job, pipeline)
- Nesses casos, prefira Service Account