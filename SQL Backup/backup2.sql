-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 06, 2022 at 07:20 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `maindatabase`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminlogin`
--

CREATE TABLE `adminlogin` (
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adminlogin`
--

INSERT INTO `adminlogin` (`username`, `password`) VALUES
('root', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `clientconnector`
--

CREATE TABLE `clientconnector` (
  `uuid` text NOT NULL,
  `timecreated` text NOT NULL,
  `lastpinged` text NOT NULL,
  `status` int(11) NOT NULL,
  `ipaddress` text NOT NULL,
  `internalip` text NOT NULL,
  `osname` text NOT NULL,
  `commit` text NOT NULL,
  `correctmic` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clientconnector`
--

INSERT INTO `clientconnector` (`uuid`, `timecreated`, `lastpinged`, `status`, `ipaddress`, `internalip`, `osname`, `commit`, `correctmic`) VALUES
('49433c5a-2583-11ed-861a-e91fafb58039', '2022-08-26 22:02:55', '1661579284', 0, '98.242.199.97', '10.0.0.2', 'ADMIN', '5fce6', 2),
('8a514b42-25af-11ed-a60d-e91fafb58039', '2022-08-26 22:25:38', '1661579345', 0, '98.242.199.97', '10.0.0.24', 'NICHOLASLAPTOP', '5fce6', 0),
('8c5c0f4b-25bf-11ed-912d-08002797edd1', '2022-08-26 21:20:10', '1661579346', 0, '98.242.199.97', '10.0.2.15', 'VIRTUALMACHINE1', '5fce6', 0),
('97ec2973-2e06-11ed-979b-086266274ad8', '2022-09-06 13:08:13', '1662484093', 0, '98.242.199.97', '10.0.0.9', '', '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `cookies`
--

CREATE TABLE `cookies` (
  `ipaddress` text NOT NULL,
  `internalip` text NOT NULL,
  `groupname` text NOT NULL,
  `cookiedata` blob NOT NULL,
  `username` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `databaseinfo`
--

CREATE TABLE `databaseinfo` (
  `origin` text NOT NULL,
  `backup` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `databaseinfo`
--

INSERT INTO `databaseinfo` (`origin`, `backup`) VALUES
('2022-09-06 13:08:19', '2022-09-06 13:08:19');

-- --------------------------------------------------------

--
-- Table structure for table `groupstospam`
--

CREATE TABLE `groupstospam` (
  `groupspam` text NOT NULL,
  `time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `groupstospam`
--

INSERT INTO `groupstospam` (`groupspam`, `time`) VALUES
('https://www.roblox.com/groups/42/Building#!/about', '2022-08-24 05:40:26pm'),
('https://www.roblox.com/groups/2969540/Shyfoox-studios#!/about', '2022-08-24 05:40:30pm'),
('https://www.roblox.com/groups/4348877/Building-Friendships#!/about', '2022-08-27 01:33:25am');

-- --------------------------------------------------------

--
-- Table structure for table `machinelearning`
--

CREATE TABLE `machinelearning` (
  `messagessent` int(11) NOT NULL,
  `captchasuccess` text NOT NULL,
  `time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `robloxaccounts`
--

CREATE TABLE `robloxaccounts` (
  `username` text NOT NULL,
  `password` text NOT NULL,
  `timecreated` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `robloxaccounts`
--

INSERT INTO `robloxaccounts` (`username`, `password`, `timecreated`) VALUES
('RFV3ANGJ01NM8N3J8N2W', '93AMZ161F98WQE2KRJBO', '2022-08-24 17:23:44.838085'),
('I87UDND6HP7TUG4ZMVCL', 'E4209TI49VUDY5YFONXX', '2022-08-24 17:26:52.176435'),
('QBO4A3QL9LDPEAPVDCB9', 'H4AC05FCJFV6FU0D2EL2', '2022-08-24 17:37:48.809450'),
('VWKJZW2ZBSU73NG47PV7', 'I4HIKMN7O9VFXWVHM92D', '2022-08-26 22:18:24.338359'),
('GZ3AQXMPGPIHXPR2YV2J', 'P0AGCL9TL9S0IHOF5DXC', '2022-08-26 22:19:57.317318'),
('CQBCORDAZZ3KQJ5ZR2SE', 'VRMBS9N6VXRSM1D4D90V', '2022-08-26 22:28:17.521685'),
('NNY4UAUJ2DE82X6XNCTC', 'D1QY70P37R1IRYUAN9VI', '2022-08-26 22:28:43.559019'),
('R0ZM1F6RMN0HNV8ZPY5A', '5J46MD4ZKSBUZE03G788', '2022-08-26 22:28:17.521685'),
('NNY4UAUJ2DE82X6XNCTC', 'D1QY70P37R1IRYUAN9VI', '2022-08-26 22:28:43.559019'),
('NNY4UAUJ2DE82X6XNCTC', 'D1QY70P37R1IRYUAN9VI', '2022-08-26 22:28:43.559019'),
('ZPG6XVGOZ6CZB291J3U9', 'PAVEVFFEMVJF97C1QAUH', '2022-08-26 22:31:14.973292'),
('ZSHDRUZBSEEJ89W0T6XN', 'YXNPDQT2RR71LA6XMNBV', '2022-08-26 22:31:14.973292'),
('TSJ4IHSSL9IXTV0EP5CJ', 'T6XF8KOVCYGXRV8BVUSO', '2022-08-26 22:33:43.453328'),
('RDDWYW3CBA9J7G5CJB91', 'NXQGCQLTGWFIA32901AU', '2022-08-26 22:35:38.707444'),
('FVJ3D7A4LY6OFBE5Q2ED', 'OS7A7TECWMC04HVT09VW', '2022-08-26 22:35:38.707444'),
('A1LRFQ0TH0YLHTFDJXUK', 'VCTZRVGM182VJ5X5SU84', '2022-08-26 22:35:38.707444'),
('SVBYP1I065WW8HOA43H0', 'IJ8RN8VNL3GAS435B3EJ', '2022-08-26 23:17:09.813888'),
('SVBYP1I065WW8HOA43H0', 'IJ8RN8VNL3GAS435B3EJ', '2022-08-26 23:17:09.813888'),
('5T2BMLM8PAS6WHF200CY', 'KP2UMURYVHCHP6U8F1HZ', '2022-08-26 23:19:59.692305'),
('YD5AIKQVWKUHAYFP1KMK', 'VP7ET25FIUTVS7P6ZQLX', '2022-08-26 23:19:59.692305'),
('GVXF1T8J6NQ0JQCA7AO0', 'L07XHOJS093D77GMR7EG', '2022-08-26 23:19:59.692305'),
('GTGN0VKTPFTU62CRFNOA', 'FRROR98F1C1MAKSBNN1X', '2022-08-26 23:19:59.692305'),
('FOIYVHYJAYIGW4RTEVR6', '8KTVISHS5CY08XRDY3NT', '2022-08-26 23:19:59.692305'),
('77LF6EVOLNMV1JX13T9Z', 'M4WAGL329ZXCI87PKHUR', '2022-08-26 23:19:59.692305'),
('S0XRRPBEPJO37C4F6EW3', 'M4ZYYTYWLIGGVMJ87P15', '2022-08-26 23:39:25.399078'),
('X0C9WUADR68QREI1I3Y1', 'SFYS8AEODM700US06E6F', '2022-08-26 23:39:25.399078'),
('SHVCJIYBY8H9AXET4FSI', 'DHFUF7WP1FQW36FQD8II', '2022-08-26 23:39:25.399078'),
('A2MB86B389BDPT3QOU6C', '18RSQNBG5RKJ1VOOV5BQ', '2022-08-26 23:39:25.399078'),
('YMZK04J3A2NJLKNCFQUS', 'T590SM3L7QNH91NXCEIU', '2022-08-26 23:39:25.399078'),
('ZQE7G8GKFIHASNS5KS1L', '7FSS9HKDDU0S3SMV63VM', '2022-08-26 23:39:25.399078'),
('D6Y6FPCO3U3IZ4GVLSBJ', 'KVAHEFLVN4A46PH6TBVV', '2022-08-26 23:39:25.399078'),
('FW3QDMAHWRTUAUNDP76Q', 'U5G7KU4XS1EYI5AOVZ5W', '2022-08-26 23:39:25.399078'),
('SLK7KPOSNJ6VANT4ODW7', 'LOSVLW4Z6M5BWJRZCT1M', '2022-08-26 23:39:25.399078'),
('6YLJZ40D2WL2R0684VQ4', 'EAEBAGJ47IBU1EF7HPQ8', '2022-08-26 23:39:25.399078'),
('63HSDXTBDGFHXQBG4MBU', 'RXUXKH4VXG8ENBCQZRFT', '2022-08-26 23:39:25.399078'),
('XJ3ER37953HR0OXKDX8P', 'UCXSLU2BCAGHHCQY4MEP', '2022-08-26 23:39:25.399078'),
('HPEAQJ7ER5NHOYMVFE00', 'QUV5CGNSO5N1FVMKBZRP', '2022-08-26 23:39:25.399078'),
('HLH6YM3LRRYWA9AIWQVY', '8XVU0WFB9B7C5LJTM4WF', '2022-08-26 23:39:25.399078'),
('FZ2YH8R8T1G627WQH3XS', 'IMIPVJWHB6U9Z0OZYOCH', '2022-08-27 00:03:48.985514'),
('H9G8WTE0YWP878W28XEF', 'L4DYW30LOKMN9PIZK8V3', '2022-08-27 00:03:48.985514'),
('9X6W20EOUW1GUOCP6TL7', '5U1H01GVKRT15LFTHOTT', '2022-08-27 00:03:48.985514'),
('JXH5JFN4CATCJY8SSO8Y', '7305SYDC82TL2JX1UYBX', '2022-08-27 00:03:48.985514'),
('GHZW6BP5EHU52F98ZZ7O', 'WI0RWZMTXJSTWELMVLK6', '2022-08-27 00:03:48.985514'),
('B2GDHBNJHG0YUK0528KZ', 'PWXI6J9ZJ9N4FB0K7SII', '2022-08-26 21:20:10.201777'),
('B2GDHBNJHG0YUK0528KZ', 'PWXI6J9ZJ9N4FB0K7SII', '2022-08-26 21:20:10.201777'),
('AEXGARXNI94FZWUJIWJ0', 'OEK6DHIDXD6K4P5T2XQG', '2022-08-26 21:20:10.201777'),
('MTW5FYW7NK0B5MTHGW25', 'G0P6INV9853YTNAGORH3', '2022-08-26 21:20:10.201777'),
('CRGE5F65WEHPATLTY5JJ', '2XRLDX0QVDBIMPMZH8P2', '2022-08-26 21:20:10.201777'),
('128WV8ERNZN8WE4XR8IB', '7RVO82KSO4ZZDKQ104UA', '2022-08-26 21:28:59.820413'),
('GKSKKOX8X3E1MOJJXF7H', 'NWATMR5CR861TC0MYMVC', '2022-08-27 00:29:49.134449'),
('AOEYNP046QQA363QD9JK', 'GS6ORTUSP3BXKSODTVKG', '2022-08-26 21:31:36.378070'),
('2HWNMZN6AB2U0MZW6C2O', 'W5H8JJJKQW333YW27R6D', '2022-08-27 00:29:49.134449'),
('8O76EFIFQBT8GDY9VD0K', 'MWI81PXTWRQX16YO6NNQ', '2022-08-26 21:31:36.378070'),
('VHMPT7ZBFXJXMGJ9RLUX', 'Q105R9YUU6JGKQHIFR4H', '2022-08-27 00:29:49.134449'),
('DJS8B7V8B5RT47HMKKVH', 'AIC9F6TV8Y4EANSOV4V4', '2022-08-26 21:31:36.378070'),
('QNLHUGCF9OP5090PYA8X', '098OT46187USC6BR9L9B', '2022-08-27 00:29:49.134449'),
('UKAAO54959B6N07DO6NI', 'H800GFYIL5808PCYKEIR', '2022-08-26 21:31:36.378070'),
('VWQGER48F9ZB8HK0DF1I', 'IZ9UCAIOPTWM73O4NL52', '2022-08-27 00:29:49.134449'),
('F5I9COFPNM07ZSVT4MRX', 'OVPI50HCGXN17OMRYHRD', '2022-08-26 21:31:36.378070'),
('KRNQHRW58IU6C0QA536B', 'W60EQ57AMSEX26DQGK75', '2022-08-26 21:31:36.378070'),
('MVWZ936CPKBAIAPP41X7', 'YCDYJ04JNJQWSSHVLFH2', '2022-08-27 00:29:49.134449'),
('27X1YVQ8SZLIYZTPPZEK', '0J5MYM7LB86XUH6FPKD2', '2022-08-27 00:29:49.134449'),
('8BRP9EFC190JEO2IL2WV', 'PODBY0M3MMX67QSRY9H4', '2022-08-27 00:29:49.134449'),
('J0BUDVF2E6IHE6JEX38Y', '6QV7KWH3AAUTI4XC33T6', '2022-08-26 21:31:36.378070'),
('SPPYFDZ71ZRYLGDM6A0P', 'NYNRBMJM2U0S8RL6E4JF', '2022-08-26 21:31:36.378070'),
('A8NQWXASO86661L8OTBW', 'L9B5CT3RDYIOXKURGYMC', '2022-08-27 00:29:49.134449'),
('CBWQQDLDOAX9Z3PTS065', 'JF2M5CI9YMPOA75U0HWD', '2022-08-27 00:29:49.134449'),
('XJUWQ0EEZNWL9S2TZDIN', 'G6KAIY6GKYGGPC4RAXLF', '2022-08-26 21:31:36.378070'),
('IIWD45KMEFXD4389OQQ3', '4DKWAGSNLK40CGUODSWW', '2022-08-27 00:29:49.134449'),
('QC8EUSAESZIVYUCA5O8N', '3ZUB46FFSJ9UF65506JL', '2022-08-26 22:25:21.070557'),
('QC8EUSAESZIVYUCA5O8N', '3ZUB46FFSJ9UF65506JL', '2022-08-26 22:25:21.070557'),
('DDES6GL6OH5LV3ALW4BR', 'ZCNQLHAF9I59B9DXI59D', '2022-08-27 01:26:10.768837'),
('CVBOVLYBUPXZR8158DZR', '1TTOAVD2A2PCHJ38J42I', '2022-08-26 22:25:21.070557'),
('NHS98NUEXLULLST77CXR', 'VKXEK9YDYRWGFC370M98', '2022-08-27 01:26:10.768837'),
('GXBWAHNYQ1Y12SMKSHX0', 'JF2TA08B0NCHOVUVNX2V', '2022-08-26 22:25:21.070557'),
('0V6ZFR7BBUB0QG3O02NJ', 'AGD65F6ECPSCRJWGAVQ1', '2022-08-27 01:26:10.768837'),
('OSXT6DGJF2DV1XO8WJC6', 'FCQYLF0YUTUGFYMUTMSO', '2022-08-26 22:25:21.070557'),
('0ZBW9E233XVFQHXX65XO', '1N89FL27433NHH42BHRW', '2022-08-27 01:26:10.768837'),
('DRWBO1E7B5NSZJNM50SS', 'VLNT8LIEGRVAPPT81FDU', '2022-08-27 01:26:10.768837'),
('OVMRIR7DMRXNS113BXHR', '3C8INIBRBVZ1NUBHOHYD', '2022-08-26 22:25:21.070557'),
('FU5WEJM8OPE92Q1EJXTB', 'HN2LOFRH0MK46ZPJPVNR', '2022-08-27 01:26:10.768837'),
('PDMLCRG5HICTAC0QYCAT', 'XLFODJKWLEYF1NKECLFB', '2022-08-26 22:25:21.070557'),
('PMZIJ68HNCR53J63ELZ6', '2XGJI6U1GB8HW9FKUV7A', '2022-08-26 22:25:21.070557'),
('9IDQMWQRYT3OVH2UPHZ2', '9GDPESRSENK14EWBNUBC', '2022-08-27 01:26:10.768837'),
('KQOOGANJ2805CLCWADOF', '5O9UPW80HOXU0QJ23S8H', '2022-08-27 01:26:10.768837'),
('D50GQCW7D8IKP45BJEH5', 'F0GOR1C2JAITVA7XAAI9', '2022-08-26 22:25:21.070557'),
('TCWXD06OTFJNLYUYQM2B', 'LHJ3NGX6HSP5F4URXVVD', '2022-08-27 01:26:10.768837'),
('8I5QXM6WS7N8FN9XOR8Z', 'F5OB8ALH1LAKY7W6IJO3', '2022-08-26 22:25:21.070557'),
('PXVDK2R5C25OJVXM0X7W', 'S7HQ2FWJ69NUA9MMNVJ0', '2022-08-26 22:25:21.070557'),
('DXS38K7UT0S8R3JS0MQ2', 'RQ6Z0VTUGQCT625BFMO8', '2022-08-27 01:26:10.768837'),
('EESW08MRFUU8BB14JA8I', 'CEBYSLKC3ZFD5E7NC445', '2022-08-26 22:25:21.070557');

-- --------------------------------------------------------

--
-- Table structure for table `spambotmode`
--

CREATE TABLE `spambotmode` (
  `mode` int(11) NOT NULL,
  `time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `spambotmode`
--

INSERT INTO `spambotmode` (`mode`, `time`) VALUES
(0, '0'),
(0, '2022-08-24 05:10:53pm'),
(1, '2022-08-24 05:13:33pm'),
(0, '2022-08-24 05:14:26pm'),
(1, '2022-08-24 05:14:34pm'),
(0, '2022-08-24 05:15:31pm'),
(1, '2022-08-24 05:20:00pm'),
(0, '2022-08-24 05:21:36pm'),
(1, '2022-08-24 05:21:40pm'),
(0, '2022-08-24 05:22:09pm'),
(1, '2022-08-24 05:23:24pm'),
(0, '2022-08-24 05:23:34pm'),
(1, '2022-08-24 05:40:21pm'),
(0, '2022-08-26 10:23:55pm'),
(1, '2022-08-27 12:41:25am'),
(0, '2022-09-06 01:10:37pm');

-- --------------------------------------------------------

--
-- Table structure for table `spamgroup`
--

CREATE TABLE `spamgroup` (
  `groupspam` text NOT NULL,
  `time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `spamgroup`
--

INSERT INTO `spamgroup` (`groupspam`, `time`) VALUES
('https://www.roblox.com/groups/42/Building#!/about', '2022-08-24 05:26:11pm');

-- --------------------------------------------------------

--
-- Table structure for table `spammessage`
--

CREATE TABLE `spammessage` (
  `message` text NOT NULL,
  `time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `spammessage`
--

INSERT INTO `spammessage` (`message`, `time`) VALUES
('This is a test.', '2022-08-24 05:14:49pm'),
('Attention scums! The KING of ROBLOX is now @FADEDTOILETMAN ! Bow down to your new overlord! He has recruited an army of spam bots to spread the message, you better respect you new KING!', '2022-08-27 12:34:05am'),
('Attention scums! The KING of ROBLOX is now @FADEDTOILETMAN ! Bow down to your new overlord! He has recruited an army of spam bots to spread the message, you better respect your new KING!', '2022-08-27 12:34:15am');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
