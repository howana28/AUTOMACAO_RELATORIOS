🇬🇧 [Read in English](README.md)

# Automação de Relatórios Comerciais

Pipeline automatizado para análise, visualização, geração e distribuição de relatórios de vendas.

> Acesso ao projeto: https://automacaorelatorios-abxbbwx42y85fms7s5ah5c.streamlit.app/

Este projeto transforma uma planilha de vendas em um fluxo automatizado de análise comercial. A aplicação valida os dados, calcula indicadores, permite filtros interativos, exibe gráficos em um dashboard, gera um relatório em PDF e pode enviá-lo por e-mail.

Projeto desenvolvido para demonstrar automação de processos, análise de dados, organização de código Python, testes automatizados, integração contínua e construção de uma interface simples para usuários não técnicos.

## Visão geral

Relatórios comerciais produzidos manualmente costumam exigir várias etapas repetitivas: abrir planilhas, conferir dados, calcular indicadores, montar gráficos, exportar arquivos e distribuí-los para as pessoas responsáveis.

Além do tempo gasto, esse processo pode gerar inconsistências, retrabalho e dificuldade para reproduzir a mesma análise em novos períodos.

A proposta deste projeto é centralizar esse fluxo em uma aplicação reutilizável, modular e automatizável.

## Arquitetura da solução

O projeto também pode ser executado por linha de comando, permitindo sua integração futura com agendadores, pipelines ou outros serviços.

## Funcionalidades

- Upload de planilha Excel pela interface.
- Base fictícia de demonstração incluída no projeto.
- Validação automática da estrutura da planilha.
- Tratamento e preparação dos dados.
- Filtros por período e categoria.
- Cálculo de faturamento total.
- Total de pedidos.
- Ticket médio.
- Total de itens vendidos.
- Produto mais vendido.
- Produto com maior faturamento.
- Lucro e margem estimados quando há custo unitário.
- Evolução diária do faturamento.
- Ranking de produtos.
- Participação do faturamento por categoria.
- Dashboard interativo com Streamlit.
- Geração de relatório em PDF.
- Download do relatório pela interface.
- Envio opcional do PDF por e-mail.
- Configuração de credenciais por variáveis de ambiente.
- Registro de execução em arquivo de log.
- Testes automatizados das principais regras de negócio.
- Integração contínua com GitHub Actions.
- Execução por interface ou linha de comando.
- Suporte a execução em container Docker.

## Indicadores disponíveis

| Indicador | Descrição |
| --- | --- |
| Faturamento | Soma da receita dos itens vendidos |
| Pedidos | Quantidade de pedidos únicos |
| Ticket médio | Faturamento dividido pelo número de pedidos |
| Itens vendidos | Soma das quantidades vendidas |
| Produto mais vendido | Produto com maior quantidade vendida |
| Maior faturamento | Produto que mais gerou receita |
| Lucro estimado | Receita menos custo, quando o custo é informado |
| Margem estimada | Percentual de lucro sobre o faturamento |

## Tecnologias utilizadas

- Python
- pandas para tratamento e análise dos dados
- Streamlit para a interface web
- Plotly para gráficos interativos
- Matplotlib para visualizações utilizadas no relatório
- ReportLab para geração de PDF
- openpyxl para leitura de arquivos Excel
- python-dotenv para variáveis de ambiente
- SMTP para envio de e-mails
- pytest para testes automatizados
- GitHub Actions para integração contínua
- Docker para containerização

## Estrutura do projeto

```text
AUTOMACAO_RELATORIOS/
│
├── app.py                       # Interface Streamlit
├── main.py                      # Execução por linha de comando
├── requirements.txt            # Dependências do projeto
├── Dockerfile                  # Configuração do container
├── .dockerignore
├── pytest.ini
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore
├── LICENSE
│
├── .github/
│   └── workflows/
│       └── testes.yml          # Testes automáticos no GitHub Actions
│
├── docs/
│   └── relatorio_exemplo.pdf   # Exemplo de relatório gerado
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Configurações e variáveis de ambiente
│   ├── carregador_dados.py     # Leitura da planilha
│   ├── validador.py            # Validação e preparação dos dados
│   ├── analises.py             # KPIs e agregações
│   ├── relatorio_pdf.py        # Geração do PDF
│   ├── email_service.py        # Envio de e-mail
│   └── logger_config.py        # Configuração de logs
│
├── dados/
│   └── vendas_exemplo.xlsx     # Base fictícia para demonstração
│
├── saida/
│   └── .gitkeep                # Relatórios gerados localmente
│
├── logs/
│   └── .gitkeep                # Logs locais
│
└── tests/
    ├── test_analises.py
    └── test_validador.py
```

## Exemplo de saída

O diretório `docs/` contém um relatório de demonstração gerado pela própria aplicação a partir da base fictícia incluída no projeto.

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

