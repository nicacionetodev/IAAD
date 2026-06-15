-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Copa_do_Mundo
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `Copa_do_Mundo` ;

-- -----------------------------------------------------
-- Schema Copa_do_Mundo
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Copa_do_Mundo` DEFAULT CHARACTER SET utf8 ;
USE `Copa_do_Mundo` ;

-- -----------------------------------------------------
-- Table `Copa_do_Mundo`.`selecoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa_do_Mundo`.`selecoes` (
  `id_selecao` INT NOT NULL,
  `nome_selecao` VARCHAR(50) NOT NULL,
  `continente` VARCHAR(45) NOT NULL,
  `tecnico` VARCHAR(50) NOT NULL,
  `titulos` INT NOT NULL,
  PRIMARY KEY (`id_selecao`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa_do_Mundo`.`estadios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa_do_Mundo`.`estadios` (
  `id_estadio` INT NOT NULL,
  `nome_estadio` VARCHAR(80) NOT NULL,
  `cidade` VARCHAR(50) NOT NULL,
  `pais` VARCHAR(50) NOT NULL,
  `capacidade` INT NOT NULL,
  PRIMARY KEY (`id_estadio`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa_do_Mundo`.`partidas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa_do_Mundo`.`partidas` (
  `id_partida` INT NOT NULL,
  `data_partida` DATE NOT NULL,
  `id_estadio` INT NOT NULL,
  `id_selecao_1` INT NOT NULL,
  `id_selecao_2` INT NOT NULL,
  `quantidade_gols_selecao_1` INT NOT NULL,
  `quantidade_gols_selecao_2` VARCHAR(45) NOT NULL,
  `vencedor` INT NULL,
  PRIMARY KEY (`id_partida`),
  INDEX `id_estadio_idx` (`id_estadio` ASC) VISIBLE,
  INDEX `id_selecao_1_idx` (`id_selecao_1` ASC) VISIBLE,
  INDEX `id_selecao_2_idx` (`id_selecao_2` ASC) VISIBLE,
  INDEX `vencedor_idx` (`vencedor` ASC) VISIBLE,
  CONSTRAINT `id_estadio`
    FOREIGN KEY (`id_estadio`)
    REFERENCES `Copa_do_Mundo`.`estadios` (`id_estadio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_selecao_1`
    FOREIGN KEY (`id_selecao_1`)
    REFERENCES `Copa_do_Mundo`.`selecoes` (`id_selecao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_selecao_2`
    FOREIGN KEY (`id_selecao_2`)
    REFERENCES `Copa_do_Mundo`.`selecoes` (`id_selecao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `vencedor`
    FOREIGN KEY (`vencedor`)
    REFERENCES `Copa_do_Mundo`.`selecoes` (`id_selecao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa_do_Mundo`.`jogadores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa_do_Mundo`.`jogadores` (
  `id_jogador` INT NOT NULL,
  `nome_jogador` VARCHAR(60) NOT NULL,
  `posicao` VARCHAR(30) NOT NULL,
  `numero_camisa` INT NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `id_selecao` INT NOT NULL,
  PRIMARY KEY (`id_jogador`),
  INDEX `id_selecao_idx` (`id_selecao` ASC) VISIBLE,
  CONSTRAINT `id_selecao`
    FOREIGN KEY (`id_selecao`)
    REFERENCES `Copa_do_Mundo`.`selecoes` (`id_selecao`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa_do_Mundo`.`cartoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa_do_Mundo`.`cartoes` (
  `id_cartao` INT NOT NULL,
  `id_partida` INT NOT NULL,
  `id_jogador` INT NOT NULL,
  `cor_cartao` VARCHAR(15) NOT NULL,
  `minuto` INT NOT NULL,
  PRIMARY KEY (`id_cartao`),
  INDEX `partida_idx` (`id_partida` ASC) VISIBLE,
  INDEX `jogador_idx` (`id_jogador` ASC) VISIBLE,
  CONSTRAINT `partida`
    FOREIGN KEY (`id_partida`)
    REFERENCES `Copa_do_Mundo`.`partidas` (`id_partida`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `jogador`
    FOREIGN KEY (`id_jogador`)
    REFERENCES `Copa_do_Mundo`.`jogadores` (`id_jogador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
