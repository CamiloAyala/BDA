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
-- Table structure for table `Grades_fact`
--

DROP TABLE IF EXISTS `Grades_fact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Grades_fact` (
  `gr_id` int unsigned NOT NULL AUTO_INCREMENT,
  `gr_score` decimal(10,0) unsigned NOT NULL,
  `gr_sb_id` int unsigned NOT NULL,
  `gr_dt_id` int unsigned NOT NULL,
  `gr_us_id` int unsigned NOT NULL,
  PRIMARY KEY (`gr_id`,`gr_sb_id`,`gr_dt_id`,`gr_us_id`),
  KEY `fk_Grades_fact_Subject_dimension1_idx` (`gr_sb_id`),
  KEY `fk_Grades_fact_Date_dimension1_idx` (`gr_dt_id`),
  KEY `fk_Grades_fact_User_dimension1_idx` (`gr_us_id`),
  CONSTRAINT `fk_Grades_fact_Date_dimension1` FOREIGN KEY (`gr_dt_id`) REFERENCES `Date_dimension` (`dt_id`),
  CONSTRAINT `fk_Grades_fact_Subject_dimension1` FOREIGN KEY (`gr_sb_id`) REFERENCES `Subject_dimension` (`sb_id`),
  CONSTRAINT `fk_Grades_fact_User_dimension1` FOREIGN KEY (`gr_us_id`) REFERENCES `User_dimension` (`us_id`)
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
