CREATE DATABASE IF NOT EXISTS `copa_renault`;

USE `copa_renault`;

CREATE TABLE `Personas` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100),
  `email` VARCHAR(150) UNIQUE,
  `password` VARCHAR(255),
  `rol` ENUM('administrador','entrenador','jugador','staff'),
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Equipos` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100),
  `deporte` ENUM('futbol','baloncesto','voleibol'),
  `categoria` ENUM('masculino','femenino'),
  `entrenador_id` INT,
  `fecha_inscripcion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`entrenador_id`) REFERENCES `Personas`(`id`)
);

CREATE TABLE `Sponsors` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(150),
  `logo_url` VARCHAR(255),
  `descripcion` TEXT,
  `enlace_url` VARCHAR(255),
  `fecha_contrato` DATE
);

CREATE TABLE `Partidos` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `equipo_local_id` INT,
  `equipo_visita_id` INT,
  `fecha_hora` DATETIME,
  `sede` VARCHAR(150),
  `deporte` ENUM('futbol','baloncesto','voleibol'),
  `categoria` ENUM('masculino','femenino'),
  `estado` ENUM('pendiente','en_curso','finalizado') DEFAULT 'pendiente',
  `sponsor_id` INT,
  FOREIGN KEY (`equipo_local_id`) REFERENCES `Equipos`(`id`),
  FOREIGN KEY (`equipo_visita_id`) REFERENCES `Equipos`(`id`),
  FOREIGN KEY (`sponsor_id`) REFERENCES `Sponsors`(`id`)
);

CREATE TABLE `Cantina` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre_item` VARCHAR(150),
  `descripcion` TEXT,
  `precio` DECIMAL(7,2),
  `restricciones` TEXT,
  `disponible` BOOLEAN DEFAULT TRUE
);

CREATE TABLE `Vendedores_Cantina` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `nombre` VARCHAR(100),
  `dni` VARCHAR(20),
  `turno` ENUM('mañana','tarde','completo')
);

CREATE TABLE `Ordenes` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `persona_id` INT,
  `comprador_externo` BOOLEAN DEFAULT FALSE,
  `nombre_comprador` VARCHAR(150),
  `item_id` INT,
  `vendedor_id` INT,
  `fecha_venta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `cantidad` INT,
  FOREIGN KEY (`persona_id`) REFERENCES `Personas`(`id`),
  FOREIGN KEY (`item_id`) REFERENCES `Cantina`(`id`),
  FOREIGN KEY (`vendedor_id`) REFERENCES `Vendedores_Cantina`(`id`)
);

CREATE TABLE `Participaciones` (
  `persona_id` INT,
  `partido_id` INT,
  `minutos_jugados` INT,
  `goles` INT,
  PRIMARY KEY (`persona_id`,`partido_id`),
  FOREIGN KEY (`persona_id`) REFERENCES `Personas`(`id`),
  FOREIGN KEY (`partido_id`) REFERENCES `Partidos`(`id`)
);

CREATE TABLE `Tareas_Staff` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `persona_id` INT,
  `tarea` ENUM('cobro_entrada','cuidado_cancha','asistencia_general','ayuda_cantina'),
  `ubicacion` VARCHAR(100),
  `horario_inicio` DATETIME,
  `horario_fin` DATETIME,
  FOREIGN KEY (`persona_id`) REFERENCES `Personas`(`id`)
);
