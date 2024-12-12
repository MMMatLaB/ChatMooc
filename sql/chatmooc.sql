-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: chatmooc
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `base`
--

DROP TABLE IF EXISTS `base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `base` (
  `bid` int NOT NULL,
  `rid` int NOT NULL,
  `path` varchar(128) NOT NULL,
  `updatetime` timestamp(6) NOT NULL,
  PRIMARY KEY (`bid`),
  KEY `fk_production_recource1_idx` (`rid`),
  CONSTRAINT `fk_production_recource1` FOREIGN KEY (`rid`) REFERENCES `resource` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base`
--

LOCK TABLES `base` WRITE;
/*!40000 ALTER TABLE `base` DISABLE KEYS */;
/*!40000 ALTER TABLE `base` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `question` varchar(45) NOT NULL,
  `answer` varchar(45) NOT NULL,
  `nextTime` varchar(45) NOT NULL,
  `createtime` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `status` int NOT NULL COMMENT '0 未学习 1 学习中 2等待复习',
  `fid` int NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card`
--

LOCK TABLES `card` WRITE;
/*!40000 ALTER TABLE `card` DISABLE KEYS */;
INSERT INTO `card` VALUES (1,'proident non312312','ADSADSDsmod consectetur irure','2024-05-22 18:42:45','1','text',1,1),(3,'2YRYEY','2212313','2024-05-22 19:00:03','22','text',1,1),(4,'1','1','2024-05-21 07:19:36','1','text',2,2),(5,'111','111','2024-05-22 19:00:30','111','text',1,1),(6,'occaecat','fugiat irure','2024-05-22 19:00:32','2024-05-20 22:43:50','text',1,1),(7,'occaecat','fugiat irure','2024-05-28 18:50:35','2024-05-20','text',1,1),(8,'in aliqua adipisicing qui','cillum ad id sunt Duis','2024-05-20 05:18:35','2024-05-20','text',2,40),(10,'aute pariatur veniam quis labore','anim ut','2024-05-22 19:28:48','2024-05-22','text',1,4);
/*!40000 ALTER TABLE `card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cardfolder`
--

DROP TABLE IF EXISTS `cardfolder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cardfolder` (
  `fid` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(45) NOT NULL,
  `createtime` varchar(45) NOT NULL,
  `sid` int DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cardfolder`
--

LOCK TABLES `cardfolder` WRITE;
/*!40000 ALTER TABLE `cardfolder` DISABLE KEYS */;
INSERT INTO `cardfolder` VALUES (1,'NoneY','2023-05-22',1),(4,'ASA','2024-05-22',1);
/*!40000 ALTER TABLE `cardfolder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gc`
--

DROP TABLE IF EXISTS `gc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gc` (
  `idgc` int NOT NULL AUTO_INCREMENT,
  `rid` int NOT NULL,
  `summary` varchar(512) DEFAULT NULL,
  `keyword` varchar(128) DEFAULT NULL,
  `abstract` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`idgc`),
  KEY `fk_gc_recource1_idx` (`rid`),
  CONSTRAINT `fk_gc_recource1` FOREIGN KEY (`rid`) REFERENCES `resource` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gc`
--

LOCK TABLES `gc` WRITE;
/*!40000 ALTER TABLE `gc` DISABLE KEYS */;
/*!40000 ALTER TABLE `gc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `hid` int NOT NULL AUTO_INCREMENT,
  `some` varchar(45) DEFAULT NULL,
  `section_sid` int NOT NULL,
  PRIMARY KEY (`hid`),
  KEY `fk_history_section1_idx` (`section_sid`),
  CONSTRAINT `fk_history_section1` FOREIGN KEY (`section_sid`) REFERENCES `section` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `updatetime` varchar(45) NOT NULL,
  `ownerid` int NOT NULL,
  `url` varchar(128) NOT NULL,
  `status` int NOT NULL COMMENT '0 未解析，1已经解析',
  `posterurl` varchar(128) NOT NULL,
  `text` text,
  PRIMARY KEY (`rid`),
  KEY `fk_recource_user_idx` (`ownerid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
INSERT INTO `resource` VALUES (1,'1','1','1',1,'1',1,'1','1'),(2,'2','2','1',1,'2',22,'2','1');
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `section` (
  `sid` int NOT NULL AUTO_INCREMENT,
  `ownerid` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `createtime` varchar(45) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `section`
--

LOCK TABLES `section` WRITE;
/*!40000 ALTER TABLE `section` DISABLE KEYS */;
INSERT INTO `section` VALUES (1,1,'计算机','2024-05-19'),(2,1,'软件','2024-05-22'),(3,1,'牛马','2024-05-23');
/*!40000 ALTER TABLE `section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sectionhasresource`
--

DROP TABLE IF EXISTS `sectionhasresource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sectionhasresource` (
  `sid` int NOT NULL,
  `rid` int NOT NULL,
  `kid` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`kid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sectionhasresource`
--

LOCK TABLES `sectionhasresource` WRITE;
/*!40000 ALTER TABLE `sectionhasresource` DISABLE KEYS */;
INSERT INTO `sectionhasresource` VALUES (19,0,2),(19,2,4),(20,0,5),(20,1,6),(20,2,7),(21,0,8),(21,1,9),(21,2,10);
/*!40000 ALTER TABLE `sectionhasresource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `uname` varchar(45) NOT NULL,
  `upass` varchar(128) NOT NULL,
  `avatar` varchar(256) NOT NULL COMMENT '''url of avatar''',
  `createtime` varchar(45) NOT NULL,
  `status` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'1','1','1','1',1),(2,'2','2','23','2',0);
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

-- Dump completed on 2024-05-22 17:38:02
