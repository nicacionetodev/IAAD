# Sistema de Gerenciamento da Copa do Mundo — CRUD Streamlit + MySQL

Este projeto é um sistema computacional web completo para gerenciamento de dados de seleções, estádios, jogadores, partidas e cartões da Copa do Mundo 2026. Ele possui uma interface desenvolvida com Streamlit e comunicação direta com o banco de dados MySQL.

---

## Pré-requisitos Obrigatórios

Para executar este projeto na sua máquina, é necessário ter instalado:

1. **Python 3.8 ou superior**
2. **Servidor MySQL** ativo e rodando localmente (pode ser o MySQL Community Server, XAMPP, WampServer ou uma instância em Docker).

---

## Guia de Instalação e Execução Completo

### Passo 1: Preparar o Servidor MySQL
Certifique-se de que o seu serviço do MySQL está em execução. O sistema se conectará a este servidor para criar e gerenciar a base de dados.
* O host padrão é `localhost`.
* A porta padrão do MySQL é `3306`.

### Passo 2: Instalar as Dependências do Python
Abra o seu terminal ou prompt de comando (cmd) na pasta raiz do projeto e instale os pacotes necessários executando o comando:

```bash
pip install -r requirements.txt
```

As dependências instaladas serão:
* `streamlit` (interface web)
* `mysql-connector-python` (driver de conexão com o banco)
* `pandas` (manipulação de dados e tabelas)
* `plotly` (geração dos gráficos do painel de controle)

### Passo 3: Executar a Aplicação
Com o servidor do MySQL rodando e as dependências instaladas, inicie o aplicativo executando:

```bash
streamlit run app.py
```

---

## Configuração do Banco de Dados e Conexão (Sem necessidade de importação manual)

Você **não** precisa executar os arquivos `.sql` manualmente no MySQL Workbench ou no terminal. O próprio sistema possui um assistente automatizado de criação:

1. Ao abrir o Streamlit pela primeira vez, caso a conexão padrão falhe, a página exibirá uma tela de configuração intitulada **"Configurações de Acesso"**.
2. Insira as credenciais do seu servidor MySQL local nos campos:
   * **Host** (normalmente `localhost`)
   * **Porta** (normalmente `3306`)
   * **Usuário** (geralmente `root`)
   * **Senha** (insira a senha definida na instalação do seu MySQL)
3. No painel ao lado, clique no botão **"Inicializar Banco de Dados (Copa_do_Mundo)"**.
4. O sistema irá:
   * Criar a base de dados `Copa_do_Mundo` no seu servidor MySQL.
   * Criar todas as tabelas estruturais (`selecoes`, `estadios`, `jogadores`, `partidas` e `cartoes`).
   * Aplicar os triggers necessários para a lógica de expulsões automáticas.
   * Popular as tabelas com um conjunto de teste amplo (16 seleções, 80 jogadores, 16 partidas e 28 cartões).

A aplicação salvará as credenciais localmente no arquivo `db_config.json` e atualizará a tela automaticamente.

---

## Segurança e Controle de Versão

* **db_config.json**: Este arquivo armazena as suas credenciais locais de acesso ao banco (inclusive senhas).
* **.gitignore**: O projeto inclui um arquivo de exclusão que impede o arquivo `db_config.json` de ser enviado para repositórios públicos (como o GitHub), evitando vulnerabilidades de segurança e mantendo as senhas protegidas no seu ambiente de desenvolvimento.

---

## Principais Lógicas e Funcionalidades

###  Trigger de Expulsão Automática
Na tabela de cartões, um trigger é acionado antes de cada inserção:
* Cartões **Vermelhos** diretos marcam o jogador automaticamente como expulso.
* O acúmulo de **2 cartões amarelos** para o mesmo jogador dentro de uma mesma partida aciona a expulsão automática.

###  Dashboard e Consultas Não-Triviais
A aba de Dashboard do sistema apresenta 7 gráficos analíticos criados via Plotly, alimentados por consultas avançadas no MySQL contendo:
* **LEFT JOIN / INNER JOIN** para relacionar jogadores, partidas, estádios e seleções.
* **GROUP BY** associado a funções de agregação (`SUM`, `COUNT`, `AVG`).
* **TIMESTAMPDIFF** para calcular dinamicamente a idade dos jogadores baseando-se na data de nascimento gravada no banco.
