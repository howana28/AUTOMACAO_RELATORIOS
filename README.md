# Automação de Relatórios Comerciais

**Pipeline automatizado de análise, visualização, geração e distribuição de relatórios de vendas.**

Este projeto transforma uma planilha de vendas em um fluxo automatizado de análise comercial. A aplicação valida os dados, calcula indicadores, permite filtros interativos, exibe gráficos em um dashboard, gera um relatório em PDF e pode enviá-lo por e-mail.

> Projeto desenvolvido para demonstrar automação de processos, análise de dados, organização de código Python e construção de uma interface simples para usuários não técnicos.

## Problema

Relatórios comerciais feitos manualmente costumam exigir várias etapas repetitivas: abrir planilhas, conferir dados, calcular indicadores, montar gráficos, exportar arquivos e enviá-los às pessoas responsáveis.

Além do tempo gasto, esse processo pode gerar inconsistências e retrabalho.

## Solução

A aplicação centraliza esse fluxo em um único pipeline:

```text
Planilha Excel
     │
     ▼
Validação dos dados
     │
     ▼
Tratamento e cálculo de métricas
     │
     ├───────────────┐
     ▼               ▼
Dashboard         Relatório PDF
     │               │
     └───────┬───────┘
             ▼
       Envio por e-mail
             │
             ▼
        Logs de execução
```

## Funcionalidades

- Upload de planilha Excel pela interface.
- Base de demonstração incluída no projeto.
- Validação automática de estrutura e conteúdo da planilha.
- Filtros por período e categoria.
- Cálculo de faturamento total.
- Total de pedidos.
- Ticket médio.
- Total de itens vendidos.
- Produto mais vendido.
- Produto com maior faturamento.
- Lucro e margem estimados quando a planilha possui custo unitário.
- Evolução diária do faturamento.
- Ranking de produtos.
- Participação de faturamento por categoria.
- Geração de relatório em PDF.
- Download do relatório pela interface.
- Envio opcional do PDF por e-mail.
- Configuração segura de credenciais por variáveis de ambiente.
- Registro de execução em arquivo de log.
- Testes automatizados das principais regras de negócio.
- Integração contínua com GitHub Actions para executar os testes a cada push e pull request.
- Execução tanto por interface Streamlit quanto por linha de comando.

## Indicadores disponíveis

| Indicador | Descrição |
| --- | --- |
| Faturamento | Soma da receita dos itens vendidos |
| Pedidos | Quantidade de pedidos únicos |
| Ticket médio | Faturamento dividido pelo número de pedidos |
| Itens vendidos | Soma de todas as quantidades |
| Produto mais vendido | Produto com maior quantidade vendida |
| Maior faturamento | Produto que mais gerou receita |
| Lucro estimado | Receita menos custo, quando informado |
| Margem estimada | Percentual de lucro sobre o faturamento |

## Tecnologias

- Python
- pandas
- Streamlit
- Plotly
- Matplotlib
- ReportLab
- openpyxl
- python-dotenv
- SMTP
- pytest
- Docker
- GitHub Actions

## Estrutura do projeto

```text
automacao_relatorios_comerciais/
│
├── app.py                       # Interface Streamlit
├── main.py                      # Execução via terminal
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── pytest.ini
├── .env.example
├── .gitignore
├── LICENSE
│
├── .github/
│   └── workflows/
│       └── testes.yml            # CI com GitHub Actions
│
├── docs/
│   └── relatorio_exemplo.pdf     # Exemplo de saída gerada
│
├── src/
│   ├── __init__.py
│   ├── config.py                # Configurações e variáveis de ambiente
│   ├── carregador_dados.py      # Leitura da planilha
│   ├── validador.py             # Validação e preparação dos dados
│   ├── analises.py              # KPIs e agregações
│   ├── relatorio_pdf.py         # Geração do PDF
│   ├── email_service.py         # Envio de e-mail
│   └── logger_config.py         # Configuração de logs
│
├── dados/
│   └── vendas_exemplo.xlsx      # Base fictícia para demonstração
│
├── saida/
│   └── .gitkeep                 # PDFs gerados ficam aqui
│
├── logs/
│   └── .gitkeep                 # Logs locais ficam aqui
│
└── tests/
    ├── test_analises.py
    └── test_validador.py
```

## Exemplo de saída

