CREATE DATABASE IF NOT EXISTS appdb;
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'password';
GRANT SELECT,UPDATE,INSERT ON appdb.* TO 'user'@'%';
FLUSH PRIVILEGES;

USE appdb;
SET NAMES utf8;


CREATE TABLE article
(
	id           INTEGER NOT NULL AUTO_INCREMENT,
	title                TINYTEXT NULL,
	content              TEXT NOT NULL,
	datetime                 DATETIME NOT NULL,
	id_source            INTEGER NOT NULL,
	primary key (id)
);


CREATE TABLE source
(
	id            INTEGER NOT NULL AUTO_INCREMENT,
	name                 TINYTEXT NOT NULL,
	source_type          varchar(10) NOT NULL,
	primary key (id)
);


ALTER TABLE article
ADD FOREIGN KEY SOURCE_KEY (id_source) REFERENCES source (id);


INSERT INTO source (name, source_type) VALUES
("Новости Интерфакс", 'rss'),
("ПРАЙМ", 'rss'),
("Opennet", 'rss'),
("РБК", 'tg'),
("РИА Новости", 'tg'),
('RT на русском', 'tg'),
('Colonelcassad', 'tg');
