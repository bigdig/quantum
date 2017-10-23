mysqladmin -u root -p create rqalpha


############### get_price frequence 1d ################
 CREATE TABLE `get_price` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `open` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `total_turnover` float DEFAULT NULL,
  `volume` float DEFAULT NULL,
  `code` varchar(32) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `trade_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER  TABLE  `get_price`  ADD  INDEX index_name (`code`,  `trade_date`);