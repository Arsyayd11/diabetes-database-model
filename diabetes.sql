-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2025 at 05:10 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `diabetes`
--

-- --------------------------------------------------------

--
-- Table structure for table `diabetes_inference`
--

CREATE TABLE `diabetes_inference` (
  `id` int(11) NOT NULL,
  `Pregnancies` int(11) NOT NULL,
  `Glucose` int(11) NOT NULL,
  `BloodPressure` int(11) NOT NULL,
  `SkinThickness` int(11) NOT NULL,
  `Insulin` int(11) NOT NULL,
  `BMI` float NOT NULL,
  `DiabetesPedigreeFunction` float NOT NULL,
  `Age` int(11) NOT NULL,
  `Outcome` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diabetes_inference`
--

INSERT INTO `diabetes_inference` (`id`, `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`, `Outcome`, `created_at`) VALUES
(1, 0, 89, 66, 23, 94, 28.1, 0.167, 21, 0, '2025-09-10 03:09:50'),
(2, 1, 137, 40, 35, 168, 43.1, 2.288, 33, 1, '2025-09-10 03:09:50'),
(3, 3, 78, 50, 32, 88, 31, 0.248, 26, 0, '2025-09-10 03:09:50'),
(4, 2, 115, 72, 20, 0, 24.5, 0.587, 30, 1, '2025-09-10 03:09:50'),
(5, 4, 140, 90, 33, 240, 37.2, 0.191, 45, 1, '2025-09-10 03:09:50'),
(6, 0, 99, 66, 16, 80, 24, 0.258, 22, 0, '2025-09-10 03:09:50'),
(7, 5, 120, 80, 25, 110, 29, 0.37, 36, 1, '2025-09-10 03:09:50'),
(8, 2, 85, 68, 20, 0, 27.5, 0.145, 25, 0, '2025-09-10 03:09:50'),
(9, 6, 150, 90, 35, 300, 40.3, 0.85, 50, 1, '2025-09-10 03:09:50'),
(10, 1, 92, 60, 18, 70, 23.1, 0.15, 24, 0, '2025-09-10 03:09:50'),
(11, 0, 110, 70, 22, 120, 26.8, 0.4, 31, 1, '2025-09-10 03:09:50'),
(12, 3, 105, 72, 20, 90, 25.6, 0.2, 29, 0, '2025-09-10 03:09:50');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diabetes_inference`
--
ALTER TABLE `diabetes_inference`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diabetes_inference`
--
ALTER TABLE `diabetes_inference`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
