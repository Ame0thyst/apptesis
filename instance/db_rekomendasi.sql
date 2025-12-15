CREATE DATABASE  IF NOT EXISTS `db_rekomendasi` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_rekomendasi`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: db_rekomendasi
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `recommendations`
--

DROP TABLE IF EXISTS `recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_student` int DEFAULT NULL,
  `paket_prediksi` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `probabilitas` float DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_student` (`id_student`),
  CONSTRAINT `recommendations_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendations`
--

LOCK TABLES `recommendations` WRITE;
/*!40000 ALTER TABLE `recommendations` DISABLE KEYS */;
INSERT INTO `recommendations` VALUES (1,1,'Paket 1',NULL,'2025-09-30 00:51:41'),(2,2,'1',NULL,'2025-09-30 20:47:39'),(3,3,'Paket 3',NULL,'2025-10-07 07:26:36'),(4,6,'1',NULL,'2025-10-07 12:42:05'),(5,13,'1',NULL,'2025-11-18 10:19:29'),(6,5,'1',NULL,'2025-11-28 09:47:15'),(7,12,'1',NULL,'2025-12-10 16:52:33'),(8,11,'Paket 1',NULL,'2025-12-11 20:04:18'),(9,20,'1',NULL,'2025-12-12 21:17:56'),(10,15,'1',NULL,'2025-12-12 21:39:20'),(11,17,'Paket 1',NULL,'2025-12-13 12:08:55'),(12,16,'Paket 1',NULL,'2025-12-13 12:17:51'),(13,14,'Paket 1',NULL,'2025-12-13 12:41:27');
/*!40000 ALTER TABLE `recommendations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_scores`
--

DROP TABLE IF EXISTS `report_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_scores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_student` int DEFAULT NULL,
  `biologi` float DEFAULT NULL,
  `fisika` float DEFAULT NULL,
  `kimia` float DEFAULT NULL,
  `matematika` float DEFAULT NULL,
  `ekonomi` float DEFAULT NULL,
  `sosiologi` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_student` (`id_student`),
  CONSTRAINT `report_scores_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_scores`
--

LOCK TABLES `report_scores` WRITE;
/*!40000 ALTER TABLE `report_scores` DISABLE KEYS */;
INSERT INTO `report_scores` VALUES (1,1,90,88,98,93,75,99),(2,2,80,85,78,79,81,85),(3,3,78,89,88,76,79,82),(4,6,85,87,75,89,79,88),(5,13,82,89,80,91,79,81),(6,5,82,81,85,86,87,81),(7,12,80,87,86,88,91,90),(8,11,95,81,78,98,88,85),(9,19,80,81,82,83,86,87),(10,20,98,98,97,85,80,84),(11,15,88,85,92,95,90,78),(12,17,98,97,78,91,87,85),(13,16,89,97,82,78,96,88),(14,14,88,84,85,69,87,78);
/*!40000 ALTER TABLE `report_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riasec_answers`
--

DROP TABLE IF EXISTS `riasec_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `riasec_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_student` int DEFAULT NULL,
  `id_question` int DEFAULT NULL,
  `skor` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_student` (`id_student`),
  KEY `id_question` (`id_question`),
  CONSTRAINT `riasec_answers_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  CONSTRAINT `riasec_answers_ibfk_2` FOREIGN KEY (`id_question`) REFERENCES `riasec_questions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=589 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riasec_answers`
--

LOCK TABLES `riasec_answers` WRITE;
/*!40000 ALTER TABLE `riasec_answers` DISABLE KEYS */;
INSERT INTO `riasec_answers` VALUES (1,1,1,0),(2,1,2,0),(3,1,3,1),(4,1,4,0),(5,1,5,1),(6,1,6,0),(7,1,7,1),(8,1,8,0),(9,1,9,0),(10,1,10,0),(11,1,11,1),(12,1,12,0),(13,1,13,1),(14,1,14,0),(15,1,15,0),(16,1,16,1),(17,1,17,0),(18,1,18,1),(19,1,19,0),(20,1,20,0),(21,1,21,1),(22,1,22,0),(23,1,23,1),(24,1,24,0),(25,1,25,0),(26,1,26,0),(27,1,27,0),(28,1,28,1),(29,1,29,0),(30,1,30,0),(31,1,31,1),(32,1,32,0),(33,1,33,0),(34,1,34,1),(35,1,35,0),(36,1,36,1),(37,1,37,0),(38,1,38,1),(39,1,39,1),(40,1,40,0),(41,1,41,0),(42,1,42,1),(43,2,1,1),(44,2,2,0),(45,2,3,0),(46,2,4,0),(47,2,5,1),(48,2,6,1),(49,2,7,0),(50,2,8,1),(51,2,9,1),(52,2,10,0),(53,2,11,1),(54,2,12,1),(55,2,13,0),(56,2,14,0),(57,2,15,1),(58,2,16,1),(59,2,17,1),(60,2,18,1),(61,2,19,0),(62,2,20,1),(63,2,21,1),(64,2,22,1),(65,2,23,0),(66,2,24,0),(67,2,25,1),(68,2,26,1),(69,2,27,1),(70,2,28,0),(71,2,29,1),(72,2,30,1),(73,2,31,0),(74,2,32,0),(75,2,33,1),(76,2,34,1),(77,2,35,0),(78,2,36,1),(79,2,37,1),(80,2,38,0),(81,2,39,1),(82,2,40,1),(83,2,41,1),(84,2,42,0),(85,3,1,1),(86,3,2,1),(87,3,3,0),(88,3,4,1),(89,3,5,1),(90,3,6,1),(91,3,7,1),(92,3,8,1),(93,3,9,1),(94,3,10,1),(95,3,11,0),(96,3,12,0),(97,3,13,0),(98,3,14,1),(99,3,15,0),(100,3,16,1),(101,3,17,1),(102,3,18,1),(103,3,19,1),(104,3,20,1),(105,3,21,0),(106,3,22,1),(107,3,23,1),(108,3,24,0),(109,3,25,0),(110,3,26,1),(111,3,27,0),(112,3,28,0),(113,3,29,0),(114,3,30,1),(115,3,31,1),(116,3,32,0),(117,3,33,0),(118,3,34,0),(119,3,35,0),(120,3,36,1),(121,3,37,1),(122,3,38,1),(123,3,39,0),(124,3,40,1),(125,3,41,1),(126,3,42,0),(127,6,1,1),(128,6,2,1),(129,6,3,0),(130,6,4,0),(131,6,5,1),(132,6,6,1),(133,6,7,0),(134,6,8,1),(135,6,9,0),(136,6,10,0),(137,6,11,1),(138,6,12,1),(139,6,13,1),(140,6,14,1),(141,6,15,1),(142,6,16,0),(143,6,17,1),(144,6,18,1),(145,6,19,1),(146,6,20,0),(147,6,21,0),(148,6,22,1),(149,6,23,1),(150,6,24,1),(151,6,25,0),(152,6,26,0),(153,6,27,0),(154,6,28,1),(155,6,29,1),(156,6,30,1),(157,6,31,0),(158,6,32,0),(159,6,33,0),(160,6,34,1),(161,6,35,1),(162,6,36,1),(163,6,37,1),(164,6,38,1),(165,6,39,0),(166,6,40,0),(167,6,41,0),(168,6,42,1),(169,13,1,1),(170,13,2,0),(171,13,3,0),(172,13,4,1),(173,13,5,1),(174,13,6,1),(175,13,7,1),(176,13,8,0),(177,13,9,1),(178,13,10,0),(179,13,11,0),(180,13,12,0),(181,13,13,0),(182,13,14,0),(183,13,15,0),(184,13,16,1),(185,13,17,1),(186,13,18,1),(187,13,19,1),(188,13,20,1),(189,13,21,0),(190,13,22,1),(191,13,23,1),(192,13,24,0),(193,13,25,0),(194,13,26,0),(195,13,27,0),(196,13,28,0),(197,13,29,1),(198,13,30,1),(199,13,31,1),(200,13,32,0),(201,13,33,0),(202,13,34,1),(203,13,35,1),(204,13,36,1),(205,13,37,1),(206,13,38,1),(207,13,39,1),(208,13,40,1),(209,13,41,1),(210,13,42,1),(211,5,1,1),(212,5,2,1),(213,5,3,0),(214,5,4,0),(215,5,5,0),(216,5,6,1),(217,5,7,1),(218,5,8,1),(219,5,9,0),(220,5,10,1),(221,5,11,1),(222,5,12,0),(223,5,13,0),(224,5,14,1),(225,5,15,1),(226,5,16,0),(227,5,17,0),(228,5,18,1),(229,5,19,0),(230,5,20,0),(231,5,21,1),(232,5,22,1),(233,5,23,0),(234,5,24,0),(235,5,25,0),(236,5,26,0),(237,5,27,1),(238,5,28,1),(239,5,29,1),(240,5,30,0),(241,5,31,1),(242,5,32,1),(243,5,33,1),(244,5,34,0),(245,5,35,0),(246,5,36,1),(247,5,37,0),(248,5,38,0),(249,5,39,0),(250,5,40,1),(251,5,41,1),(252,5,42,1),(253,12,1,1),(254,12,2,1),(255,12,3,1),(256,12,4,1),(257,12,5,1),(258,12,6,1),(259,12,7,1),(260,12,8,1),(261,12,9,1),(262,12,10,1),(263,12,11,1),(264,12,12,1),(265,12,13,1),(266,12,14,1),(267,12,15,1),(268,12,16,1),(269,12,17,1),(270,12,18,1),(271,12,19,1),(272,12,20,1),(273,12,21,1),(274,12,22,1),(275,12,23,1),(276,12,24,1),(277,12,25,1),(278,12,26,1),(279,12,27,1),(280,12,28,1),(281,12,29,1),(282,12,30,0),(283,12,31,1),(284,12,32,1),(285,12,33,1),(286,12,34,1),(287,12,35,1),(288,12,36,1),(289,12,37,1),(290,12,38,1),(291,12,39,1),(292,12,40,1),(293,12,41,1),(294,12,42,1),(295,11,1,1),(296,11,2,0),(297,11,3,1),(298,11,4,1),(299,11,5,0),(300,11,6,0),(301,11,7,1),(302,11,8,1),(303,11,9,0),(304,11,10,1),(305,11,11,0),(306,11,12,1),(307,11,13,1),(308,11,14,1),(309,11,15,0),(310,11,16,0),(311,11,17,1),(312,11,18,0),(313,11,19,1),(314,11,20,1),(315,11,21,0),(316,11,22,0),(317,11,23,1),(318,11,24,1),(319,11,25,0),(320,11,26,0),(321,11,27,0),(322,11,28,1),(323,11,29,0),(324,11,30,0),(325,11,31,0),(326,11,32,1),(327,11,33,0),(328,11,34,0),(329,11,35,1),(330,11,36,1),(331,11,37,0),(332,11,38,1),(333,11,39,0),(334,11,40,1),(335,11,41,0),(336,11,42,1),(337,19,1,1),(338,19,2,0),(339,19,3,1),(340,19,4,0),(341,19,5,0),(342,19,6,1),(343,19,7,1),(344,19,8,0),(345,19,9,1),(346,19,10,1),(347,19,11,1),(348,19,12,1),(349,19,13,0),(350,19,14,1),(351,19,15,1),(352,19,16,1),(353,19,17,1),(354,19,18,0),(355,19,19,0),(356,19,20,1),(357,19,21,1),(358,19,22,1),(359,19,23,0),(360,19,24,0),(361,19,25,1),(362,19,26,1),(363,19,27,1),(364,19,28,0),(365,19,29,0),(366,19,30,0),(367,19,31,0),(368,19,32,1),(369,19,33,1),(370,19,34,1),(371,19,35,1),(372,19,36,1),(373,19,37,0),(374,19,38,0),(375,19,39,0),(376,19,40,1),(377,19,41,1),(378,19,42,0),(379,20,1,1),(380,20,2,1),(381,20,3,1),(382,20,4,0),(383,20,5,0),(384,20,6,1),(385,20,7,0),(386,20,8,1),(387,20,9,0),(388,20,10,1),(389,20,11,1),(390,20,12,0),(391,20,13,0),(392,20,14,1),(393,20,15,1),(394,20,16,0),(395,20,17,0),(396,20,18,1),(397,20,19,1),(398,20,20,0),(399,20,21,0),(400,20,22,1),(401,20,23,1),(402,20,24,0),(403,20,25,1),(404,20,26,1),(405,20,27,0),(406,20,28,0),(407,20,29,1),(408,20,30,0),(409,20,31,0),(410,20,32,1),(411,20,33,0),(412,20,34,0),(413,20,35,1),(414,20,36,1),(415,20,37,1),(416,20,38,0),(417,20,39,0),(418,20,40,1),(419,20,41,1),(420,20,42,1),(421,15,1,1),(422,15,2,0),(423,15,3,1),(424,15,4,1),(425,15,5,1),(426,15,6,0),(427,15,7,1),(428,15,8,1),(429,15,9,1),(430,15,10,0),(431,15,11,1),(432,15,12,0),(433,15,13,1),(434,15,14,0),(435,15,15,1),(436,15,16,0),(437,15,17,1),(438,15,18,0),(439,15,19,1),(440,15,20,1),(441,15,21,1),(442,15,22,1),(443,15,23,0),(444,15,24,0),(445,15,25,1),(446,15,26,1),(447,15,27,0),(448,15,28,1),(449,15,29,1),(450,15,30,0),(451,15,31,1),(452,15,32,1),(453,15,33,1),(454,15,34,0),(455,15,35,1),(456,15,36,1),(457,15,37,0),(458,15,38,0),(459,15,39,1),(460,15,40,1),(461,15,41,0),(462,15,42,1),(463,17,1,1),(464,17,2,0),(465,17,3,1),(466,17,4,0),(467,17,5,0),(468,17,6,1),(469,17,7,1),(470,17,8,1),(471,17,9,0),(472,17,10,0),(473,17,11,1),(474,17,12,0),(475,17,13,1),(476,17,14,1),(477,17,15,1),(478,17,16,0),(479,17,17,1),(480,17,18,1),(481,17,19,1),(482,17,20,0),(483,17,21,1),(484,17,22,0),(485,17,23,1),(486,17,24,1),(487,17,25,0),(488,17,26,1),(489,17,27,1),(490,17,28,1),(491,17,29,0),(492,17,30,0),(493,17,31,1),(494,17,32,1),(495,17,33,1),(496,17,34,1),(497,17,35,1),(498,17,36,1),(499,17,37,1),(500,17,38,0),(501,17,39,1),(502,17,40,0),(503,17,41,1),(504,17,42,1),(505,16,1,1),(506,16,2,1),(507,16,3,1),(508,16,4,0),(509,16,5,1),(510,16,6,0),(511,16,7,0),(512,16,8,1),(513,16,9,1),(514,16,10,0),(515,16,11,1),(516,16,12,1),(517,16,13,1),(518,16,14,0),(519,16,15,1),(520,16,16,1),(521,16,17,1),(522,16,18,0),(523,16,19,0),(524,16,20,1),(525,16,21,0),(526,16,22,1),(527,16,23,0),(528,16,24,0),(529,16,25,1),(530,16,26,1),(531,16,27,0),(532,16,28,0),(533,16,29,1),(534,16,30,0),(535,16,31,1),(536,16,32,1),(537,16,33,0),(538,16,34,0),(539,16,35,1),(540,16,36,1),(541,16,37,1),(542,16,38,1),(543,16,39,0),(544,16,40,0),(545,16,41,0),(546,16,42,0),(547,14,1,1),(548,14,2,0),(549,14,3,1),(550,14,4,1),(551,14,5,0),(552,14,6,0),(553,14,7,0),(554,14,8,1),(555,14,9,1),(556,14,10,0),(557,14,11,0),(558,14,12,1),(559,14,13,0),(560,14,14,0),(561,14,15,0),(562,14,16,0),(563,14,17,1),(564,14,18,0),(565,14,19,0),(566,14,20,1),(567,14,21,0),(568,14,22,1),(569,14,23,1),(570,14,24,0),(571,14,25,0),(572,14,26,0),(573,14,27,1),(574,14,28,0),(575,14,29,0),(576,14,30,1),(577,14,31,1),(578,14,32,0),(579,14,33,0),(580,14,34,0),(581,14,35,1),(582,14,36,0),(583,14,37,1),(584,14,38,0),(585,14,39,0),(586,14,40,1),(587,14,41,0),(588,14,42,1);
/*!40000 ALTER TABLE `riasec_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riasec_questions`
--

DROP TABLE IF EXISTS `riasec_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `riasec_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pertanyaan` text COLLATE utf8mb4_general_ci NOT NULL,
  `dimensi` enum('R','I','A','S','E','C') COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riasec_questions`
--

LOCK TABLES `riasec_questions` WRITE;
/*!40000 ALTER TABLE `riasec_questions` DISABLE KEYS */;
INSERT INTO `riasec_questions` VALUES (1,'Saya suka memperbaiki mesin atau peralatan','R'),(2,'Saya menikmati bekerja di laboratorium','I'),(3,'Saya senang membuat karya seni atau menulis cerita','A'),(4,'Saya suka membantu orang lain memecahkan masalah','S'),(5,'Saya percaya diri dalam memimpin kelompok','E'),(6,'Saya suka mengatur dokumen atau data','C'),(7,'Saya suka bekerja di luar ruangan dan aktif bergerak','R'),(8,'Saya suka melakukan eksperimen untuk menemukan solusi','I'),(9,'Saya suka tampil di depan umum','A'),(10,'Saya suka memberi nasihat kepada teman','S'),(11,'Saya suka berjualan produk atau ide','E'),(12,'Saya suka menyusun jadwal atau agenda','C'),(13,'Saya suka memperbaiki barang elektronik','R'),(14,'Saya suka membaca buku sains atau teknologi','I'),(15,'Saya suka menggambar atau melukis','A'),(16,'Saya suka menjadi pendengar yang baik','S'),(17,'Saya suka mempengaruhi orang lain','E'),(18,'Saya suka mengorganisir berkas/dokumen','C'),(19,'Saya suka berkebun atau merawat tanaman','R'),(20,'Saya suka memecahkan teka-teki atau masalah logika','I'),(21,'Saya suka membuat puisi atau lagu','A'),(22,'Saya suka bekerja di kelompok sosial atau komunitas','S'),(23,'Saya suka menjadi pemimpin tim','E'),(24,'Saya suka mencatat pengeluaran dan pemasukan','C'),(25,'Saya suka menggunakan alat pertukangan','R'),(26,'Saya suka meneliti sesuatu yang baru','I'),(27,'Saya suka membuat kerajinan tangan','A'),(28,'Saya suka membantu di panti asuhan atau pelayanan masyarakat','S'),(29,'Saya suka negosiasi atau tawar-menawar','E'),(30,'Saya suka membuat laporan atau arsip','C'),(31,'Saya suka memasak di dapur','R'),(32,'Saya suka eksperimen kimia','I'),(33,'Saya suka membuat desain grafis','A'),(34,'Saya suka menjadi sukarelawan','S'),(35,'Saya suka menjadi MC atau presenter','E'),(36,'Saya suka membuat data dalam tabel','C'),(37,'Saya suka berkendara atau mengendarai kendaraan','R'),(38,'Saya suka memecahkan soal matematika','I'),(39,'Saya suka membuat video atau film pendek','A'),(40,'Saya suka mengajar anak-anak','S'),(41,'Saya suka memotivasi orang lain','E'),(42,'Saya suka membuat surat atau dokumen resmi','C');
/*!40000 ALTER TABLE `riasec_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riasec_results`
--

DROP TABLE IF EXISTS `riasec_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `riasec_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_student` int DEFAULT NULL,
  `skor_R` float DEFAULT NULL,
  `skor_I` float DEFAULT NULL,
  `skor_A` float DEFAULT NULL,
  `skor_S` float DEFAULT NULL,
  `skor_E` float DEFAULT NULL,
  `skor_C` float DEFAULT NULL,
  `top3` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_student` (`id_student`),
  CONSTRAINT `riasec_results_ibfk_1` FOREIGN KEY (`id_student`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riasec_results`
--

LOCK TABLES `riasec_results` WRITE;
/*!40000 ALTER TABLE `riasec_results` DISABLE KEYS */;
INSERT INTO `riasec_results` VALUES (1,1,3,1,3,3,3,3,'RAS'),(2,2,3,3,6,4,5,5,'AEC'),(3,3,5,6,1,5,4,4,'IRS'),(4,6,4,4,1,3,6,7,'CER'),(5,13,5,2,2,5,6,5,'ERS'),(6,5,3,4,4,4,3,4,'IAS'),(7,12,7,7,7,7,7,6,'RIA'),(8,11,4,5,1,4,3,4,'IRS'),(9,19,3,4,6,5,4,3,'ASI'),(10,20,4,5,2,3,5,4,'IER'),(11,15,6,4,6,4,5,2,'RAE'),(12,17,6,4,6,2,5,5,'RAE'),(13,16,5,6,3,2,5,2,'IRE'),(14,14,3,2,3,3,3,3,'RAS');
/*!40000 ALTER TABLE `riasec_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nisn` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `kelas` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_user` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nisn` (`nisn`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'1234567890','Budi Santoso','12 IPA 1',3),(2,'0987654321','Siti Aminah','12 IPS 2',4),(3,'1111111111','Andi Saputra','12 IPA 2',5),(4,'1111111112','Yhogi Saputra','12 IPA 2',6),(5,'1111111113','Citra Dewi','12 IPA 2',7),(6,'1111111114','Dewi Lestari','12 IPA 2',8),(7,'1111111115','Eka Pratama','12 IPA 2',9),(8,'1111111116','Fajar Nugroho','12 IPA 2',10),(9,'1111111117','Gita Putri','12 IPA 2',11),(10,'1111111118','Hendra Gunawan','12 IPA 2',12),(11,'1111111119','Intan Permata','12 IPA 2',13),(12,'1111111120','Joko Susilo','12 IPA 2',14),(13,'1111111121','Karina Sari','12 IPA 2',15),(14,'1111111122','Lukman Hakim','12 IPA 2',16),(15,'1111111123','Mega Putri','12 IPA 2',17),(16,'1111111124','Nanda Firdaus','12 IPA 2',18),(17,'1111111125','Oka Prasetya','12 IPA 2',19),(18,'1111111126','Putri Ayu','12 IPA 2',20),(19,'1111111127','Rizky Maulana','12 IPA 2',21),(20,'1111111128','Vivi Gesilanda','12 IPA 2',22),(21,'1111111129','Teguh Prakoso','12 IPA 2',23),(22,'1111111130','Umar Fauzi','12 IPA 2',24),(23,'1111111131','Vina Melati','12 IPA 2',25),(24,'1111111132','Wawan Setiawan','12 IPA 2',26),(25,'1111111133','Xenia Putri','12 IPA 2',27),(26,'1111111134','Yoga Pratama','12 IPA 2',28),(27,'1111111135','Zahra Ramadhani','12 IPA 2',29),(28,'1111111136','Ayu Lestari','12 IPA 2',30),(29,'1111111137','Bayu Saputra','12 IPA 2',31),(30,'1111111138','Cindy Oktaviani','12 IPA 2',32);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('admin','guru','siswa') COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin123','admin'),(2,'gurubk','guru123','guru'),(3,'siswa1','siswa123','siswa'),(4,'siswa2','siswa456','siswa'),(5,'siswa3','123456','siswa'),(6,'siswa4','123456','siswa'),(7,'siswa5','123456','siswa'),(8,'siswa6','123456','siswa'),(9,'siswa7','123456','siswa'),(10,'siswa8','123456','siswa'),(11,'siswa9','123456','siswa'),(12,'siswa10','123456','siswa'),(13,'siswa11','123456','siswa'),(14,'siswa12','123456','siswa'),(15,'siswa13','123456','siswa'),(16,'siswa14','123456','siswa'),(17,'siswa15','123456','siswa'),(18,'siswa16','123456','siswa'),(19,'siswa17','123456','siswa'),(20,'siswa18','123456','siswa'),(21,'siswa19','123456','siswa'),(22,'siswa20','123456','siswa'),(23,'siswa21','123456','siswa'),(24,'siswa22','123456','siswa'),(25,'siswa23','123456','siswa'),(26,'siswa24','123456','siswa'),(27,'siswa25','123456','siswa'),(28,'siswa26','123456','siswa'),(29,'siswa27','123456','siswa'),(30,'siswa28','123456','siswa'),(31,'siswa29','123456','siswa'),(32,'siswa30','123456','siswa');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-13 12:52:06
