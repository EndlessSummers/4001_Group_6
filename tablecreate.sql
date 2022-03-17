-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`User_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User_info` (
  `User_ID` INT NOT NULL AUTO_INCREMENT,
  `Password` VARCHAR(45) NOT NULL,
  `User_Email` VARCHAR(45) NOT NULL,
  `User_Name` VARCHAR(45) NULL,
  PRIMARY KEY (`User_ID`),
  UNIQUE INDEX `User_ID_UNIQUE` (`User_ID` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Activities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Activities` (
  `Activities_id` INT NOT NULL,
  `Activity_desc` VARCHAR(45) NULL,
  `Activity_timeLength` INT NULL,
  PRIMARY KEY (`Activities_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Rankings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Rankings` (
  `Activities_Activities_id` INT NOT NULL,
  `User_info_User_ID` INT NOT NULL,
  `Ranking` INT NULL,
  `Created_At` DATETIME NULL,
  PRIMARY KEY (`Activities_Activities_id`, `User_info_User_ID`),
  INDEX `fk_Rankings_User_info1_idx` (`User_info_User_ID` ASC),
  CONSTRAINT `fk_Rankings_Activities1`
    FOREIGN KEY (`Activities_Activities_id`)
    REFERENCES `mydb`.`Activities` (`Activities_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Rankings_User_info1`
    FOREIGN KEY (`User_info_User_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Group` (
  `Group_id` INT NOT NULL,
  `Group_name` VARCHAR(45) NULL,
  PRIMARY KEY (`Group_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`message` (
  `User_info_Sender_ID` INT NOT NULL,
  `User_info_Receiver_ID1` INT NOT NULL,
  `Created_At` DATETIME NULL,
  `content` VARCHAR(1000) NULL,
  PRIMARY KEY (`User_info_Sender_ID`, `User_info_Receiver_ID1`),
  INDEX `fk_table4_User_info2_idx` (`User_info_Receiver_ID1` ASC),
  CONSTRAINT `fk_table4_User_info1`
    FOREIGN KEY (`User_info_Sender_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table4_User_info2`
    FOREIGN KEY (`User_info_Receiver_ID1`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Note`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Note` (
  `Note_id` INT NOT NULL,
  `User_info_User_ID` INT NOT NULL,
  `Created_At` DATETIME NULL,
  `content` VARCHAR(1000) NULL,
  PRIMARY KEY (`Note_id`),
  CONSTRAINT `fk_Note_User_info1`
    FOREIGN KEY (`User_info_User_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User_History`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User_History` (
  `User_info_User_ID` INT NOT NULL,
  `Activities_Activities_id` INT NOT NULL,
  `Created_at` DATETIME NULL,
  PRIMARY KEY (`User_info_User_ID`, `Activities_Activities_id`),
  INDEX `fk_User_History_User_info1_idx` (`User_info_User_ID` ASC),
  INDEX `fk_User_History_Activities1_idx` (`Activities_Activities_id` ASC),
  CONSTRAINT `fk_User_History_User_info1`
    FOREIGN KEY (`User_info_User_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_History_Activities1`
    FOREIGN KEY (`Activities_Activities_id`)
    REFERENCES `mydb`.`Activities` (`Activities_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User_Preference`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User_Preference` (
  `User_info_User_ID` INT NOT NULL,
  `Activities_Activities_id` INT NOT NULL,
  INDEX `fk_User_Preference_User_info_idx` (`User_info_User_ID` ASC),
  PRIMARY KEY (`User_info_User_ID`, `Activities_Activities_id`),
  INDEX `fk_User_Preference_Activities1_idx` (`Activities_Activities_id` ASC),
  CONSTRAINT `fk_User_Preference_User_info`
    FOREIGN KEY (`User_info_User_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_Preference_Activities1`
    FOREIGN KEY (`Activities_Activities_id`)
    REFERENCES `mydb`.`Activities` (`Activities_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`User_info_has_Group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`User_info_has_Group` (
  `User_info_User_ID` INT NOT NULL,
  `Group_Group_id` INT NOT NULL,
  PRIMARY KEY (`User_info_User_ID`, `Group_Group_id`),
  INDEX `fk_User_info_has_Group_Group1_idx` (`Group_Group_id` ASC),
  INDEX `fk_User_info_has_Group_User_info1_idx` (`User_info_User_ID` ASC),
  CONSTRAINT `fk_User_info_has_Group_User_info1`
    FOREIGN KEY (`User_info_User_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User_info_has_Group_Group1`
    FOREIGN KEY (`Group_Group_id`)
    REFERENCES `mydb`.`Group` (`Group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Comment` (
  `User_info_Commentor_ID` INT NOT NULL,
  `Note_Note_id` INT NOT NULL,
  `CreatedAt` DATETIME NULL,
  PRIMARY KEY (`User_info_Commentor_ID`, `Note_Note_id`),
  INDEX `fk_User_info_has_Note_User_info1_idx` (`User_info_Commentor_ID` ASC),
  INDEX `fk_Comment_Note1_idx` (`Note_Note_id` ASC),
  CONSTRAINT `fk_User_info_has_Note_User_info1`
    FOREIGN KEY (`User_info_Commentor_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comment_Note1`
    FOREIGN KEY (`Note_Note_id`)
    REFERENCES `mydb`.`Note` (`Note_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Group_Message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Group_Message` (
  `Group_Group_id` INT NOT NULL,
  `User_info_User_ID` INT NOT NULL,
  `Content` VARCHAR(1000) NULL,
  `Created_At` DATETIME NULL,
  PRIMARY KEY (`Group_Group_id`, `User_info_User_ID`),
  INDEX `fk_Group_Message_User_info1_idx` (`User_info_User_ID` ASC),
  CONSTRAINT `fk_Group_Message_Group1`
    FOREIGN KEY (`Group_Group_id`)
    REFERENCES `mydb`.`Group` (`Group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Group_Message_User_info1`
    FOREIGN KEY (`User_info_User_ID`)
    REFERENCES `mydb`.`User_info` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