A coluna `Custo_Unitario` é opcional. Quando presente, a aplicação também calcula lucro e margem estimados.

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/howana28/AUTOMACAO_RELATORIOS.git
cd AUTOMACAO_RELATORIOS
```

### 2. Criar um ambiente virtual

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

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar a interface

```bash
streamlit run app.py
```

Após a inicialização, o Streamlit disponibiliza a aplicação localmente no navegador.

## Execução pela linha de comando

Também é possível gerar um relatório sem abrir a interface:

```bash
python main.py --arquivo dados/vendas_exemplo.xlsx
```

Para gerar o relatório e enviá-lo por e-mail:

```bash
python main.py --arquivo dados/vendas_exemplo.xlsx --email destinatario@empresa.com
```

Esse modo permite integrar a aplicação futuramente com agendadores de tarefas, pipelines de automação ou outros serviços.

## Configuração do envio por e-mail

As credenciais não ficam gravadas diretamente no código.

Primeiro, crie um arquivo `.env` a partir do exemplo existente.

Windows:

```bash
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Depois, configure as variáveis localmente:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_REMETENTE=usuario@exemplo.com
EMAIL_SENHA=senha_de_aplicativo
```

O arquivo `.env` está listado no `.gitignore` e não deve ser enviado ao repositório.

Para provedores que utilizam autenticação em duas etapas, pode ser necessário utilizar uma senha de aplicativo específica para SMTP.

## Execução com Docker

Criar a imagem:

```bash
docker build -t automacao-relatorios-comerciais .
```

Executar a aplicação:

```bash
docker run --rm -p 8501:8501 automacao-relatorios-comerciais
```

Depois da inicialização, a aplicação fica disponível em:

```text
http://localhost:8501
```

Para utilizar o envio por e-mail em ambiente containerizado, as variáveis de ambiente devem ser fornecidas de forma segura durante a execução.

## Testes automatizados

Os testes cobrem regras centrais de validação e análise.

Para executar:

```bash
pytest
```

Atualmente são verificados cenários relacionados a:

- validação de colunas obrigatórias;
- preparação dos dados;
- cálculo de faturamento;
- cálculo de KPIs;
- ranking de produtos.

## Integração contínua

O repositório possui um workflow em `.github/workflows/testes.yml`.

A cada push ou pull request, o GitHub Actions prepara o ambiente e executa automaticamente os testes do projeto.

Isso ajuda a identificar regressões antes que novas alterações sejam incorporadas ao código principal.

## Fluxo de uso

1. A planilha é enviada pela interface ou carregada pelo modo de linha de comando.
2. A aplicação valida as colunas e os valores obrigatórios.
3. Os dados são preparados e novas métricas são calculadas.
4. O dashboard apresenta KPIs e visualizações.
5. O período e a categoria podem ser filtrados.
6. O relatório em PDF é gerado com os dados selecionados.
7. O arquivo pode ser baixado ou enviado por e-mail.
8. As execuções do modo de linha de comando podem ser registradas em log.

## Decisões de arquitetura

O projeto separa responsabilidades para evitar concentrar toda a lógica em um único arquivo.

- `carregador_dados.py` concentra a entrada dos dados.
- `validador.py` reúne as regras de validação e qualidade.
- `analises.py` contém as regras analíticas e os indicadores.
- `relatorio_pdf.py` concentra a geração do documento.
- `email_service.py` isola a integração de e-mail.
- `config.py` centraliza configurações externas.
- `logger_config.py` centraliza o registro de logs.
- `app.py` funciona como camada de interface.
- `main.py` oferece uma alternativa automatizável por linha de comando.

Essa divisão facilita manutenção, testes e futuras integrações.

## Segurança

Credenciais e configurações sensíveis não devem ser escritas diretamente no código-fonte.

A aplicação utiliza variáveis de ambiente e mantém o arquivo `.env` fora do versionamento por meio do `.gitignore`.

Em um ambiente de produção, segredos devem ser armazenados em mecanismos próprios de gerenciamento de credenciais oferecidos pela infraestrutura utilizada.

## Dados de demonstração

O arquivo `dados/vendas_exemplo.xlsx` contém apenas dados fictícios criados para demonstração.

Isso permite executar e avaliar o projeto sem publicar informações comerciais reais.

## Possíveis evoluções

- Comparação automática com períodos anteriores.
- Metas comerciais e análise de atingimento.
- Exportação adicional para Excel e CSV.
- Persistência em banco de dados.
- Histórico de relatórios gerados.
- Agendamento automático de relatórios.
- Integração com APIs de ERP ou marketplaces.
- Autenticação de usuários.
- Controle de acesso por perfil.
- Deploy em ambiente cloud.
- Envio de relatórios por outros canais.
- Testes de integração e maior cobertura automatizada.

## Objetivo do projeto

Este projeto foi construído como uma aplicação de portfólio com foco em demonstrar competências em:

- automação de processos;
- análise e tratamento de dados;
- criação de indicadores de negócio;
- desenvolvimento de interfaces com Python;
- geração automatizada de documentos;
- integração com serviços externos;
- organização modular de código;
- testes automatizados;
- integração contínua;
- boas práticas de configuração e segurança;
- containerização.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE).