O diretório `docs/` contém um PDF de demonstração gerado pela própria aplicação a partir da base fictícia incluída no projeto.

## Formato esperado da planilha

A planilha deve possuir as seguintes colunas:

| Coluna | Obrigatória | Exemplo |
| --- | --- | --- |
| Data | Sim | 2026-04-01 |
| Pedido | Sim | PED-0001 |
| Produto | Sim | Hidratante Corporal 250ml |
| Categoria | Sim | Cuidados Pessoais |
| Quantidade | Sim | 2 |
| Preco_Unitario | Sim | 39.90 |
| Custo_Unitario | Não | 18.50 |

A coluna `Custo_Unitario` é opcional. Quando ela está presente, a aplicação também calcula lucro e margem estimados.

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Crie um ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a interface

```bash
streamlit run app.py
```

O navegador abrirá a aplicação localmente.


## Executando com Docker

Crie a imagem:

```bash
docker build -t automacao-relatorios-comerciais .
```

Execute a aplicação:

```bash
docker run --rm -p 8501:8501 automacao-relatorios-comerciais
```

Depois acesse `http://localhost:8501`.

Para habilitar envio por e-mail, passe as variáveis de ambiente de forma segura ou utilize um arquivo `.env` local que não seja versionado.

## Execução pelo terminal

Também é possível gerar um relatório sem abrir a interface:

```bash
python main.py --arquivo dados/vendas_exemplo.xlsx
```

Para gerar e enviar por e-mail:

```bash
python main.py --arquivo dados/vendas_exemplo.xlsx --email destinatario@empresa.com
```

## Configuração do envio por e-mail

Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

No Linux/macOS:

```bash
cp .env.example .env
```

Preencha o `.env` localmente:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_REMETENTE=seuemail@gmail.com
EMAIL_SENHA=sua_senha_de_app
```

O arquivo `.env` está no `.gitignore` e **não deve ser enviado ao GitHub**.

Para contas Google com autenticação em duas etapas, utilize uma senha de app no lugar da senha principal da conta.

## Segurança

Credenciais nunca devem ser escritas diretamente no código-fonte. Este projeto usa variáveis de ambiente para separar configurações sensíveis da aplicação.

Se uma credencial tiver sido publicada anteriormente em um repositório, apenas removê-la do arquivo não é suficiente. A credencial deve ser revogada e o histórico do Git deve ser tratado antes de considerar o vazamento resolvido.

## Testes

Execute:

```bash
pytest
```

Os testes atuais verificam regras centrais de validação, cálculo de faturamento, KPIs e ranking de produtos.

## Fluxo de uso

1. O usuário envia uma planilha ou utiliza os dados fictícios incluídos.
2. A aplicação valida as colunas e os valores obrigatórios.
3. Os dados são preparados e novas métricas são calculadas.
4. O dashboard apresenta KPIs e visualizações.
5. O usuário pode filtrar período e categoria.
6. O PDF é gerado com os dados filtrados.
7. O relatório pode ser baixado ou enviado por e-mail.
8. Execuções realizadas pelo modo de linha de comando são registradas em log.

## Decisões de arquitetura

O projeto separa responsabilidades para evitar concentrar toda a lógica em um único arquivo:

- `carregador_dados.py` é responsável pela entrada.
- `validador.py` concentra as regras de qualidade de dados.
- `analises.py` contém as regras analíticas.
- `relatorio_pdf.py` cuida exclusivamente da apresentação do relatório.
- `email_service.py` isola a integração SMTP.
- `config.py` centraliza configurações externas.
- `app.py` funciona como camada de interface.
- `main.py` oferece uma alternativa automatizável por linha de comando.

Essa divisão facilita testes, manutenção e futuras integrações.

## Possíveis evoluções

- Comparação automática com período anterior.
- Metas comerciais e análise de atingimento.
- Exportação para Excel e CSV.
- Banco de dados para histórico de execuções.
- Agendamento automático de relatórios.
- Integração com APIs de ERP ou marketplace.
- Autenticação de usuários.
- Deploy da aplicação em ambiente cloud.

## Sobre os dados de demonstração

A planilha incluída em `dados/vendas_exemplo.xlsx` contém dados fictícios gerados apenas para demonstração. Ela permite testar o projeto imediatamente sem expor informações comerciais reais.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE`.
