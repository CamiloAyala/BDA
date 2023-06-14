-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: college_db
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `Enrolled_in_fact`
--

DROP TABLE IF EXISTS `Enrolled_in_fact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Enrolled_in_fact` (
  `en_id` int unsigned NOT NULL AUTO_INCREMENT,
  `en_us_id` int unsigned NOT NULL,
  `en_sb_id` int unsigned NOT NULL,
  `en_cr_id` int unsigned NOT NULL,
  `en_dt_id` int unsigned NOT NULL,
  `en_teacher` int unsigned NOT NULL,
  `en_shour` time NOT NULL,
  `en_fhour` time NOT NULL,
  `en_days` binary(6) NOT NULL,
  PRIMARY KEY (`en_id`,`en_us_id`,`en_sb_id`,`en_cr_id`,`en_dt_id`,`en_teacher`),
  KEY `fk_Enrolled_in_Subject1_idx` (`en_sb_id`),
  KEY `fk_Enrolled_in_Classroom1_idx` (`en_cr_id`),
  KEY `fk_Enrolled_in_User1_idx` (`en_us_id`),
  KEY `fk_Enrolled_in_User2_idx` (`en_teacher`),
  KEY `fk_Enrolled_in_Date1_idx` (`en_dt_id`),
  CONSTRAINT `fk_classroom` FOREIGN KEY (`en_cr_id`) REFERENCES `Classroom_dimension` (`cr_id`),
  CONSTRAINT `fk_Enrolled_in_Date1` FOREIGN KEY (`en_dt_id`) REFERENCES `Date_dimension` (`dt_id`),
  CONSTRAINT `fk_subject` FOREIGN KEY (`en_sb_id`) REFERENCES `Subject_dimension` (`sb_id`),
  CONSTRAINT `fk_teacher` FOREIGN KEY (`en_teacher`) REFERENCES `User_dimension` (`us_id`),
  CONSTRAINT `fk_user` FOREIGN KEY (`en_us_id`) REFERENCES `User_dimension` (`us_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-12 11:50:16
