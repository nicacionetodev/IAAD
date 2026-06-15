
USE Copa_do_Mundo;

ALTER TABLE partidas MODIFY COLUMN quantidade_gols_selecao_2 INT NOT NULL;

ALTER TABLE `cartoes` ADD COLUMN `expulso` TINYINT(1) DEFAULT 0;

DROP TRIGGER IF EXISTS trg_verificar_expulsao;

DELIMITER //
CREATE TRIGGER trg_verificar_expulsao
BEFORE INSERT ON `cartoes`
FOR EACH ROW
BEGIN
    DECLARE qtd_amarelos INT;

    -- Cartão vermelho = expulsão direta
    IF NEW.cor_cartao = 'Vermelho' THEN
        SET NEW.expulso = 1;

    -- Segundo cartão amarelo na mesma partida = expulsão
    ELSEIF NEW.cor_cartao = 'Amarelo' THEN
        SELECT COUNT(*) INTO qtd_amarelos
        FROM `cartoes`
        WHERE id_jogador = NEW.id_jogador
          AND id_partida = NEW.id_partida
          AND cor_cartao = 'Amarelo';

        IF qtd_amarelos >= 1 THEN
            SET NEW.expulso = 1;
        END IF;
    END IF;
END //
DELIMITER ;

-- =====================================================
-- Dados iniciais - Seleções
-- =====================================================
INSERT INTO selecoes (id_selecao, nome_selecao, continente, tecnico, titulos) VALUES
(1, 'Brasil', 'América do Sul', 'Dorival Júnior', 5),
(2, 'Argentina', 'América do Sul', 'Lionel Scaloni', 3),
(3, 'Alemanha', 'Europa', 'Julian Nagelsmann', 4),
(4, 'França', 'Europa', 'Didier Deschamps', 2),
(5, 'Espanha', 'Europa', 'Luis de la Fuente', 2),
(6, 'Portugal', 'Europa', 'Roberto Martínez', 0),
(7, 'Uruguai', 'América do Sul', 'Marcelo Bielsa', 2),
(8, 'Croácia', 'Europa', 'Zlatko Dalić', 0),
(9, 'Inglaterra', 'Europa', 'Thomas Tuchel', 1),
(10, 'Itália', 'Europa', 'Luciano Spalletti', 4),
(11, 'Países Baixos', 'Europa', 'Ronald Koeman', 0),
(12, 'Bélgica', 'Europa', 'Domenico Tedesco', 0),
(13, 'Colômbia', 'América do Sul', 'Néstor Lorenzo', 0),
(14, 'México', 'América do Norte', 'Javier Aguirre', 0),
(15, 'Estados Unidos', 'América do Norte', 'Mauricio Pochettino', 0),
(16, 'Japão', 'Ásia', 'Hajime Moriyasu', 0);

-- =====================================================
-- Dados iniciais - Estádios 
-- =====================================================
INSERT INTO estadios (id_estadio, nome_estadio, cidade, pais, capacidade) VALUES
(1, 'MetLife Stadium', 'East Rutherford', 'Estados Unidos', 82500),
(2, 'AT&T Stadium', 'Arlington', 'Estados Unidos', 80000),
(3, 'SoFi Stadium', 'Inglewood', 'Estados Unidos', 70240),
(4, 'Estadio Azteca', 'Cidade do México', 'México', 87523),
(5, 'BMO Field', 'Toronto', 'Canadá', 30000),
(6, 'Hard Rock Stadium', 'Miami Gardens', 'Estados Unidos', 64767),
(7, 'Mercedes-Benz Stadium', 'Atlanta', 'Estados Unidos', 71000),
(8, 'Arrowhead Stadium', 'Kansas City', 'Estados Unidos', 76416);

