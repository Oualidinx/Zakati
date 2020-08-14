-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	10.3.22-MariaDB-1ubuntu1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `concerner`
--

LOCK TABLES `concerner` WRITE;
/*!40000 ALTER TABLE `concerner` DISABLE KEYS */;
/*!40000 ALTER TABLE `concerner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `critere`
--

LOCK TABLES `critere` WRITE;
/*!40000 ALTER TABLE `critere` DISABLE KEYS */;
INSERT INTO `critere` VALUES ('أجر تحت الأجر القاعدي','الاجتماعية',3),('اعاقة','الصحية',3),('بدون تأمين صحي','الاجتماعية',1),('بطال','الاجتماعية',2),('سكن هش','الاجتماعية',2),('عدم ملكية المنزل','الاجتماعية',1),('فرد غير البالغ','العائلية',1),('فرد متمدرس','العائلية',1),('كفيل متوفي','العائلية',4),('مرض مزمن','الصحية',2);
/*!40000 ALTER TABLE `critere` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `donneur`
--

LOCK TABLES `donneur` WRITE;
/*!40000 ALTER TABLE `donneur` DISABLE KEYS */;
INSERT INTO `donneur` VALUES (1,'وارم','وليد','حي 12 هكتار','035794260',5),(2,'عثامنة','زهير','دالاس حي لاقراف','0796149356',6);
/*!40000 ALTER TABLE `donneur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `fournit`
--

LOCK TABLES `fournit` WRITE;
/*!40000 ALTER TABLE `fournit` DISABLE KEYS */;
INSERT INTO `fournit` VALUES (1,1,2,30000,'2019-07-26 23:01:27');
/*!40000 ALTER TABLE `fournit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `garant`
--

LOCK TABLES `garant` WRITE;
/*!40000 ALTER TABLE `garant` DISABLE KEYS */;
INSERT INTO `garant` VALUES ('14785296',26,'وارم','جمال','2019-07-24 16:15:00','1975-07-17 00:00:00',6023,16,16,0,1,2),('33669955',84,'بلماضي','فرحات','2019-07-22 18:06:20','1940-02-15 00:00:00',1742,1.08,13,15576.9,1,1),('44116688',526,'روابح','زهير','2019-07-22 18:17:11','1978-01-15 00:00:00',126,1,12,14423.1,1,1),('84266248',89,'عبدلي','وليد','2019-07-24 16:17:35','1975-07-17 00:00:00',1456,1,1,0,1,2);
/*!40000 ALTER TABLE `garant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `mosque`
--

LOCK TABLES `mosque` WRITE;
/*!40000 ALTER TABLE `mosque` DISABLE KEYS */;
INSERT INTO `mosque` VALUES (1,'ابي بكر الصديق','وليد مهساس','حي 12 هكتار','برج بو عريريج','الجزائر','0790906125',3,"مسجد"),(2,'الامـام الحسين','فرحات عبد الحليم','حي المحطة','برج بو عريريج','الجزائر','0668465310',4,"مسجد");
/*!40000 ALTER TABLE `mosque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `participe`
--

LOCK TABLES `participe` WRITE;
/*!40000 ALTER TABLE `participe` DISABLE KEYS */;
/*!40000 ALTER TABLE `participe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `personne`
--

LOCK TABLES `personne` WRITE;
/*!40000 ALTER TABLE `personne` DISABLE KEYS */;
INSERT INTO `personne` VALUES (34,'بلماضي','أحمد','1990-03-15 00:00:00','ابن(ة)','33669955'),(35,'وارم','سليمة','1989-08-10 00:00:00','زوجة','33669955'),(36,'بلماضي','بلال','1970-05-12 00:00:00','الأب','33669955'),(37,'روابح','اسلام','2002-10-15 00:00:00','ابن(ة)','44116688'),(38,'روابح','محمد','2008-12-12 00:00:00','ابن(ة)','44116688'),(39,'فحيمة','حميدة','1982-02-17 00:00:00','زوجة','44116688'),(40,'وارم','أحمد','1996-02-15 00:00:00','ابن(ة)','14785296'),(41,'وارم','حليمة','2001-05-16 00:00:00','ابن(ة)','14785296'),(42,'وارم','حميدة','2000-12-12 00:00:00','ابن(ة)','14785296'),(43,'بلواهري','كنزة','1975-12-15 00:00:00','زوجة','14785296'),(44,'عثامنية','لاميس','1996-03-06 00:00:00','زوجة','84266248');
/*!40000 ALTER TABLE `personne` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `projet`
--

LOCK TABLES `projet` WRITE;
/*!40000 ALTER TABLE `projet` DISABLE KEYS */;
/*!40000 ALTER TABLE `projet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `situation_garant`
--

LOCK TABLES `situation_garant` WRITE;
/*!40000 ALTER TABLE `situation_garant` DISABLE KEYS */;
INSERT INTO `situation_garant` VALUES ('14785296','أجر تحت الأجر القاعدي'),('14785296','سكن هش'),('14785296','مرض مزمن'),('33669955','أجر تحت الأجر القاعدي'),('33669955','اعاقة'),('33669955','سكن هش'),('44116688','بطال'),('44116688','سكن هش'),('44116688','مرض مزمن');
/*!40000 ALTER TABLE `situation_garant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `situation_personne`
--

LOCK TABLES `situation_personne` WRITE;
/*!40000 ALTER TABLE `situation_personne` DISABLE KEYS */;
INSERT INTO `situation_personne` VALUES (34,'فرد متمدرس'),(35,'مرض مزمن'),(36,'مرض مزمن'),(37,'فرد متمدرس'),(37,'مرض مزمن'),(38,'فرد متمدرس'),(39,'مرض مزمن'),(40,'فرد متمدرس'),(40,'مرض مزمن'),(41,'فرد متمدرس'),(42,'فرد متمدرس'),(42,'مرض مزمن'),(43,'مرض مزمن'),(44,'فرد متمدرس');
/*!40000 ALTER TABLE `situation_personne` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'admin','$2b$12$QXluT0Qw/DQdobAdUnj.DeSRD5XjM5HHhgNYLf6.hppO7S.H.AOjK'),(3,'0673669397','$2b$12$pom2Y6pKYBN4YJy3K9Z.OO6EjdEixK4G8ory14lJ1XJsmzzgkpgH6'),(4,'0668465310','$2b$12$G19dWKCPvUAZmsBoPSPaa.t9kvxbn8cYati5qwDxoZ0Qv15avvDba'),(5,'035794260','$2b$12$q/AnoFY86MM7WBGlgvbVPuW9JdIBozbNOAA.20ohWNjlfwkezr/cu'),(6,'0796149356','$2b$12$tN/o/aFmYHrWNhJSvuwfp.fvjctIbrZdQi0nQ1el/mcDS9h4fXIYu');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-13 19:06:43
