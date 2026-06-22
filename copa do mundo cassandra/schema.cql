CREATE KEYSPACE copa_do_mundo_cassandra
WITH replication = {
    'class': 'SimpleStrategy',
    replication_factor: '1'
};

USE copa_do_mundo_cassandra;

CREATE TABLE selecoes (
    id_selecao int,
    nome_selecao text,
    continente text,
    tecnico text,
    titulos int,
    PRIMARY KEY (id_selecao)
);

CREATE TABLE jogadores_por_selecao (
    id_selecao int,
    id_jogador int,
    nome_jogador text,
    posicao text,
    numero_camisa int,
    PRIMARY KEY (id_selecao, id_jogador)
);

CREATE TABLE estadios (
    id_estadio int, 
    nome_estadio text,
    cidade text,
    pais text,
    capacidade int,
    PRIMARY KEY (id_estadio)
);

CREATE TABLE partidas_por_data (
    data_partida date,
    id_partida int,
    estadio text,
    selecao_1 text,
    selecao_2 text,
    gols_1 int,
    gols_2 int,
    vencedor text,
    PRIMARY KEY (data_partida, id_partida)
);

CREATE TABLE cartoes_por_partida (
    id_partida int,
    id_cartao int,
    jogador text,
    cor_cartao text,
    minuto int,
    expulso boolean,
    PRIMARY KEY (id_partida, id_cartao)
);