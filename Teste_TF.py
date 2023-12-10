import mysql.connector
from mysql.connector import errorcode
import matplotlib.pyplot as plt
import numpy as np

# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {
'PESSOA': ("""CREATE TABLE IF NOT EXISTS `aaaca`.`pessoa` (
  `CPF` VARCHAR(20) NOT NULL,
  `Nome` VARCHAR(100) NULL DEFAULT NULL,
  `Telefone` VARCHAR(20) NULL DEFAULT NULL,
  `Email` VARCHAR(100) NULL DEFAULT NULL,
  `Aluno` TINYINT(1) NULL DEFAULT NULL,
  `Aniversario` VARCHAR(100) NULL DEFAULT NULL,
  `Sexo` VARCHAR(30) NULL DEFAULT NULL,
  PRIMARY KEY (`CPF`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;"""),
    'ASSOCIACAO': ("""CREATE TABLE IF NOT EXISTS `aaaca`.`associacao` (
  `ID_Associacao` INT NOT NULL AUTO_INCREMENT,
  `Tipo` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Associacao`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'SOCIO_ASSOCIADO': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`socio_associado` (
  `Status` TINYINT(1) NULL DEFAULT NULL,
  `Data_Filiacao` TIMESTAMP NULL DEFAULT NULL,
  `ID_Socio` INT NOT NULL AUTO_INCREMENT,
  `fk_Associacao_ID_Associacao` INT NULL DEFAULT NULL,
  `fk_Pessoa_CPF` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Socio`),
  INDEX `FK_Socio_Associado_2` (`fk_Associacao_ID_Associacao` ASC) VISIBLE,
  INDEX `FK_Socio_Associado_3` (`fk_Pessoa_CPF` ASC) VISIBLE,
  CONSTRAINT `FK_Socio_Associado_2`
    FOREIGN KEY (`fk_Associacao_ID_Associacao`)
    REFERENCES `aaaca`.`associacao` (`ID_Associacao`),
  CONSTRAINT `FK_Socio_Associado_3`
    FOREIGN KEY (`fk_Pessoa_CPF`)
    REFERENCES `aaaca`.`pessoa` (`CPF`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'MODALIDADE': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`modalidade` (
  `ID_Modalidade` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Modalidade`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'PRODUTO': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`produto` (
  `ID_Produto` INT NOT NULL AUTO_INCREMENT,
  `Descricao` VARCHAR(100) NULL DEFAULT NULL,
  `Quantidade` INT NULL DEFAULT NULL,
  `Valor` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Produto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

"""),
    'FORNECEDOR': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`fornecedor` (
  `ID_Fornecedor` INT NOT NULL AUTO_INCREMENT,
  `Descricao` VARCHAR(100) NULL DEFAULT NULL,
  `Contato` VARCHAR(100) NULL DEFAULT NULL,
  `Nome` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Fornecedor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'SETOR': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`setor` (
  `Nome` VARCHAR(100) NULL DEFAULT NULL,
  `ID_Setor` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID_Setor`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'CARGO': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`cargo` (
  `ID_Cargo` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Cargo`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'MATERIAL_ESPORTIVO': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`material_esportivo` (
  `ID_Material` INT NOT NULL AUTO_INCREMENT,
  `Quantidade` INT NULL DEFAULT NULL,
  `Descricao` VARCHAR(100) NULL DEFAULT NULL,
  `Nome` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Material`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'VENDA': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`venda` (
  `Data` TIMESTAMP NULL DEFAULT NULL,
  `ID_Venda` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ID_Venda`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'COMPRA': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`compra` (
  `ID_Compra` INT NOT NULL AUTO_INCREMENT,
  `Data` TIMESTAMP NULL DEFAULT NULL,
  `fk_Fornecedor_ID_Fornecedor` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Compra`),
  INDEX `FK_Compra_2` (`fk_Fornecedor_ID_Fornecedor` ASC) VISIBLE,
  CONSTRAINT `FK_Compra_2`
    FOREIGN KEY (`fk_Fornecedor_ID_Fornecedor`)
    REFERENCES `aaaca`.`fornecedor` (`ID_Fornecedor`)
    ON DELETE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'GESTAO_PERTENCE': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`gestao_pertence` (
  `ID_Gestao` INT NOT NULL AUTO_INCREMENT,
  `Data_Saida` TIMESTAMP NULL DEFAULT NULL,
  `Data_Entrada` TIMESTAMP NULL DEFAULT NULL,
  `fk_Setor_ID_Setor` INT NULL DEFAULT NULL,
  `fk_Socio_Associado_ID_Socio` INT NULL DEFAULT NULL,
  `fk_Cargo_ID_Cargo` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ID_Gestao`),
  INDEX `FK_Gestao_Pertence_2` (`fk_Setor_ID_Setor` ASC) VISIBLE,
  INDEX `FK_Gestao_Pertence_3` (`fk_Socio_Associado_ID_Socio` ASC) VISIBLE,
  INDEX `FK_Gestao_Pertence_4` (`fk_Cargo_ID_Cargo` ASC) VISIBLE,
  CONSTRAINT `FK_Gestao_Pertence_2`
    FOREIGN KEY (`fk_Setor_ID_Setor`)
    REFERENCES `aaaca`.`setor` (`ID_Setor`)
    ON DELETE CASCADE,
  CONSTRAINT `FK_Gestao_Pertence_3`
    FOREIGN KEY (`fk_Socio_Associado_ID_Socio`)
    REFERENCES `aaaca`.`socio_associado` (`ID_Socio`),
  CONSTRAINT `FK_Gestao_Pertence_4`
    FOREIGN KEY (`fk_Cargo_ID_Cargo`)
    REFERENCES `aaaca`.`cargo` (`ID_Cargo`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
"""),
    'ATLETA': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`atleta` (
  `fk_Modalidade_ID_Modalidade` INT NULL DEFAULT NULL,
  `fk_Socio_Associado_ID_Socio` INT NULL DEFAULT NULL,
  INDEX `FK_Atleta_1` (`fk_Modalidade_ID_Modalidade` ASC) VISIBLE,
  INDEX `FK_Atleta_2` (`fk_Socio_Associado_ID_Socio` ASC) VISIBLE,
  CONSTRAINT `FK_Atleta_1`
    FOREIGN KEY (`fk_Modalidade_ID_Modalidade`)
    REFERENCES `aaaca`.`modalidade` (`ID_Modalidade`)
    ON DELETE RESTRICT,
  CONSTRAINT `FK_Atleta_2`
    FOREIGN KEY (`fk_Socio_Associado_ID_Socio`)
    REFERENCES `aaaca`.`socio_associado` (`ID_Socio`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'MODALIDADE_MATERIAL': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`modalidade_material` (
  `fk_Material_Esporivo_ID_Material` INT NULL DEFAULT NULL,
  `fk_Modalidade_ID_Modalidade` INT NULL DEFAULT NULL,
  INDEX `FK_Modalidade_Material_1` (`fk_Material_Esporivo_ID_Material` ASC) VISIBLE,
  INDEX `FK_Modalidade_Material_2` (`fk_Modalidade_ID_Modalidade` ASC) VISIBLE,
  CONSTRAINT `FK_Modalidade_Material_1`
    FOREIGN KEY (`fk_Material_Esporivo_ID_Material`)
    REFERENCES `aaaca`.`material_esportivo` (`ID_Material`)
    ON DELETE RESTRICT,
  CONSTRAINT `FK_Modalidade_Material_2`
    FOREIGN KEY (`fk_Modalidade_ID_Modalidade`)
    REFERENCES `aaaca`.`modalidade` (`ID_Modalidade`)
    ON DELETE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

"""),
    'GESTAO_REALIZA_VENDA': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`gestao_realiza_venda` (
  `fk_Venda_ID_Venda` INT NULL DEFAULT NULL,
  `fk_Gestao_Pertence_ID_Gestao` INT NULL DEFAULT NULL,
  INDEX `FK_Gestao_Realiza_Venda_1` (`fk_Venda_ID_Venda` ASC) VISIBLE,
  INDEX `FK_Gestao_Realiza_Venda_2` (`fk_Gestao_Pertence_ID_Gestao` ASC) VISIBLE,
  CONSTRAINT `FK_Gestao_Realiza_Venda_1`
    FOREIGN KEY (`fk_Venda_ID_Venda`)
    REFERENCES `aaaca`.`venda` (`ID_Venda`)
    ON DELETE SET NULL,
  CONSTRAINT `FK_Gestao_Realiza_Venda_2`
    FOREIGN KEY (`fk_Gestao_Pertence_ID_Gestao`)
    REFERENCES `aaaca`.`gestao_pertence` (`ID_Gestao`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

"""),
    'VENDA_PRODUTO': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`venda_produto` (
  `fk_Produto_ID_Produto` INT NULL DEFAULT NULL,
  `fk_Venda_ID_Venda` INT NULL DEFAULT NULL,
  `Quantidade` INT NULL DEFAULT NULL,
  `Valor` FLOAT NULL DEFAULT NULL,
  INDEX `FK_Venda_Produto_1` (`fk_Produto_ID_Produto` ASC) VISIBLE,
  INDEX `FK_Venda_Produto_2` (`fk_Venda_ID_Venda` ASC) VISIBLE,
  CONSTRAINT `FK_Venda_Produto_1`
    FOREIGN KEY (`fk_Produto_ID_Produto`)
    REFERENCES `aaaca`.`produto` (`ID_Produto`)
    ON DELETE RESTRICT,
  CONSTRAINT `FK_Venda_Produto_2`
    FOREIGN KEY (`fk_Venda_ID_Venda`)
    REFERENCES `aaaca`.`venda` (`ID_Venda`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'GESTAO_EFETUA_COMPRA': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`gestao_efetua_compra` (
  `fk_Compra_ID_Compra` INT NULL DEFAULT NULL,
  `fk_Gestao_Pertence_ID_Gestao` INT NULL DEFAULT NULL,
  INDEX `FK_Gestao_Efetua_Compra_1` (`fk_Compra_ID_Compra` ASC) VISIBLE,
  INDEX `FK_Gestao_Efetua_Compra_2` (`fk_Gestao_Pertence_ID_Gestao` ASC) VISIBLE,
  CONSTRAINT `FK_Gestao_Efetua_Compra_1`
    FOREIGN KEY (`fk_Compra_ID_Compra`)
    REFERENCES `aaaca`.`compra` (`ID_Compra`)
    ON DELETE SET NULL,
  CONSTRAINT `FK_Gestao_Efetua_Compra_2`
    FOREIGN KEY (`fk_Gestao_Pertence_ID_Gestao`)
    REFERENCES `aaaca`.`gestao_pertence` (`ID_Gestao`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
"""),
    'COMPRA_PRODUTO': (
        """CREATE TABLE IF NOT EXISTS `aaaca`.`compra_produto` (
  `fk_Produto_ID_Produto` INT NULL DEFAULT NULL,
  `fk_Compra_ID_Compra` INT NULL DEFAULT NULL,
  `Quantidade` INT NULL DEFAULT NULL,
  `Valor` FLOAT NULL DEFAULT NULL,
  INDEX `FK_Compra_Produto_1` (`fk_Produto_ID_Produto` ASC) VISIBLE,
  INDEX `FK_Compra_Produto_2` (`fk_Compra_ID_Compra` ASC) VISIBLE,
  CONSTRAINT `FK_Compra_Produto_1`
    FOREIGN KEY (`fk_Produto_ID_Produto`)
    REFERENCES `aaaca`.`produto` (`ID_Produto`)
    ON DELETE RESTRICT,
  CONSTRAINT `FK_Compra_Produto_2`
    FOREIGN KEY (`fk_Compra_ID_Compra`)
    REFERENCES `aaaca`.`compra` (`ID_Compra`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;
""")
}

# Valores para serem inseridos no Banco de Dados
inserts= {'PESSOA': (
    """INSERT INTO PESSOA (aniversario, aluno, email, telefone, sexo, cpf, nome) VALUES
        ('1990-05-15', 1, 'joao.silva@email.com', '(12)34567-8901', 'M', '125.456.789-01', 'João Silva'),
        ('1998-02-10', 1, 'carlos.souza@email.com', '(55)51234-5678', 'M', '555.666.767-01', 'Carlos Souza'),
        ('1976-11-30', 0, 'maria.pereira@email.com', '(11)12223-3333', 'F', '111.252.333-01', 'Maria Pereira'),
        ('2000-07-05', 1, 'laura.oliveira@email.com', '(99)98887-7777', 'F', '999.888.777-01', 'Laura Oliveira'),
        ('1982-04-18', 0, 'pedro.silva@email.com', '(44)45556-6666', 'M', '444.555.666-01', 'Pedro Silva'),
        ('1995-09-25', 1, 'claudia.souza@email.com', '(77)76665-5555', 'F', '777.666.552-01', 'Claudia Souza'),
        ('1988-12-12', 0, 'roberto.pereira@email.com', '(22)23334-4444', 'M', '222.333.444-01', 'Roberto Pereira'),
        ('1993-03-08', 1, 'amanda.silva@email.com', '(88)89990-0000', 'F', '888.999.000-01', 'Amanda Silva'),
        ('1970-01-20', 0, 'felipe.souza@email.com', '(33)34445-5555', 'M', '333.444.555-01', 'Felipe Souza'),
        ('1987-06-14', 1, 'sandra.oliveira@email.com', '(77)76665-5555', 'F', '555.666.777-02', 'Sandra Oliveira'),
        ('1991-09-30', 0, 'rodrigo.silva@email.com', '(77)78889-9999', 'M', '777.888.999-02', 'Rodrigo Silva'),
        ('1980-04-02', 1, 'patricia.souza@email.com', '(11)12223-3333', 'F', '111.222.333-02', 'Patricia Souza'),
        ('1994-11-17', 0, 'carolina.pereira@email.com', '(44)45556-6666', 'F', '444.555.666-02', 'Carolina Pereira'),
        ('1975-08-23', 1, 'gustavo.silva@email.com', '(99)98887-7777', 'M', '999.888.777-02', 'Gustavo Silva'),
        ('1983-12-07', 0, 'luis.souza@email.com', '(33)34445-5555', 'M', '333.444.555-02', 'Luis Souza'),
        ('1999-02-28', 1, 'marina.oliveira@email.com', '(77)76665-5555', 'F', '777.666.555-02', 'Marina Oliveira'),
        ('1978-05-10', 0, 'vitor.pereira@email.com', '(22)23334-4444', 'M', '222.333.444-02', 'Vitor Pereira'),
        ('1989-10-05', 1, 'isabela.silva@email.com', '(88)89990-0000', 'F', '888.999.000-02', 'Isabela Silva'),
        ('1996-03-19', 0, 'renato.souza@email.com', '(55)56667-7777', 'M', '555.666.777-03', 'Renato Souza'),
        ('1990-05-15', 1, 'isa.silva@email.com', '(12)34567-8901', 'F', '123.456.789-11', 'Isa Silva'),
        ('1985-08-22', 0, 'ana.oliveira@email.com', '(98)76543-2101', 'F', '987.654.321-11', 'Ana Oliveira'),
        ('1998-02-10', 1, 'felipe.souza@email.com', '(55)51234-5678', 'M', '555.666.777-11', 'Felipe Souza'),
        ('1976-11-30', 0, 'bernardo.pereira@email.com', '(11)12223-3333', 'M', '111.222.333-11', 'Bernardo Pereira'),
        ('2000-07-05', 1, 'julia.oliveira@email.com', '(99)98887-7777', 'F', '999.888.777-11', 'Julia Oliveira'),
        ('1982-04-18', 0, 'matheus.silva@email.com', '(44)45556-6666', 'M', '444.555.666-11', 'Matheus Silva'),
        ('1995-09-25', 1, 'carla.souza@email.com', '(77)76665-5555', 'F', '777.666.555-11', 'Carla Souza'),
        ('1988-12-12', 0, 'gabriel.pereira@email.com', '(22)23334-4444', 'M', '222.333.444-11', 'Gabriel Pereira'),
        ('1993-03-08', 1, 'lais.silva@email.com', '(88)89990-0000', 'F', '888.999.000-11', 'Lais Silva'),
        ('1970-01-20', 0, 'marcio.souza@email.com', '(33)34445-5555', 'M', '333.444.555-11', 'Marcio Souza'),
        ('1991-06-14', 1, 'ana.carvalho@email.com', '(55)51112-2222', 'F', '555.111.222-11', 'Ana Carvalho'),
        ('1987-09-29', 0, 'rafael.silva@email.com', '(77)78889-9999', 'M', '777.888.999-11', 'Rafael Silva'),
        ('1996-04-03', 1, 'larissa.oliveira@email.com', '(44)49995-5555', 'F', '444.999.555-11', 'Larissa Oliveira')"""),

    'ASSOCIACAO': (
        """insert into ASSOCIACAO (id_associacao, tipo) values
        (1, 'socio interno'),
        (2, 'socio externo'),
        (3, 'socio atleta'),
        (4, 'gestao')"""),
    'SOCIO_ASSOCIADO': (
        """insert into SOCIO_ASSOCIADO (fk_Associacao_ID_Associacao, id_socio, fk_Pessoa_CPF, status, data_filiacao) values
        (1, 1, '125.456.789-01', '1', '2022-01-01'),
        (1, 2, '555.666.767-01', '1', '2022-02-01'),
        (1, 3, '111.252.333-01', '1', '2022-03-01'),
        (2, 4, '999.888.777-01', '1', '2022-04-01'),
        (2, 5, '444.555.666-01', '1', '2022-05-01'),
        (2, 6, '777.666.552-01', '1', '2022-06-01'),
        (3, 7, '555.666.777-02', '0', '2022-07-01'),
        (3, 8, '777.888.999-02', '1', '2022-08-01'),
        (3, 9, '111.222.333-02', '1', '2022-09-01'),
        (4, 10, '888.999.000-02', '1', '2022-10-01'),
        (4, 11, '333.444.555-02', '0', '2022-11-01'),
        (4, 12, '555.666.777-03', '1', '2022-12-01'),
        (1, 13, '123.456.789-11', '1', '2023-01-01'),
        (2, 14, '987.654.321-11', '1', '2023-02-01'),
        (3, 15, '555.666.777-11', '1', '2023-03-01'),
        (4, 16, '111.222.333-11', '0', '2023-04-01'),
        (1, 17, '999.888.777-11', '1', '2023-05-01'),
        (2, 18, '444.555.666-11', '0', '2023-06-01'),
        (3, 19, '777.666.555-11', '1', '2023-07-01'),
        (4, 20, '222.333.444-11', '0', '2023-08-01'),
        (1, 21, '888.999.000-11', '1', '2023-09-01'),
        (2, 22, '555.111.222-11', '0', '2023-10-01'),
        (3, 23, '777.888.999-11', '1', '2023-11-01'),
        (4, 24, '444.999.555-11', '1', '2023-12-01')"""),
    'MODALIDADE': (
        """insert into MODALIDADE (id_modalidade, nome) values
        (1, 'Futsal'),
        (2, 'Basquete'),
        (3, 'Vôlei'),
        (4, 'Natação'),
        (5, 'Atletismo'),
        (6, 'Handebol'),
        (7, 'Futvolei'),
        (8, 'Tênis'),
        (9, 'Tênis de mesa'),
        (10, 'Xadrez')"""),
    'MATERIAL_ESPORTIVO': (
        """insert into MATERIAL_ESPORTIVO (Id_material, nome, quantidade, descricao) values
        (1, 'Bola de Futsal', 4, 'Bola esportiva para Futsal'),
        (2, 'Bola de Basquete', 5, 'Bola esportiva para Basquete'),
        (3, 'Bola de Vôlei', 11, 'Bola esportiva para Vôlei'),
        (4, 'Touca de Natação', 15, 'Touca para Natação'),
        (5, 'Barreiras de Corrida', 10, 'Barreiras para salto em distancia'),
        (6, 'Bola de Handebol', 6, 'Bola esportiva para Handebol'),
        (7, 'Bola de Futvolei', 2, 'Bola esportiva para Futvolei'),
        (8, 'Raquete de Tênis', 3, 'Raquete para Tênis'),
        (9, 'Raquete de Tênis de Mesa', 5, 'Raquete para Tênis de Mesa'),
        (10, 'Tabuleiro de Xadrez', 5, 'Tabuleiro e peças para Xadrez'),
        (11, 'Rede', 2, 'Rede esportiva para Futevôlei e Vôlei'),
        (12, 'Bomba para Regular Pressão', 5, 'Bomba utilizada para regular a pressão de diversas bolas')"""),
    'MODALIDADE_MATERIAL': (
        """insert into MODALIDADE_MATERIAL (fk_Modalidade_ID_Modalidade, fk_Material_Esporivo_ID_Material) values
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (7, 11),
        (3, 11),
        (7, 12),
        (3, 12),
        (1, 12)"""),
    'ATLETA': (
        """insert into ATLETA (fk_Socio_Associado_ID_Socio, fk_Modalidade_ID_Modalidade) values
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 1),
        (12, 2),
        (13, 3),
        (14, 4),
        (15, 5),
        (16, 6),
        (17, 7),
        (18, 8),
        (19, 9),
        (20, 10),
        (21, 1),
        (22, 2),
        (23, 3),
        (24, 4)
        """),
    'SETOR': (
        """insert into SETOR (id_setor, nome) values
        (1, 'Presidência'),
        (2, 'Marketing'),
        (3, 'Comercial'),
        (4, 'Gestão de Pessoas'),
        (5, 'Financeiro')
        """),
    'CARGO': (
        """insert into CARGO (id_cargo, nome) values
        (1, 'Presidente'),
        (2, 'Vice-Presidente'),
        (3, 'Tesoureiro'),
        (4, 'Conselheiro'),
        (5, 'Diretor'),
        (6, 'Gerente'),
        (7, 'Assessor')
        """),
    'GESTAO_PERTENCE': (
        """insert into GESTAO_PERTENCE (id_gestao,fk_Socio_Associado_ID_Socio, fk_Cargo_ID_Cargo, fk_Setor_ID_Setor, data_entrada, data_saida) values
        (1, 1, 1, 1, '2022-01-01', '2023-01-01'),
        (2, 2, 2, 2, '2022-02-01', '2023-02-01'),
        (3, 3, 3, 3, '2022-03-01', '2023-03-01'),
        (4, 4, 4, 4, '2022-04-01', '2023-04-01'),
        (5, 5, 5, 5, '2022-05-01', '2023-05-01'),
        (6, 6, 6, 5, '2022-06-01', '2023-06-01'),
        (7, 7, 7, 4, '2022-07-01', '2023-07-01'),
        (8, 8, 1, 3, '2022-08-01', '2023-08-01'),
        (9, 9, 2, 1, '2022-09-01', '2023-09-01'),
        (10, 10, 3, 2, '2022-10-01', '2023-10-01'),
        (11, 11, 4, 3, '2022-11-01', '2023-11-01'),
        (12, 12, 5, 4, '2022-12-01', '2023-12-01'),
        (13, 13, 6, 5, '2023-01-01', '2024-01-01'),
        (14, 14, 7, 5, '2023-02-01', '2024-02-01'),
        (15, 15, 1, 4, '2023-03-01', '2024-03-01'),
        (16, 16, 2, 2, '2023-04-01', '2024-04-01')"""),
    'PRODUTO': (
        """insert into PRODUTO (id_produto, valor, descricao, quantidade) values
        (1, 20.00, 'Ingresso Festa Fantasia', 500),
        (2, 20.00, 'Ingresso Festa 10 Anos', 500),
        (3, 30.00, 'Camiseta 10 Anos', 100),
        (4, 30.00, 'Camiseta 23.1', 100),
        (5, 50.00, 'Moletom Estilizado', 50),
        (6, 10.00, 'Caneca Padrão', 100),
        (7, 15.00, 'Caneca Uni', 50),
        (8, 40.00, 'Kit Universipraia (Ingresso + Camiseta)', 200),
        (9, 20.00, 'Ingresso Universipraia', 500),
        (10, 25.00, 'Boné AAACA', 30)
        """),
    'FORNECEDOR': (
        """insert into FORNECEDOR (id_fornecedor, descricao, contato, nome) values
        (1, 'Fornecedor de tecidos', 'contato@fornecedor1.com', 'ArtImpressoes'),
        (2, 'Fornecedor de plástico', 'contato@fornecedor2.com', 'Multitecidos'),
        (3, 'Fornecedor de papel', 'contato@fornecedor3.com', 'PrintSupplies'),
        (4, 'Fornecedor de metal', 'contato@fornecedor4.com', 'MetalArts'),
        (5, 'Fornecedor de camisetas', 'contato@fornecedor5.com', 'TextilStyle'),
        (6, 'Fornecedor de canecas', 'contato@fornecedor6.com', 'CeramicWonders'),
        (7, 'Fornecedor de ingressos', 'contato@fornecedor7.com', 'TicketMaster'),
        (8, 'Fornecedor de brindes', 'contato@fornecedor8.com', 'GiftHub'),
        (9, 'Fornecedor de produtos esportivos', 'contato@fornecedor9.com', 'SportsGearCo'),
        (10, 'Fornecedor de embalagens', 'contato@fornecedor10.com', 'PackagingSolutions')
        """),
    'COMPRA': (
        """insert into COMPRA (id_compra, data, fk_Fornecedor_ID_Fornecedor) values
        (1, '2023-01-10',1),
        (2, '2023-02-15',1),
        (3, '2023-03-20',3),
        (4, '2023-04-25',2),
        (5, '2023-05-30',4),
        (6, '2023-06-05',5),
        (7, '2023-07-10',6),
        (8, '2023-08-15',7),
        (9, '2023-09-20',8),
        (10, '2023-10-25',9)
        """),
    'VENDA': (
        """insert into VENDA (id_venda, data) values
        (1, '2023-01-12'),
        (2, '2023-02-17'),
        (3, '2023-03-22'),
        (4, '2023-04-27'),
        (5, '2023-06-01'),
        (6, '2023-06-08'),
        (7, '2023-07-12'),
        (8, '2023-08-17'),
        (9, '2023-09-22'),
        (10, '2023-11-01')
        """),
    'COMPRA_PRODUTO': (
        """insert into COMPRA_PRODUTO (fk_Compra_ID_Compra, fk_Produto_ID_Produto, quantidade, valor) values
        (1, 1, 100, 200.00),
        (2, 1, 150, 300.00),
        (2, 2, 100, 100.00),
        (3, 3, 50, 150.00),
        (4, 4, 50, 150.00),
        (5, 5, 20, 100.00),
        (6, 6, 50, 500.00),
        (7, 7, 30, 450.00),
        (8, 8, 100, 400.00),
        (9, 9, 200, 400.00),
        (10, 10, 20, 500.00)
        """),
    'VENDA_PRODUTO': (
        """insert into VENDA_PRODUTO (fk_Venda_ID_Venda, fk_Produto_ID_Produto, quantidade, valor) values
        (1, 1, 10, 200.00),
        (2, 2, 15, 300.00),
        (3, 3, 5, 150.00),
        (4, 4, 5, 150.00),
        (5, 5, 2, 100.00),
        (6, 6, 20, 200.00),
        (7, 7, 10, 150.00),
        (8, 8, 5, 200.00),
        (9, 9, 10, 200.00),
        (10, 10, 3, 75.00)
        """),
    'GESTAO_EFETUA_COMPRA': (
        """insert into GESTAO_EFETUA_COMPRA (fk_Gestao_Pertence_ID_Gestao, fk_Compra_ID_Compra) values
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
        """),
    'GESTAO_REALIZA_VENDA': (
        """insert into GESTAO_REALIZA_VENDA (fk_Gestao_Pertence_ID_Gestao, fk_Venda_ID_Venda) values
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
        """)    
}

# Valores para deletar as tabelas
drop = {
    'VENDA_PRODUTO': ("DROP TABLE IF EXISTS aaaca.venda_produto"),
    'COMPRA_PRODUTO': ("DROP TABLE IF EXISTS aaaca.compra_produto"),
    'ATLETA': ("DROP TABLE IF EXISTS aaaca.atleta"),
    'MODALIDADE_MATERIAL': ("DROP TABLE IF EXISTS aaaca.modalidade_material"),
    'GESTAO_REALIZA_VENDA': ("DROP TABLE IF EXISTS aaaca.gestao_realiza_venda"),
    'GESTAO_EFETUA_COMPRA': ("DROP TABLE IF EXISTS aaaca.gestao_efetua_compra"),
    'GESTAO_PERTENCE': ("DROP TABLE IF EXISTS aaaca.gestao_pertence"),
    'SOCIO_ASSOCIADO': ("DROP TABLE IF EXISTS aaaca.socio_associado"),
    'VENDA': ("DROP TABLE IF EXISTS aaaca.venda"),
    'COMPRA': ("DROP TABLE IF EXISTS aaaca.compra"),
    'MODALIDADE': ("DROP TABLE IF EXISTS aaaca.modalidade"),
    'MATERIAL_ESPORTIVO': ("DROP TABLE IF EXISTS aaaca.material_esportivo"),
    'CARGO': ("DROP TABLE IF EXISTS aaaca.cargo"),
    'SETOR': ("DROP TABLE IF EXISTS aaaca.setor"),
    'ASSOCIACAO': ("DROP TABLE IF EXISTS aaaca.associacao"),
    'PRODUTO': ("DROP TABLE IF EXISTS aaaca.produto"),
    'FORNECEDOR': ("DROP TABLE IF EXISTS aaaca.fornecedor"),
    'PESSOA': ("DROP TABLE IF EXISTS aaaca.pessoa"),
}

# Valores para teste de update
update = {'PESSOA': (
    """UPDATE aaaca.pessoa
        SET Nome = 'Novo Nome',
        Telefone = '(12)34567-8900',
        Email = 'novoemail@example.com',
        Aluno = 1,
        Aniversario = '01-01-2000',
        Sexo = 'M'
        WHERE CPF = '125.456.789-01'"""),

'ASSOCIACAO': (
    """UPDATE aaaca.associacao
        SET Tipo = 'Novo Tipo'
        WHERE ID_Associacao = 1"""),

'SOCIO_ASSOCIADO': (
    """UPDATE aaaca.socio_associado
        SET Status = 0,
        Data_Filiacao = CURRENT_TIMESTAMP,
        fk_Associacao_ID_Associacao = 1,
        fk_Pessoa_CPF = '555.666.767-01'
        WHERE ID_Socio = 1"""),

'MODALIDADE': (
    """UPDATE aaaca.modalidade
        SET Nome = 'Nova Modalidade'
        WHERE ID_Modalidade = 1"""),

'PRODUTO': (
    """UPDATE aaaca.produto
        SET Descricao = 'Nova Descrição',
        Quantidade = 10,
        Valor = 99.99
        WHERE ID_Produto = 1"""),

'FORNECEDOR': (
    """UPDATE aaaca.fornecedor
        SET Descricao = 'Nova Descrição',
        Contato = 'Novo Contato',
        Nome = 'Novo Nome'
        WHERE ID_Fornecedor = 1"""),

'SETOR': (
    """UPDATE aaaca.setor
        SET Nome = 'Novo Setor'
        WHERE ID_Setor = 1"""),

'CARGO': (
    """UPDATE aaaca.cargo
        SET Nome = 'Novo Cargo'
        WHERE ID_Cargo = 1"""),

'MATERIAL_ESPORTIVO': (
    """UPDATE aaaca.material_esportivo
        SET Quantidade = 20,
        Descricao = 'Nova Descrição',
        Nome = 'Novo Nome'
        WHERE ID_Material = 1"""),


}

# Valores para teste de delete
delete = {'PESSOA': (
    """DELETE FROM aaaca.pessoa
        WHERE CPF = '123.456.789-01'"""),
'SETOR': (
    """DELETE FROM aaaca.setor
        WHERE ID_Setor = 1"""),

'VENDA': (
    """DELETE FROM aaaca.venda
        WHERE ID_Venda = 1"""),

'COMPRA': (
    """DELETE FROM aaaca.compra
        WHERE ID_Compra = 1"""),

'GESTAO_PERTENCE': (
    """DELETE FROM aaaca.gestao_pertence
        WHERE ID_Gestao = 1"""),

'ATLETA': (
    """DELETE FROM aaaca.atleta
        WHERE fk_Modalidade_ID_Modalidade = 1
        AND fk_Socio_Associado_ID_Socio = 1"""),

'MODALIDADE_MATERIAL': (
    """DELETE FROM aaaca.modalidade_material
        WHERE fk_Material_Esporivo_ID_Material = 1
        AND fk_Modalidade_ID_Modalidade = 1"""),

'GESTAO_REALIZA_VENDA': (
    """DELETE FROM aaaca.gestao_realiza_venda
        WHERE fk_Venda_ID_Venda = 1
        AND fk_Gestao_Pertence_ID_Gestao = 1"""),

'VENDA_PRODUTO': (
    """DELETE FROM aaaca.venda_produto
        WHERE fk_Produto_ID_Produto = 1
        AND fk_Venda_ID_Venda = 1"""),

'GESTAO_EFETUA_COMPRA': (
    """DELETE FROM aaaca.gestao_efetua_compra
        WHERE fk_Compra_ID_Compra = 1
        AND fk_Gestao_Pertence_ID_Gestao = 1"""),

'COMPRA_PRODUTO': (
    """DELETE FROM aaaca.compra_produto
        WHERE fk_Produto_ID_Produto = 1
        AND fk_Compra_ID_Compra = 1""")

}


# Funções
def connect_aaaca():
    cnx = mysql.connector.connect(host='localhost', user='root', password='@Augusto0907')
    if cnx.is_connected():
        cursor = cnx.cursor()
        create_schema(cnx)
        db_info = cnx.get_server_info()
        print("Conectado ao servidor MySQL versão", db_info)
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados", linha)
        #print("Conectado ao banco de dados 'aaaca'")
        cursor.close()
    return cnx


def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Deletando {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    cursor.execute("DROP DATABASE `aaaca`;")
    connect.commit()
    cursor.close()

def create_schema(connect):
    cursor = connect.cursor()
    cursor.execute("CREATE SCHEMA IF NOT EXISTS `aaaca` DEFAULT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' ;")
    cursor.execute("USE `aaaca`;")
    connect.commit()
    cursor.close()
    print("\n---CREATE SCHEMA---")
    print("Schema 'aaaca' criado com sucesso.\n")

    

def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        select = "select * from " + name
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()


def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuido: ")
        codigo_f = input("Digite a variavel primaria: ")
        codigo = input("Digite o codigo numerico: ")
        query = ['UPDATE ', name, ' SET ', atributo, ' = ', valor, ' WHERE ', codigo_f, '= ', codigo]
        sql = ''.join(query)
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()


def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def update_test(connect):
    print("\n---UPDATE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
            cursor.execute(update_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def delete_test(connect):
    print("\n---DELETE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print("Teste de atualização de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def consulta1(connect):
    select_query = """
    SELECT
        p.id_produto,
        p.descricao AS produto,
        COALESCE(SUM(vp.valor), 0) - COALESCE(SUM(cp.valor), 0) AS fluxo_caixa
    FROM
        produto p
    LEFT JOIN
        venda_produto vp ON p.id_produto = vp.fk_produto_id_produto
    LEFT JOIN
        compra_produto cp ON p.id_produto = cp.fk_produto_id_produto
    GROUP BY
        p.id_produto, p.descricao; 
    """

    print("\nApresenta o Fluxo de Caixa de cada produto vendido pela Atlética ")

    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

    produtos = [x[1] for x in myresult]
    fluxo_caixa = [float(x[2]) for x in myresult]
    
    figsize = (12, 6)
    fig, ax= plt.subplots(figsize=figsize)
    bars = ax.bar(produtos, fluxo_caixa, color='plum', edgecolor='black', linewidth=1.0)

    ax.axhline(0, color='black', linewidth=1.2) 

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 10 if yval < 0 else yval - 10, round(yval, 2), ha='center', va='bottom' if yval < 0 else 'top', color='black', fontsize=11)

    ax.set_xlabel('Produtos')
    ax.set_ylabel('Fluxo de Caixa')
    ax.set_title('Fluxo de Caixa de Produtos')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def consulta2(connect):
    select_query = """
    SELECT 
        m.Nome AS Modalidade,
        COUNT(a.fk_Socio_Associado_ID_Socio) AS Total_Atletas,
        AVG(YEAR(curdate()) - YEAR(p.Aniversario)) AS Media_Idade
    FROM
        modalidade m
    LEFT JOIN
        atleta a ON m.ID_Modalidade = a.fk_Modalidade_ID_Modalidade
    LEFT JOIN
        socio_associado sa ON a.fk_Socio_Associado_ID_Socio = sa.ID_Socio
    LEFT JOIN
        pessoa p ON sa.fk_Pessoa_CPF = p.CPF
    GROUP BY
        m.Nome;
    """
    
    print("\nEsta consulta apresenta o número total de atletas por modalidade e a média de idade desses atletas.")
    
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()

    for x in myresult:
        print(x)

    modalidades = [x[0] for x in myresult]
    total_atletas = [int(x[1]) for x in myresult]
    media_idade = [float(x[2]) for x in myresult]

    figsize = (12, 6)
    fig, ax1 = plt.subplots(figsize=figsize)

    ax1.set_xlabel('Modalidades',fontsize=12)
    ax1.set_ylabel('Total de Atletas', fontsize=12)
    bars = ax1.bar(modalidades, total_atletas, color='plum', edgecolor='black', linewidth=1.2)
    ax1.tick_params(axis='y', labelcolor='plum')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Média de Idade', fontsize=12)
    line = ax2.plot(modalidades, media_idade, color='red', marker='o', label='Média de Idade')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.subplots_adjust(top=0.9)

    plt.xticks(rotation=45, ha='right')
    plt.title('Número Total de Atletas e Média de Idade por Modalidade', pad=0)
    plt.show()


def consulta3(connect):
    select_query = """
    SELECT
        p.Descricao AS Produto,
        f.Nome AS Fornecedor,
        SUM(vp.Quantidade) AS Quantidade_Vendida,
        SUM(vp.Valor) AS Lucro_Total,
        SUM(cp.Quantidade) AS Quantidade_Comprada,
	    SUM(cp.Valor) AS Valor_Pago,
        SUM(vp.Valor)  - SUM(cp.Valor) AS Lucro_Liquido 
    FROM
     aaaca.produto p
    JOIN
        aaaca.venda_produto vp ON p.ID_Produto = vp.fk_Produto_ID_Produto
    JOIN
        aaaca.venda v ON vp.fk_Venda_ID_Venda = v.ID_Venda
    LEFT JOIN
        aaaca.compra_produto cp ON p.ID_Produto = cp.fk_Produto_ID_Produto
    LEFT JOIN
        aaaca.compra c ON cp.fk_Compra_ID_Compra = c.ID_Compra
    LEFT JOIN
        aaaca.fornecedor f ON c.fk_Fornecedor_ID_Fornecedor = f.ID_Fornecedor
    GROUP BY
        p.Descricao, f.Nome;
 """
    print("\n Consulta mostra o Produto, Fornecedor, qtde. vendida, lucro, qtde. comprada. custo e lucro liquido")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()

    for x in myresult:
        print(x)
    
    produtos_fornecedores = [f"{x[0]} - {x[1]}" for x in myresult]
    quantidades_vendidas = [int(x[2]) for x in myresult]
    quantidades_compradas = [int(x[4]) for x in myresult]
    lucro_liquido = [float(x[6]) for x in myresult]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    bar_width = 0.35
    index = np.arange(len(produtos_fornecedores))
    bar1 = ax1.bar(index, quantidades_vendidas, bar_width, label='Qtde. Vendida', color='plum')
    bar2 = ax1.bar(index + bar_width, quantidades_compradas, bar_width, label='Qtde. Comprada', color='pink')

    ax1.set_ylabel('Quantidades')
    ax1.set_title('Quantidades Vendidas e Compradas por Produto-Fornecedor')
    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(produtos_fornecedores, rotation=45, ha='right')
    ax1.legend(loc='upper right')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Lucro Líquido', color='red')
    line = ax2.plot(produtos_fornecedores, lucro_liquido, color='red', marker='o', label='Lucro Líquido')
    ax2.tick_params(axis='y')
    ax2.legend(loc='upper left')
    
    fig.subplots_adjust(bottom=0.5, top=0.95)
    plt.show()


def consulta_extra(connect):
    select_query = """
    SELECT
        pa.nome AS associado,
        SUM(vp.valor) AS valor_total_vendas
    FROM
        venda_produto vp
    JOIN  
        venda v ON vp.fk_venda_id_venda = v.id_venda
    JOIN  
        gestao_realiza_venda grv ON v.id_venda = grv.fk_venda_id_venda
    JOIN 
        gestao_pertence gp ON grv.fk_gestao_pertence_id_gestao = gp.id_gestao
    JOIN 
        socio_associado sa ON gp.fk_socio_associado_id_socio = sa.id_socio
    JOIN 
        pessoa pa ON sa.fk_pessoa_cpf = pa.cpf
    GROUP BY
        pa.nome;
"""
    print("\nCalcular o valor total de vendas realizado por cada membro da gestao.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()

    for x in myresult:
        print(x)
    
    associados = [x[0] for x in myresult]
    valores_vendas = [float(x[1]) for x in myresult]

    fig, ax = plt.subplots(figsize=(10, 6))
    index = np.arange(len(associados))
    bars = ax.bar(index, valores_vendas, color='plum')

    ax.set_ylabel('Valor Total de Vendas')
    ax.set_title('Valor Total de Vendas por Membro da Gestão')
    ax.set_xticks(index)
    ax.set_xticklabels(associados, rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

    fig.subplots_adjust(bottom=0.17, top=0.95)
    plt.show()
        
def consulta_extra2(connect):
    select_query = """
    SELECT
    a.`Tipo` AS TipoAssociacao,
    SUM(CASE WHEN sa.`Status` = 1 AND p.`Aluno` = 1 THEN 1 ELSE 0 END) AS Ativos_Alunos,
    SUM(CASE WHEN sa.`Status` = 0 AND p.`Aluno` = 1 THEN 1 ELSE 0 END) AS Inativos_Alunos,
    SUM(CASE WHEN sa.`Status` = 1 AND p.`Aluno` = 0 THEN 1 ELSE 0 END) AS Ativos_NaoAlunos,
    SUM(CASE WHEN sa.`Status` = 0 AND p.`Aluno` = 0 THEN 1 ELSE 0 END) AS Inativos_NaoAlunos
    FROM
        `aaaca`.`associacao` a
    JOIN
        `aaaca`.`socio_associado` sa ON a.`ID_Associacao` = sa.`fk_Associacao_ID_Associacao`
    JOIN
        `aaaca`.`pessoa` p ON sa.`fk_Pessoa_CPF` = p.`CPF`
    GROUP BY
        a.`Tipo`;
"""
    print("\nNúmero de sócios ativos e inativos para cada tipo de associação")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()

    for x in myresult:
        print(x)
    
    tipos_associacao = [x[0] for x in myresult]
    ativos_alunos = [int(x[1]) for x in myresult]
    inativos_alunos = [int(x[2]) for x in myresult]
    ativos_nao_alunos = [int(x[3]) for x in myresult]
    inativos_nao_alunos = [int(x[4]) for x in myresult]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    index = np.arange(len(tipos_associacao))
    width = 0.2
    
    bars1 = ax.bar(index - 1.5*width, ativos_alunos, width, label='Ativos Alunos', color='pink')
    bars2 = ax.bar(index -0.5*width, inativos_alunos, width, label='Inativos Alunos', color='plum')
    bars3 = ax.bar(index + 0.5*width, ativos_nao_alunos, width, label='Ativos Não Alunos', color='darkviolet')
    bars4 = ax.bar(index + 1.5*width, inativos_nao_alunos, width, label='Inativos Não Alunos', color='purple')
    
    ax.set_ylabel('Número de Sócios')
    ax.set_title('Número de Sócios Ativos e Inativos para Cada Tipo de Associação')
    ax.set_xticks(index + width / 2)
    ax.set_xticklabels(tipos_associacao)
    ax.legend()
    
    plt.show()


def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão ao MySQL foi encerrada")


def crud_aaaca(connect):
    create_schema(con)
    drop_all_tables(connect)
    create_schema(connect)
    
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)
    consulta_extra2(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)
    consulta_extra2(connect)


# Main
try:
    # Estabelece Conexão com o DB
    con = connect_aaaca()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD AAACA
        2.  TEST - Create all tables
        3.  TEST - Insert all values
        4.  TEST - Update
        5.  TEST - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  CONSULTA EXTRA
        10. CONSULTA EXTRA 2
        11. Show Table
        12. Update Value
        13. CLEAR ALL AAACA
        0.  Disconnect DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 13:
            print("Erro tente novamente")
            choice = int(input())

        if choice == 0:
            if con.is_connected():
                exit_db(con)
                print("Muito obrigado.")
                break
            else:
                break

        if choice == 1:
            crud_aaaca(con)

        if choice == 2:
            create_schema(con)
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:
            consulta1(con)

        if choice == 7:
            consulta2(con)

        if choice == 8:
            consulta3(con)

        if choice == 9:
            consulta_extra(con)
        
        if choice == 10:
            consulta_extra2(con)
            
        if choice == 11:
            show_table(con)

        if choice == 12:
            update_value(con)

        if choice == 13:
            drop_all_tables(con)

except mysql.connector.Error as err:
    print("Erro na conexão com o sqlite", err.msg)



