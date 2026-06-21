# Copa do Mundo - Cassandra (NoSQL)

## Descrição

Este projeto foi desenvolvido para a disciplina **Introdução ao Armazenamento e Análise de Dados (IAAD)** da Universidade Federal Rural de Pernambuco (UFRPE).

O objetivo é demonstrar o funcionamento de um Banco de Dados NoSQL utilizando o **Apache Cassandra**, tendo como base o domínio "Copa do Mundo de Futebol".

O projeto apresenta:

* Criação do banco Cassandra
* Inserção de dados (Create)
* Consulta de dados (Read)
* Atualização de dados (Update)
* Remoção de dados (Delete)
* Comparação entre MySQL e Cassandra
* Modelagem orientada a consultas

---

# Tecnologias Utilizadas

* Apache Cassandra 5.x
* Docker
* Docker Desktop
* CQL (Cassandra Query Language)

---

# Estrutura do Projeto

```text
copa-do-mundo-cassandra/
│
├── schema.cql
├── seed.cql
├── crud.cql
├── README.md
```

### Arquivos

#### schema.cql

Responsável pela criação do Keyspace e das tabelas Cassandra.

#### seed.cql

Responsável pela carga inicial dos dados.

#### crud.cql

Contém exemplos das operações CRUD utilizadas na apresentação.

#### modelagem.png

Representação visual da modelagem NoSQL utilizada.

---

# Pré-requisitos

Instalar:

* Docker Desktop

Verificar instalação:

```bash
docker --version
```

---

# Executando o Cassandra

Baixar a imagem:

```bash
docker pull cassandra:latest
```

Criar o container:

```bash
docker run --name IAAD_projeto -p 9042:9042 -d cassandra:latest
```

Verificar se o container está ativo:

```bash
docker ps
```

Saída esperada:

```text
CONTAINER ID   IMAGE              STATUS
xxxxxxxxxxxx   cassandra:latest   Up
```

---

# Acessando o Cassandra

Entrar no terminal CQL:

```bash
docker exec -it IAAD_projeto cqlsh
```

Saída esperada:

```text
Connected to Test Cluster
cqlsh>
```

---

# Criando o Banco de Dados

Dentro do cqlsh, execute o conteúdo do arquivo:

```text
schema.cql
```

Ou copie e cole os comandos diretamente no terminal.

Após a execução, selecione o keyspace:

```sql
USE copa_do_mundo_cassandra;
```

---

# Inserindo os Dados

Executar os comandos presentes em:

```text
seed.cql
```

Após a execução, os dados de exemplo estarão disponíveis.

---

# Testando o Banco

Exibir todas as seleções:

```sql
SELECT * FROM selecoes;
```

Exibir jogadores da seleção brasileira:

```sql
SELECT * FROM jogadores_por_selecao
WHERE id_selecao = 1;
```

Exibir partidas:

```sql
SELECT * FROM partidas_por_data;
```

Exibir cartões:

```sql
SELECT * FROM cartoes_por_partida;
```

---

# Operações CRUD

## CREATE

```sql
INSERT INTO selecoes (
id_selecao,
nome_selecao,
continente,
tecnico,
titulos
)
VALUES (
5,
'Portugal',
'Europa',
'Roberto Martinez',
0
);
```

## READ

```sql
SELECT *
FROM selecoes
WHERE id_selecao = 5;
```

## UPDATE

```sql
UPDATE selecoes
SET tecnico = 'Jose Mourinho'
WHERE id_selecao = 5;
```

## DELETE

```sql
DELETE
FROM selecoes
WHERE id_selecao = 5;
```

---

# Modelagem Utilizada

O Cassandra não utiliza:

* Foreign Keys
* JOINs

Por esse motivo, os dados foram modelados de forma orientada às consultas.

Tabelas criadas:

* selecoes
* jogadores_por_selecao
* partidas_por_data
* cartoes_por_partida

A modelagem utiliza desnormalização para facilitar consultas e melhorar desempenho.

---

# Comparação MySQL x Cassandra

| Característica            | MySQL           | Cassandra            |
| ------------------------- | --------------- | -------------------- |
| Modelo                    | Relacional      | NoSQL                |
| JOIN                      | Sim             | Não                  |
| Foreign Key               | Sim             | Não                  |
| Escalabilidade Horizontal | Limitada        | Nativa               |
| Desnormalização           | Pouco utilizada | Amplamente utilizada |
| Consultas                 | Flexíveis       | Orientadas ao acesso |
