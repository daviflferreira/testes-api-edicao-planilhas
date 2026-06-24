# Comparativo de abordagens — Python + Google Sheets

Esse projeto implementa seis formas de integrar Python com Google Sheets,
combinando duas bibliotecas, dois métodos de autenticação e duas fontes de dados.

---

## Visão geral

| Variante | Autenticação | Biblioteca | Fonte de dados | Ponto de entrada |
|---|---|---|---|---|
| 1 | Service Account | gspread | CSV | `src/main.py` |
| 2 | Service Account | API direta | CSV | `src/main_api.py` |
| 3 | OAuth (usuário) | gspread | CSV | `src/main_oauth.py` |
| 4 | OAuth (usuário) | API direta | CSV | `src/main_api_oauth.py` |
| 5 | Service Account | gspread | JSON (mock DB) | `src/main_db_gspread.py` |
| 6 | Service Account | API direta | JSON (mock DB) | `src/main_db_api.py` |

---

## Autenticação: Service Account vs OAuth

| | Service Account | OAuth |
|---|---|---|
| **Quem autentica** | Um robô com identidade própria | Um usuário real |
| **Login humano** | Nunca | Sim, na 1ª execução |
| **Token salvo** | Não precisa | `token.json` |
| **Ideal para** | Automações, pipelines, cron jobs | Apps com login do usuário |
| **Acessa planilhas** | Só as compartilhadas com o service account | Qualquer planilha do usuário autenticado |
| **Credencial** | `service_account.json` | `credentials.json` + `token.json` |

---

## Biblioteca: gspread vs API direta

| | gspread | API direta |
|---|---|---|
| **Nível** | Alto nível (abstração) | Baixo nível (requests explícitos) |
| **Escrita** | `sheet.update(data, "A1")` | `spreadsheets().values().update(...).execute()` |
| **Verbosidade** | Menor | Maior |
| **Controle** | Limitado à API do gspread | Total sobre parâmetros e endpoints |
| **Dependência** | Biblioteca de terceiro | SDK oficial do Google |
| **Documentação** | [docs.gspread.org](https://docs.gspread.org) | [developers.google.com/sheets/api](https://developers.google.com/sheets/api) |

---

## Fonte de dados: CSV vs JSON mockado

| | CSV | JSON (mock DB) |
|---|---|---|
| **Arquivo** | `data/metrics.csv` | `data/metrics.json` |
| **Módulo de leitura** | `load_csv` em `sheets.py` / `sheets_api.py` | `load_json` em `data_source.py` |
| **Cabeçalhos** | Primeira linha do arquivo | Extraídos automaticamente das chaves do primeiro objeto |
| **Simula** | Arquivo exportado | Retorno de uma query em banco de dados |
| **Formato de saída** | `list[list[str]]` | `list[list[str]]` (mesmo formato) |

O módulo `data_source.py` é compartilhado entre as variantes 5 e 6 — a função `load_json`
extrai as chaves do primeiro dict como cabeçalho e converte cada linha para `list[str]`,
produzindo o mesmo formato que `load_csv` já entregava. Por isso `clear_and_write` não precisou mudar.

---

## Qual variante usar?

```
De onde vêm os dados?
├── CSV → Variantes 1–4
│
└── JSON / retorno de banco → Variantes 5–6
    ├── Quer menos código? → Variante 5 (gspread)
    └── Quer só libs oficiais? → Variante 6 (API direta)

Para variantes CSV:
Vai rodar automaticamente (cron, pipeline)?
├── Sim → Service Account
│   ├── Quer menos código e simplicidade? → Variante 1 (gspread)
│   └── Quer controle total ou só libs oficiais? → Variante 2 (API direta)
│
└── Não → usuário vai autorizar via login?
    ├── Sim → OAuth
    │   ├── Quer menos código e simplicidade? → Variante 3 (gspread + OAuth)
    │   └── Quer controle total ou só libs oficiais? → Variante 4 (API direta + OAuth)
```

---

## Documentação por variante

- [gspread + Service Account](docs/gspread.md)
- [API direta + Service Account](docs/google_sheets_api.md)
- [OAuth (gspread e API direta)](docs/oauth.md)
- [JSON mock DB + gspread](docs/db_gspread.md)
- [JSON mock DB + API direta](docs/db_api.md)