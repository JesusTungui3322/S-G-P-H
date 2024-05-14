CREATE TABLE IF NOT EXISTS `Paciente` (
	`id` integer primary key NOT NULL UNIQUE,
	`nombre` TEXT NOT NULL,
	`apellido` TEXT NOT NULL,
	`cedula` TEXT NOT NULL,
	`historial_medico_id` INTEGER NOT NULL,
FOREIGN KEY(`historial_medico_id`) REFERENCES `HistorialMedico`(`id`)
);
CREATE TABLE IF NOT EXISTS `Medico` (
	`id` integer primary key NOT NULL UNIQUE,
	`nombre` TEXT NOT NULL,
	`apellido` TEXT NOT NULL,
	`cedula` TEXT NOT NULL,
	`especialidad_id` INTEGER NOT NULL,
FOREIGN KEY(`especialidad_id`) REFERENCES `Especialidad`(`id`)
);
CREATE TABLE IF NOT EXISTS `Medico_1715708772` (
	`id` integer primary key NOT NULL UNIQUE,
	`nombre` TEXT NOT NULL,
	`apellido` TEXT NOT NULL,
	`cedula` TEXT NOT NULL,
	`especialidad_id` INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS `Medico_1715708773` (
	`id` integer primary key NOT NULL UNIQUE,
	`nombre` TEXT NOT NULL,
	`apellido` TEXT NOT NULL,
	`cedula` TEXT NOT NULL,
	`especialidad_id` INTEGER NOT NULL,
FOREIGN KEY(`especialidad_id`) REFERENCES `undefined`(`id`)
);
CREATE TABLE IF NOT EXISTS `Cita` (
	`id` integer primary key NOT NULL UNIQUE,
	`paciente_id` INTEGER NOT NULL,
	`medico_id` INTEGER NOT NULL,
	`fecha` REAL NOT NULL,
FOREIGN KEY(`paciente_id`) REFERENCES `Paciente`(`id`),
FOREIGN KEY(`medico_id`) REFERENCES `Medico`(`id`)
);
CREATE TABLE IF NOT EXISTS `HistorialMedico` (
	`id` integer primary key NOT NULL UNIQUE,
	`detalles` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Especialidad` (
	`id` integer primary key NOT NULL UNIQUE,
	`nombre` TEXT NOT NULL,
	`descripcion` TEXT NOT NULL
);
FOREIGN KEY(`historial_medico_id`) REFERENCES `HistorialMedico`(`id`)
FOREIGN KEY(`especialidad_id`) REFERENCES `Especialidad`(`id`)

FOREIGN KEY(`especialidad_id`) REFERENCES `undefined`(`id`)
FOREIGN KEY(`paciente_id`) REFERENCES `Paciente`(`id`)
FOREIGN KEY(`medico_id`) REFERENCES `Medico`(`id`)

