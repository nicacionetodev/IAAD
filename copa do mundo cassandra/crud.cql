USE copa_do_mundo_cassandra;

-- =====================================================
-- CREATE
-- =====================================================
-- Inserindo uma nova seleção

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

-- Verificando inserção

SELECT *
FROM selecoes
WHERE id_selecao = 5;


-- =====================================================
-- READ
-- =====================================================

-- Buscar uma seleção específica

SELECT *
FROM selecoes
WHERE id_selecao = 1;

-- Buscar todos os jogadores do Brasil
-- No MySQL seria necessário JOIN em vários cenários
-- Aqui os dados já estão agrupados pela seleção

SELECT *
FROM jogadores_por_selecao
WHERE id_selecao = 1;

-- Buscar partidas de uma data

SELECT *
FROM partidas_por_data
WHERE data_partida = '2026-06-15';

-- Buscar cartões de uma partida

SELECT *
FROM cartoes_por_partida
WHERE id_partida = 1;


-- =====================================================
-- UPDATE
-- =====================================================

-- Alterar técnico de Portugal

UPDATE selecoes
SET tecnico = 'Jose Mourinho'
WHERE id_selecao = 5;

-- Conferir atualização

SELECT *
FROM selecoes
WHERE id_selecao = 5;


-- Atualizar número de títulos

UPDATE selecoes
SET titulos = 1
WHERE id_selecao = 5;

-- Conferir atualização

SELECT *
FROM selecoes
WHERE id_selecao = 5;


-- =====================================================
-- DELETE
-- =====================================================

-- Remover Portugal

DELETE
FROM selecoes
WHERE id_selecao = 5;

-- Confirmar exclusão

SELECT *
FROM selecoes
WHERE id_selecao = 5;


-- =====================================================
-- CONSULTAS DE RELACIONAMENTO
-- =====================================================

-- Exemplo 1:
-- Todos os jogadores da seleção brasileira

SELECT *
FROM jogadores_por_selecao
WHERE id_selecao = 1;

-- Exemplo 2:
-- Todos os cartões da partida 1

SELECT *
FROM cartoes_por_partida
WHERE id_partida = 1;

-- Exemplo 3:
-- Todas as partidas do dia 15/06/2026

SELECT *
FROM partidas_por_data
WHERE data_partida = '2026-06-15';
