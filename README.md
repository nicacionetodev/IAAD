# Sistema de Gerenciamento da Copa do Mundo — CRUD Streamlit + MySQL

Este projeto é um sistema computacional web completo para gerenciamento de dados de seleções, estádios, jogadores, partidas e cartões da Copa do Mundo 2026. Ele conta com uma interface gráfica desenvolvida com Streamlit e conexão nativa ao banco de dados MySQL.

## Estrutura do Projeto

* **app.py**: Ponto de entrada do aplicativo, contendo a página inicial e estatísticas gerais.
* **db_connection.py**: Módulo responsável pela conexão dinâmica com o MySQL e execução de scripts SQL.
* **style.css**: Arquivo contendo estilos CSS customizados .
* **requirements.txt**: Arquivo que especifica as dependências Python necessárias.
* **Copa_do_Mundo.sql**: Script SQL com a estrutura básica de tabelas do banco de dados.
* **setup_database.sql**: Script SQL com modificações de colunas, trigger de verificação de expulsão e dados de exemplo ampliados (16 seleções, 80 jogadores, 16 partidas e 28 cartões).
* **pages/**: Diretório que contém as telas de gerenciamento (CRUD) de cada entidade e o dashboard gráfico.
  * **01_Estadios.py**: Gerenciamento de Estádios.
  * **02_Selecoes.py**: Gerenciamento de Seleções .
  * **03_Jogadores.py**: Gerenciamento de Jogadores .
  * **04_Partidas.py**: Gerenciamento de Partidas .
  * **05_Cartoes.py**: Gerenciamento de Cartões .
  * **06_Dashboard.py**: Painel analítico com gráficos interativos utilizando Plotly.

## Pré-requisitos

1. **MySQL Server**: Certifique-se de que o servidor do MySQL esteja em execução na sua máquina.
2. **Python 3.8+**: Certifique-se de ter o Python instalado.

## Como Executar o Projeto

### 1. Instalar as dependências

Abra o terminal ou prompt de comando no diretório raiz do projeto e execute:

```bash
pip install -r requirements.txt
```

### 2. Iniciar a aplicação

Execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

### 3. Configurar e Inicializar o Banco de Dados

* Se for a primeira execução e a conexão falhar, a tela inicial exibirá automaticamente um painel de configuração.
* Preencha os campos com os dados de acesso do seu MySQL local (**Host**, **Porta**, **Usuário** e **Senha**).
* Clique no botão **"Inicializar Banco de Dados (Copa_do_Mundo)"** para criar o banco de dados, aplicar o trigger e popular as tabelas com os dados iniciais.
* O sistema irá gerar um arquivo `db_config.json` localmente para salvar as credenciais e recarregará a aplicação automaticamente já conectada.

*Caso queira redefinir a conexão ou recriar o banco a qualquer momento, expanda a aba **"Conexão MySQL"** no menu lateral esquerdo da aplicação e clique em **"Recriar Banco de Dados"**.*

## Funcionalidades e Regras de Negócio

### Trigger de Expulsão 
O sistema conta com um trigger no MySQL associado à tabela `cartoes`. Ao inserir um cartão, o banco de dados verifica automaticamente:
* Se for um cartão **Vermelho** direto: O jogador é marcado como expulso.
* Se for o segundo cartão **Amarelo** recebido pelo mesmo jogador na mesma partida: O jogador é marcado como expulso.

Essa verificação e marcação ocorrem diretamente na camada do banco de dados e são refletidas instantaneamente na listagem de cartões do Streamlit.

### Consultas Não-Triviais
O painel de controle (Dashboard) e as páginas CRUD realizam consultas avançadas no banco de dados utilizando:
* **TIMESTAMPDIFF** para obter a idade exata dos jogadores baseando-se na data de nascimento atual.
* **LEFT JOIN** e **INNER JOIN** para cruzar informações de partidas, seleções, estádios e cartões.
* Funções de agregação como **SUM**, **COUNT** e **AVG** agrupadas via **GROUP BY** para exibir estatísticas como gols por seleção, cartões acumulados e capacidade média dos estádios por país.

# IAAD