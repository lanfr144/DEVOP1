-- ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: xau
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CodeBcee`
--

DROP TABLE IF EXISTS `CodeBcee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CodeBcee` (
  `codeBcee` varchar(7) NOT NULL,
  PRIMARY KEY (`codeBcee`),
  CONSTRAINT `CodeBcee_chk_1` CHECK (regexp_like(`codeBcee`,_utf8mb4'^[0-9]{7}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CodeBcee`
--

/*!40000 ALTER TABLE `CodeBcee` DISABLE KEYS */;
/*!40000 ALTER TABLE `CodeBcee` ENABLE KEYS */;

--
-- Table structure for table `Form`
--

DROP TABLE IF EXISTS `Form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Form` (
  `form` varchar(20) NOT NULL,
  PRIMARY KEY (`form`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Form`
--

/*!40000 ALTER TABLE `Form` DISABLE KEYS */;
/*!40000 ALTER TABLE `Form` ENABLE KEYS */;

--
-- Table structure for table `Image`
--

DROP TABLE IF EXISTS `Image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Image` (
  `image` varchar(200) NOT NULL,
  PRIMARY KEY (`image`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Image`
--

/*!40000 ALTER TABLE `Image` DISABLE KEYS */;
/*!40000 ALTER TABLE `Image` ENABLE KEYS */;

--
-- Table structure for table `Name`
--

DROP TABLE IF EXISTS `Name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Name` (
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Name`
--

/*!40000 ALTER TABLE `Name` DISABLE KEYS */;
/*!40000 ALTER TABLE `Name` ENABLE KEYS */;

--
-- Table structure for table `Purity`
--

DROP TABLE IF EXISTS `Purity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Purity` (
  `purity` varchar(20) NOT NULL,
  PRIMARY KEY (`purity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purity`
--

/*!40000 ALTER TABLE `Purity` DISABLE KEYS */;
/*!40000 ALTER TABLE `Purity` ENABLE KEYS */;

--
-- Table structure for table `Rate`
--

DROP TABLE IF EXISTS `Rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Rate` (
  `pkfk_uid` int NOT NULL,
  `pk_dt` date NOT NULL,
  `priceBceeBuy` decimal(15,2) NOT NULL,
  `priceBceeSell` decimal(15,2) NOT NULL,
  PRIMARY KEY (`pk_dt`,`pkfk_uid`),
  KEY `pkfk_uid` (`pkfk_uid`),
  CONSTRAINT `Rate_ibfk_1` FOREIGN KEY (`pkfk_uid`) REFERENCES `Uid` (`uid`),
  CONSTRAINT `Rate_ibfk_2` FOREIGN KEY (`pkfk_uid`) REFERENCES `Xau` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rate`
--

/*!40000 ALTER TABLE `Rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `Rate` ENABLE KEYS */;

--
-- Table structure for table `Uid`
--

DROP TABLE IF EXISTS `Uid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Uid` (
  `uid` int NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Uid`
--

/*!40000 ALTER TABLE `Uid` DISABLE KEYS */;
/*!40000 ALTER TABLE `Uid` ENABLE KEYS */;

--
-- Table structure for table `Weight`
--

DROP TABLE IF EXISTS `Weight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Weight` (
  `weight` decimal(7,3) NOT NULL,
  PRIMARY KEY (`weight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Weight`
--

/*!40000 ALTER TABLE `Weight` DISABLE KEYS */;
/*!40000 ALTER TABLE `Weight` ENABLE KEYS */;

--
-- Table structure for table `Xau`
--

DROP TABLE IF EXISTS `Xau`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Xau` (
  `uid` int NOT NULL,
  `codeBcee` varchar(7) NOT NULL,
  `name` varchar(50) NOT NULL,
  `form` varchar(20) NOT NULL,
  `purity` varchar(20) NOT NULL,
  `weightNet` decimal(7,3) NOT NULL,
  `weightBrut` decimal(7,3) NOT NULL,
  `image` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `codeBcee` (`codeBcee`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `image` (`image`),
  KEY `form` (`form`),
  KEY `purity` (`purity`),
  KEY `weightNet` (`weightNet`),
  KEY `weightBrut` (`weightBrut`),
  CONSTRAINT `Xau_ibfk_1` FOREIGN KEY (`name`) REFERENCES `Name` (`name`),
  CONSTRAINT `Xau_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `Uid` (`uid`),
  CONSTRAINT `Xau_ibfk_3` FOREIGN KEY (`codeBcee`) REFERENCES `CodeBcee` (`codeBcee`),
  CONSTRAINT `Xau_ibfk_4` FOREIGN KEY (`form`) REFERENCES `Form` (`form`),
  CONSTRAINT `Xau_ibfk_5` FOREIGN KEY (`purity`) REFERENCES `Purity` (`purity`),
  CONSTRAINT `Xau_ibfk_6` FOREIGN KEY (`weightNet`) REFERENCES `Weight` (`weight`),
  CONSTRAINT `Xau_ibfk_7` FOREIGN KEY (`weightBrut`) REFERENCES `Weight` (`weight`),
  CONSTRAINT `Xau_ibfk_8` FOREIGN KEY (`image`) REFERENCES `Image` (`image`),
  CONSTRAINT `chk_weightBrut_positive` CHECK ((`weightBrut` > 0)),
  CONSTRAINT `chk_weightNet_positive` CHECK ((`weightNet` > 0)),
  CONSTRAINT `CodeBcee_chk_2` CHECK (regexp_like(`codeBcee`,_utf8mb4'^[0-9]{7}$'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Xau`
--

/*!40000 ALTER TABLE `Xau` DISABLE KEYS */;
/*!40000 ALTER TABLE `Xau` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-18 13:08:26
