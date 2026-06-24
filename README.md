# Python + Google Sheets

Estudo de diferentes formas de integrar Python com Google Sheets, combinando duas bibliotecas, dois métodos de autenticação e duas fontes de dados. Objetivo é automatizar uma planilha que serve de fonte de dados pra um dashboard de metricas. Estudo foi realizado com auxílio de ferramenta de IA claude code como assistente/guia, corrigindo e apontando erros e explicando coisas que eu não entendia muito bem.

## Variantes implementadas

| Variante | Autenticação | Biblioteca | Fonte de dados | Arquivo |
|---|---|---|---|---|
| 1 | Service Account | gspread | CSV | `src/main.py` |
| 2 | Service Account | API direta | CSV | `src/main_api.py` |
| 3 | OAuth | gspread | CSV | `src/main_oauth.py` |
| 4 | OAuth | API direta | CSV | `src/main_api_oauth.py` |
| 5 | Service Account | gspread | JSON (mock DB) | `src/main_db_gspread.py` |
| 6 | Service Account | API direta | JSON (mock DB) | `src/main_db_api.py` |

Para entender as diferenças entre cada abordagem, veja o [COMPARATIVO.md](COMPARATIVO.md).

## Como rodar

```bash
# instalar dependências
pip install -r requirements.txt

# executar a variante desejada
cd src
python main.py
```

## Requisitos

- Python 3.10+
- Credenciais do Google Cloud (Service Account ou OAuth — ver documentação em `docs/`)