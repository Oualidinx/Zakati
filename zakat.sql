-- MySQL dump 10.17  Distrib 10.3.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	10.3.13-MariaDB-2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `concerner`
--

DROP TABLE IF EXISTS `concerner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `concerner` (
  `garant_id` varchar(10) NOT NULL,
  `projet_id` int(11) NOT NULL,
  PRIMARY KEY (`garant_id`,`projet_id`),
  KEY `projet_id` (`projet_id`),
  CONSTRAINT `concerner_ibfk_1` FOREIGN KEY (`garant_id`) REFERENCES `garant` (`id`),
  CONSTRAINT `concerner_ibfk_2` FOREIGN KEY (`projet_id`) REFERENCES `projet` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concerner`
--

LOCK TABLES `concerner` WRITE;
/*!40000 ALTER TABLE `concerner` DISABLE KEYS */;
/*!40000 ALTER TABLE `concerner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `critere`
--

DROP TABLE IF EXISTS `critere`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `critere` (
  `id` varchar(40) NOT NULL,
  `categorie` varchar(50) DEFAULT NULL,
  `poids` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `critere`
--

LOCK TABLES `critere` WRITE;
/*!40000 ALTER TABLE `critere` DISABLE KEYS */;
/*!40000 ALTER TABLE `critere` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donneur`
--

DROP TABLE IF EXISTS `donneur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `donneur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `adresse` varchar(100) NOT NULL,
  `num_tele` varchar(10) NOT NULL,
  `user_account` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_account` (`user_account`),
  CONSTRAINT `donneur_ibfk_1` FOREIGN KEY (`user_account`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donneur`
--

LOCK TABLES `donneur` WRITE;
/*!40000 ALTER TABLE `donneur` DISABLE KEYS */;
/*!40000 ALTER TABLE `donneur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fournit`
--

DROP TABLE IF EXISTS `fournit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fournit` (
  `mosque_id` int(11) NOT NULL,
  `donneur_id` int(11) NOT NULL,
  `montant` float DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`mosque_id`,`donneur_id`),
  KEY `donneur_id` (`donneur_id`),
  CONSTRAINT `fournit_ibfk_1` FOREIGN KEY (`mosque_id`) REFERENCES `mosque` (`id`),
  CONSTRAINT `fournit_ibfk_2` FOREIGN KEY (`donneur_id`) REFERENCES `donneur` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fournit`
--

LOCK TABLES `fournit` WRITE;
/*!40000 ALTER TABLE `fournit` DISABLE KEYS */;
/*!40000 ALTER TABLE `fournit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garant`
--

DROP TABLE IF EXISTS `garant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `garant` (
  `id` varchar(10) NOT NULL,
  `cle_CCP` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `date_inscrit` datetime NOT NULL,
  `date_nais` datetime NOT NULL,
  `num_extrait_nais` int(11) NOT NULL,
  `Solde_finale` float DEFAULT NULL,
  `Solde_points` int(11) DEFAULT NULL,
  `Solde_part_financiere` float DEFAULT NULL,
  `actif` int(11) DEFAULT NULL,
  `mosque_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mosque_id` (`mosque_id`),
  CONSTRAINT `garant_ibfk_1` FOREIGN KEY (`mosque_id`) REFERENCES `mosque` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garant`
--

LOCK TABLES `garant` WRITE;
/*!40000 ALTER TABLE `garant` DISABLE KEYS */;
/*!40000 ALTER TABLE `garant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mosque`
--

DROP TABLE IF EXISTS `mosque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mosque` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `imam` varchar(50) NOT NULL,
  `addresse` varchar(100) NOT NULL,
  `state` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `num_tele` varchar(10) NOT NULL,
  `user_account` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_account` (`user_account`),
  CONSTRAINT `mosque_ibfk_1` FOREIGN KEY (`user_account`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mosque`
--

LOCK TABLES `mosque` WRITE;
/*!40000 ALTER TABLE `mosque` DISABLE KEYS */;
/*!40000 ALTER TABLE `mosque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participe`
--

DROP TABLE IF EXISTS `participe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `participe` (
  `donneur_id` int(11) NOT NULL,
  `projet_id` int(11) NOT NULL,
  PRIMARY KEY (`donneur_id`,`projet_id`),
  KEY `projet_id` (`projet_id`),
  CONSTRAINT `participe_ibfk_1` FOREIGN KEY (`donneur_id`) REFERENCES `donneur` (`id`),
  CONSTRAINT `participe_ibfk_2` FOREIGN KEY (`projet_id`) REFERENCES `projet` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participe`
--

LOCK TABLES `participe` WRITE;
/*!40000 ALTER TABLE `participe` DISABLE KEYS */;
/*!40000 ALTER TABLE `participe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personne`
--

DROP TABLE IF EXISTS `personne`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `personne` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `date_naissance` datetime NOT NULL,
  `relation_ship` varchar(6) NOT NULL,
  `garant_id` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `garant_id` (`garant_id`),
  CONSTRAINT `personne_ibfk_1` FOREIGN KEY (`garant_id`) REFERENCES `garant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personne`
--

LOCK TABLES `personne` WRITE;
/*!40000 ALTER TABLE `personne` DISABLE KEYS */;
/*!40000 ALTER TABLE `personne` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projet`
--

DROP TABLE IF EXISTS `projet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `Description` text DEFAULT NULL,
  `montant_estime` float NOT NULL,
  `montant_quantise` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projet`
--

LOCK TABLES `projet` WRITE;
/*!40000 ALTER TABLE `projet` DISABLE KEYS */;
/*!40000 ALTER TABLE `projet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `situation_garant`
--

DROP TABLE IF EXISTS `situation_garant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `situation_garant` (
  `garant_id` varchar(10) NOT NULL,
  `critere_id` varchar(40) NOT NULL,
  PRIMARY KEY (`garant_id`,`critere_id`),
  KEY `critere_id` (`critere_id`),
  CONSTRAINT `situation_garant_ibfk_1` FOREIGN KEY (`garant_id`) REFERENCES `garant` (`id`),
  CONSTRAINT `situation_garant_ibfk_2` FOREIGN KEY (`critere_id`) REFERENCES `critere` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `situation_garant`
--

LOCK TABLES `situation_garant` WRITE;
/*!40000 ALTER TABLE `situation_garant` DISABLE KEYS */;
/*!40000 ALTER TABLE `situation_garant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `situation_personne`
--

DROP TABLE IF EXISTS `situation_personne`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `situation_personne` (
  `personne_id` int(11) NOT NULL,
  `critere_id` varchar(40) NOT NULL,
  PRIMARY KEY (`personne_id`,`critere_id`),
  KEY `critere_id` (`critere_id`),
  CONSTRAINT `situation_personne_ibfk_1` FOREIGN KEY (`personne_id`) REFERENCES `personne` (`id`),
  CONSTRAINT `situation_personne_ibfk_2` FOREIGN KEY (`critere_id`) REFERENCES `critere` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `situation_personne`
--

LOCK TABLES `situation_personne` WRITE;
/*!40000 ALTER TABLE `situation_personne` DISABLE KEYS */;
/*!40000 ALTER TABLE `situation_personne` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-20 23:08:39