-- =====================================================
-- Dados iniciais - Jogadores 
-- =====================================================
INSERT INTO jogadores (id_jogador, nome_jogador, posicao, numero_camisa, data_nascimento, id_selecao) VALUES
(1, 'Alisson', 'Goleiro', 1, '1992-10-02', 1),
(2, 'Marquinhos', 'Zagueiro', 4, '1994-05-14', 1),
(3, 'Vinícius Jr.', 'Atacante', 7, '2000-07-12', 1),
(4, 'Rodrygo', 'Atacante', 10, '2001-01-09', 1),
(5, 'Bruno Guimarães', 'Meio-campista', 5, '1997-11-16', 1),
(6, 'Emiliano Martínez', 'Goleiro', 23, '1992-09-02', 2),
(7, 'Lionel Messi', 'Atacante', 10, '1987-06-24', 2),
(8, 'Lautaro Martínez', 'Atacante', 22, '1997-08-22', 2),
(9, 'Rodrigo de Paul', 'Meio-campista', 7, '1994-05-24', 2),
(10, 'Cristian Romero', 'Zagueiro', 13, '1998-04-27', 2),
(11, 'Manuel Neuer', 'Goleiro', 1, '1986-03-27', 3),
(12, 'Joshua Kimmich', 'Meio-campista', 6, '1995-02-08', 3),
(13, 'Kai Havertz', 'Atacante', 7, '1999-06-11', 3),
(14, 'Jamal Musiala', 'Meio-campista', 10, '2003-02-26', 3),
(15, 'Antonio Rüdiger', 'Zagueiro', 2, '1993-03-03', 3),
(16, 'Mike Maignan', 'Goleiro', 16, '1995-07-03', 4),
(17, 'Kylian Mbappé', 'Atacante', 10, '1998-12-20', 4),
(18, 'Antoine Griezmann', 'Atacante', 7, '1991-03-21', 4),
(19, 'Aurélien Tchouaméni', 'Meio-campista', 8, '2000-01-27', 4),
(20, 'William Saliba', 'Zagueiro', 4, '2001-03-24', 4),
(21, 'Unai Simón', 'Goleiro', 23, '1997-06-11', 5),
(22, 'Pedri', 'Meio-campista', 8, '2002-11-25', 5),
(23, 'Lamine Yamal', 'Atacante', 19, '2007-07-13', 5),
(24, 'Rodri', 'Meio-campista', 16, '1996-06-22', 5),
(25, 'Dani Carvajal', 'Zagueiro', 2, '1992-01-11', 5),
(26, 'Diogo Costa', 'Goleiro', 22, '1999-09-19', 6),
(27, 'Cristiano Ronaldo', 'Atacante', 7, '1985-02-05', 6),
(28, 'Bruno Fernandes', 'Meio-campista', 8, '1994-09-08', 6),
(29, 'Bernardo Silva', 'Meio-campista', 10, '1994-08-10', 6),
(30, 'Rúben Dias', 'Zagueiro', 4, '1997-05-14', 6),
(31, 'Sergio Rochet', 'Goleiro', 1, '1993-03-23', 7),
(32, 'Federico Valverde', 'Meio-campista', 15, '1998-07-22', 7),
(33, 'Darwin Núñez', 'Atacante', 11, '1999-06-24', 7),
(34, 'Ronald Araújo', 'Zagueiro', 4, '1999-03-07', 7),
(35, 'Giorgian De Arrascaeta', 'Meio-campista', 10, '1994-06-01', 7),
(36, 'Dominik Livaković', 'Goleiro', 40, '1995-01-09', 8),
(37, 'Luka Modrić', 'Meio-campista', 10, '1985-09-09', 8),
(38, 'Mateo Kovačić', 'Meio-campista', 8, '1994-05-06', 8),
(39, 'Joško Gvardiol', 'Zagueiro', 4, '2002-01-23', 8),
(40, 'Andrej Kramarić', 'Atacante', 9, '1991-06-19', 8),
(41, 'Jordan Pickford', 'Goleiro', 1, '1994-03-07', 9),
(42, 'Harry Kane', 'Atacante', 9, '1993-07-28', 9),
(43, 'Jude Bellingham', 'Meio-campista', 10, '2003-06-29', 9),
(44, 'Bukayo Saka', 'Atacante', 7, '2001-09-05', 9),
(45, 'John Stones', 'Zagueiro', 5, '1994-05-28', 9),
(46, 'Gianluigi Donnarumma', 'Goleiro', 1, '1999-02-25', 10),
(47, 'Nicolò Barella', 'Meio-campista', 18, '1997-02-07', 10),
(48, 'Federico Chiesa', 'Atacante', 14, '1997-10-25', 10),
(49, 'Alessandro Bastoni', 'Zagueiro', 23, '1999-04-13', 10),
(50, 'Mateo Retegui', 'Atacante', 9, '1999-04-29', 10),
(51, 'Bart Verbruggen', 'Goleiro', 1, '2002-08-18', 11),
(52, 'Virgil van Dijk', 'Zagueiro', 4, '1991-07-08', 11),
(53, 'Frenkie de Jong', 'Meio-campista', 21, '1997-05-12', 11),
(54, 'Cody Gakpo', 'Atacante', 11, '1999-05-07', 11),
(55, 'Xavi Simons', 'Meio-campista', 7, '2003-04-21', 11),
(56, 'Koen Casteels', 'Goleiro', 1, '1992-06-25', 12),
(57, 'Kevin De Bruyne', 'Meio-campista', 7, '1991-06-28', 12),
(58, 'Romelu Lukaku', 'Atacante', 10, '1993-05-13', 12),
(59, 'Jeremy Doku', 'Atacante', 11, '2002-05-27', 12),
(60, 'Wout Faes', 'Zagueiro', 4, '1998-04-03', 12),
(61, 'Camilo Vargas', 'Goleiro', 12, '1989-03-09', 13),
(62, 'James Rodríguez', 'Meio-campista', 10, '1991-07-12', 13),
(63, 'Luis Díaz', 'Atacante', 7, '1997-01-13', 13),
(64, 'Davinson Sánchez', 'Zagueiro', 23, '1996-06-12', 13),
(65, 'Richard Ríos', 'Meio-campista', 6, '2000-06-02', 13),
(66, 'Luis Malagón', 'Goleiro', 1, '1997-03-02', 14),
(67, 'Edson Álvarez', 'Meio-campista', 4, '1997-10-24', 14),
(68, 'Santiago Giménez', 'Atacante', 11, '2001-04-18', 14),
(69, 'César Montes', 'Zagueiro', 3, '1997-02-24', 14),
(70, 'Luis Chávez', 'Meio-campista', 24, '1996-01-15', 14),
(71, 'Matt Turner', 'Goleiro', 1, '1994-06-24', 15),
(72, 'Christian Pulisic', 'Atacante', 10, '1998-09-18', 15),
(73, 'Weston McKennie', 'Meio-campista', 8, '1998-08-28', 15),
(74, 'Antonee Robinson', 'Zagueiro', 5, '1997-08-08', 15),
(75, 'Folarin Balogun', 'Atacante', 9, '2001-07-03', 15),
(76, 'Zion Suzuki', 'Goleiro', 1, '2002-08-21', 16),
(77, 'Wataru Endo', 'Meio-campista', 6, '1993-02-09', 16),
(78, 'Kaoru Mitoma', 'Atacante', 7, '1997-05-20', 16),
(79, 'Takefusa Kubo', 'Atacante', 20, '2001-06-04', 16),
(80, 'Ko Itakura', 'Zagueiro', 4, '1997-01-27', 16);

