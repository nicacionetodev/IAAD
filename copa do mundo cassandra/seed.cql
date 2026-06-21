USE copa_do_mundo_cassandra;

-- =====================================================
-- SELEÇÕES
-- =====================================================

INSERT INTO selecoes (id_selecao, nome_selecao, continente, tecnico, titulos)
VALUES (1, 'Brasil', 'America do Sul', 'Dorival Junior', 5);

INSERT INTO selecoes (id_selecao, nome_selecao, continente, tecnico, titulos)
VALUES (2, 'Argentina', 'America do Sul', 'Lionel Scaloni', 3);

INSERT INTO selecoes (id_selecao, nome_selecao, continente, tecnico, titulos)
VALUES (3, 'Alemanha', 'Europa', 'Julian Nagelsmann', 4);

INSERT INTO selecoes (id_selecao, nome_selecao, continente, tecnico, titulos)
VALUES (4, 'Franca', 'Europa', 'Didier Deschamps', 2);


-- =====================================================
-- JOGADORES POR SELEÇÃO
-- =====================================================

-- Brasil
INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (1, 1, 'Alisson', 'Goleiro', 1);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (1, 2, 'Marquinhos', 'Zagueiro', 4);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (1, 3, 'Vinicius Junior', 'Atacante', 7);

-- Argentina
INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (2, 1, 'Emiliano Martinez', 'Goleiro', 23);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (2, 2, 'Lionel Messi', 'Atacante', 10);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (2, 3, 'Lautaro Martinez', 'Atacante', 22);

-- Alemanha
INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (3, 1, 'Manuel Neuer', 'Goleiro', 1);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (3, 2, 'Joshua Kimmich', 'Meio-Campista', 6);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (3, 3, 'Jamal Musiala', 'Meio-Campista', 10);

-- França
INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (4, 1, 'Mike Maignan', 'Goleiro', 16);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (4, 2, 'Kylian Mbappe', 'Atacante', 10);

INSERT INTO jogadores_por_selecao (
    id_selecao,
    id_jogador,
    nome_jogador,
    posicao,
    numero_camisa
)
VALUES (4, 3, 'Antoine Griezmann', 'Atacante', 7);


-- =====================================================
-- PARTIDAS
-- =====================================================

INSERT INTO partidas_por_data (
    data_partida,
    id_partida,
    estadio,
    selecao_1,
    selecao_2,
    gols_1,
    gols_2,
    vencedor
)
VALUES (
    '2026-06-15',
    1,
    'MetLife Stadium',
    'Brasil',
    'Alemanha',
    2,
    1,
    'Brasil'
);

INSERT INTO partidas_por_data (
    data_partida,
    id_partida,
    estadio,
    selecao_1,
    selecao_2,
    gols_1,
    gols_2,
    vencedor
)
VALUES (
    '2026-06-15',
    2,
    'Estadio Azteca',
    'Argentina',
    'Franca',
    1,
    1,
    'Empate'
);

INSERT INTO partidas_por_data (
    data_partida,
    id_partida,
    estadio,
    selecao_1,
    selecao_2,
    gols_1,
    gols_2,
    vencedor
)
VALUES (
    '2026-06-18',
    3,
    'SoFi Stadium',
    'Brasil',
    'Argentina',
    3,
    2,
    'Brasil'
);

INSERT INTO partidas_por_data (
    data_partida,
    id_partida,
    estadio,
    selecao_1,
    selecao_2,
    gols_1,
    gols_2,
    vencedor
)
VALUES (
    '2026-06-18',
    4,
    'AT&T Stadium',
    'Alemanha',
    'Franca',
    0,
    2,
    'Franca'
);


-- =====================================================
-- CARTÕES
-- =====================================================

INSERT INTO cartoes_por_partida (
    id_partida,
    id_cartao,
    jogador,
    cor_cartao,
    minuto,
    expulso
)
VALUES (
    1,
    1,
    'Marquinhos',
    'Amarelo',
    35,
    false
);

INSERT INTO cartoes_por_partida (
    id_partida,
    id_cartao,
    jogador,
    cor_cartao,
    minuto,
    expulso
)
VALUES (
    1,
    2,
    'Joshua Kimmich',
    'Amarelo',
    41,
    false
);

INSERT INTO cartoes_por_partida (
    id_partida,
    id_cartao,
    jogador,
    cor_cartao,
    minuto,
    expulso
)
VALUES (
    1,
    3,
    'Vinicius Junior',
    'Vermelho',
    88,
    true
);

INSERT INTO cartoes_por_partida (
    id_partida,
    id_cartao,
    jogador,
    cor_cartao,
    minuto,
    expulso
)
VALUES (
    3,
    1,
    'Lionel Messi',
    'Amarelo',
    22,
    false
);

INSERT INTO cartoes_por_partida (
    id_partida,
    id_cartao,
    jogador,
    cor_cartao,
    minuto,
    expulso
)
VALUES (
    3,
    2,
    'Alisson',
    'Amarelo',
    65,
    false
);