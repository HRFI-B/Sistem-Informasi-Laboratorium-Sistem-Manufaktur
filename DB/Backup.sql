-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: silsm
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `alat_praktikum`
--

DROP TABLE IF EXISTS `alat_praktikum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alat_praktikum` (
  `id_alat` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `spesifikasi_alat` varchar(255) DEFAULT NULL,
  `status_peminjaman` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_alat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alat_praktikum`
--

LOCK TABLES `alat_praktikum` WRITE;
/*!40000 ALTER TABLE `alat_praktikum` DISABLE KEYS */;
INSERT INTO `alat_praktikum` VALUES ('AL001','Laptop','i7-7400kf','Dipinjam');
/*!40000 ALTER TABLE `alat_praktikum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `arsip_ta`
--

DROP TABLE IF EXISTS `arsip_ta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arsip_ta` (
  `id_arsip` varchar(25) NOT NULL,
  `topik_arsip` varchar(255) DEFAULT NULL,
  `penulis_arsip` varchar(255) DEFAULT NULL,
  `status_peminjaman` varchar(15) DEFAULT NULL,
  `tanggal_arsip` date DEFAULT NULL,
  PRIMARY KEY (`id_arsip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arsip_ta`
--

LOCK TABLES `arsip_ta` WRITE;
/*!40000 ALTER TABLE `arsip_ta` DISABLE KEYS */;
INSERT INTO `arsip_ta` VALUES ('AR001','Analisis BBB','Tralalala','Tersedia','2023-10-07'),('AR002','Analisis Lalalala','Budi Setiawan','Tersedia','2001-02-22');
/*!40000 ALTER TABLE `arsip_ta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peminjaman_alat`
--

DROP TABLE IF EXISTS `peminjaman_alat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peminjaman_alat` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `id_alat` varchar(25) NOT NULL,
  `tanggal_peminjaman` date DEFAULT NULL,
  `tanggal_pengembalian` date DEFAULT NULL,
  `id_peminjam` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_peminjam` (`id_peminjam`),
  KEY `id_alat` (`id_alat`),
  CONSTRAINT `peminjaman_alat_ibfk_1` FOREIGN KEY (`id_peminjam`) REFERENCES `user` (`user_id`),
  CONSTRAINT `peminjaman_alat_ibfk_2` FOREIGN KEY (`id_alat`) REFERENCES `alat_praktikum` (`id_alat`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peminjaman_alat`
--

LOCK TABLES `peminjaman_alat` WRITE;
/*!40000 ALTER TABLE `peminjaman_alat` DISABLE KEYS */;
INSERT INTO `peminjaman_alat` VALUES (5,'AL001','2023-10-09','2023-10-16','MHS001');
/*!40000 ALTER TABLE `peminjaman_alat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peminjaman_arsip`
--

DROP TABLE IF EXISTS `peminjaman_arsip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peminjaman_arsip` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `id_arsip` varchar(25) NOT NULL,
  `tanggal_peminjaman` date DEFAULT NULL,
  `tanggal_pengembalian` date DEFAULT NULL,
  `id_peminjam` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_peminjam` (`id_peminjam`),
  KEY `id_arsip` (`id_arsip`),
  CONSTRAINT `peminjaman_arsip_ibfk_1` FOREIGN KEY (`id_peminjam`) REFERENCES `user` (`user_id`),
  CONSTRAINT `peminjaman_arsip_ibfk_2` FOREIGN KEY (`id_arsip`) REFERENCES `arsip_ta` (`id_arsip`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peminjaman_arsip`
--

LOCK TABLES `peminjaman_arsip` WRITE;
/*!40000 ALTER TABLE `peminjaman_arsip` DISABLE KEYS */;
/*!40000 ALTER TABLE `peminjaman_arsip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peminjaman_ruangan`
--

DROP TABLE IF EXISTS `peminjaman_ruangan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peminjaman_ruangan` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `id_ruangan` varchar(25) NOT NULL,
  `tanggal_peminjaman` datetime DEFAULT NULL,
  `waktu_peminjaman` int DEFAULT NULL,
  `id_peminjam` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_peminjam` (`id_peminjam`),
  KEY `id_ruangan` (`id_ruangan`),
  CONSTRAINT `peminjaman_ruangan_ibfk_1` FOREIGN KEY (`id_peminjam`) REFERENCES `user` (`user_id`),
  CONSTRAINT `peminjaman_ruangan_ibfk_2` FOREIGN KEY (`id_ruangan`) REFERENCES `ruang_praktikum` (`id_ruangan`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peminjaman_ruangan`
--

LOCK TABLES `peminjaman_ruangan` WRITE;
/*!40000 ALTER TABLE `peminjaman_ruangan` DISABLE KEYS */;
/*!40000 ALTER TABLE `peminjaman_ruangan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pengajuan_peminjaman`
--

DROP TABLE IF EXISTS `pengajuan_peminjaman`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pengajuan_peminjaman` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
  `tanggal_pengajuan` datetime DEFAULT NULL,
  `barang` varchar(30) DEFAULT NULL,
  `id_barang` varchar(25) DEFAULT NULL,
  `tanggal_peminjaman` date DEFAULT NULL,
  `waktu_peminjaman` int DEFAULT NULL,
  `tanggal_pengembalian` date DEFAULT NULL,
  `peminjam` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pengajuan_peminjaman`
--

LOCK TABLES `pengajuan_peminjaman` WRITE;
/*!40000 ALTER TABLE `pengajuan_peminjaman` DISABLE KEYS */;
/*!40000 ALTER TABLE `pengajuan_peminjaman` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ruang_praktikum`
--

DROP TABLE IF EXISTS `ruang_praktikum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ruang_praktikum` (
  `id_ruangan` varchar(10) NOT NULL,
  `nama` varchar(255) DEFAULT NULL,
  `lokasi` varchar(255) DEFAULT NULL,
  `status_peminjaman` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_ruangan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ruang_praktikum`
--

LOCK TABLES `ruang_praktikum` WRITE;
/*!40000 ALTER TABLE `ruang_praktikum` DISABLE KEYS */;
INSERT INTO `ruang_praktikum` VALUES ('TPB001','Laboratium TPB','GKU1','Tersedia');
/*!40000 ALTER TABLE `ruang_praktikum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nama` varchar(255) NOT NULL,
  `nim` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(30) NOT NULL,
  `email` varchar(130) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('ADM001','Aldi Ibrahim','119140130','81132329','Admin','ihza.119140130@student.itera.ac.id'),('MHS0002','Bambang','119140130','81132329frh','Mahasiswa','ihzafrh1@gmail.com'),('MHS001','Ihza','1119140130','81132329','Mahasiswa','ihzafrh@gmail.com');
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

-- Dump completed on 2023-10-09 19:44:39