-- =====================================================
-- Dados iniciais - Partidas
-- =====================================================
INSERT INTO partidas (id_partida, data_partida, id_estadio, id_selecao_1, id_selecao_2, quantidade_gols_selecao_1, quantidade_gols_selecao_2, vencedor) VALUES
(1, '2026-06-15', 1, 1, 3, 2, 1, 1),
(2, '2026-06-15', 4, 2, 5, 3, 0, 2),
(3, '2026-06-16', 3, 4, 7, 1, 1, NULL),
(4, '2026-06-16', 2, 6, 8, 2, 0, 6),
(5, '2026-06-17', 7, 9, 10, 1, 2, 10),
(6, '2026-06-17', 8, 11, 12, 2, 2, NULL),
(7, '2026-06-18', 4, 13, 14, 3, 1, 13),
(8, '2026-06-18', 6, 15, 16, 2, 1, 15),
(9, '2026-06-20', 1, 1, 2, 1, 0, 1),
(10, '2026-06-20', 3, 3, 5, 2, 2, NULL),
(11, '2026-06-21', 2, 4, 6, 0, 1, 6),
(12, '2026-06-21', 8, 7, 8, 3, 2, 7),
(13, '2026-06-22', 6, 9, 11, 1, 0, 9),
(14, '2026-06-22', 7, 10, 12, 0, 0, NULL),
(15, '2026-06-23', 5, 13, 15, 4, 2, 13),
(16, '2026-06-23', 4, 14, 16, 1, 2, 16);

-- =====================================================
-- Dados iniciais - Cartões
-- =====================================================
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (1, 1, 2, 'Amarelo', 34);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (2, 1, 12, 'Amarelo', 45);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (3, 1, 3, 'Vermelho', 85);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (4, 2, 22, 'Amarelo', 30);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (5, 2, 9, 'Amarelo', 41);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (6, 2, 22, 'Amarelo', 75);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (7, 3, 19, 'Amarelo', 18);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (8, 3, 34, 'Amarelo', 55);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (9, 4, 28, 'Amarelo', 12);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (10, 4, 37, 'Amarelo', 40);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (11, 4, 37, 'Amarelo', 80);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (12, 5, 45, 'Amarelo', 60);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (13, 5, 47, 'Amarelo', 72);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (14, 6, 52, 'Amarelo', 15);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (15, 6, 60, 'Amarelo', 22);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (16, 6, 52, 'Amarelo', 60);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (17, 7, 64, 'Amarelo', 37);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (18, 7, 67, 'Amarelo', 51);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (19, 8, 72, 'Amarelo', 10);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (20, 8, 77, 'Amarelo', 30);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (21, 8, 72, 'Amarelo', 88);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (22, 8, 78, 'Vermelho', 90);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (23, 9, 5, 'Amarelo', 28);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (24, 9, 10, 'Amarelo', 33);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (25, 11, 18, 'Amarelo', 62);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (26, 12, 33, 'Amarelo', 44);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (27, 12, 39, 'Amarelo', 71);
INSERT INTO `cartoes` (`id_cartao`, id_partida, id_jogador, cor_cartao, minuto) VALUES (28, 15, 65, 'Amarelo', 15);
