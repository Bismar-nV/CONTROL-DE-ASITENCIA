-- Crear la base de datos
CREATE DATABASE PDIregistroDigital;
GO

-- Usar la base de datos
USE PDIregistroDigital;
GO

-- Tabla de estudiantes
CREATE TABLE Estudiante (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    foto NVARCHAR(255), -- Foto almacenada como datos binarios  
    estado INT
);
GO

-- Tabla de docentes
CREATE TABLE Docente (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    foto NVARCHAR(255), -- Foto almacenada como datos binarios    
    estado INT
);
GO

-- Crea la tabla Carrera con la columna id como IDENTITY
CREATE TABLE Carrera (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    estado INT
);
GO

-- Tabla de materias
CREATE TABLE Materia (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    carrera_id INT,
    estado INT,
    FOREIGN KEY (carrera_id) REFERENCES Carrera(id)
);
GO

-- Tabla de aulas
CREATE TABLE Aula (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    ubicacion NVARCHAR(255) NOT NULL,
    estado INT
);
GO

-- Tabla de clases
CREATE TABLE Clase (
    id INT PRIMARY KEY IDENTITY(1,1),
    materia_id INT,
    docente_id INT,
    aula_id INT,
    horario NVARCHAR(100),
    estado INT,
    FOREIGN KEY (materia_id) REFERENCES Materia(id),
    FOREIGN KEY (docente_id) REFERENCES Docente(id),
    FOREIGN KEY (aula_id) REFERENCES Aula(id)
);
GO

-- Tabla de asistencias
CREATE TABLE Asistencia (
    id INT PRIMARY KEY IDENTITY(1,1),
    clase_id INT,
    estudiante_id INT,
    fecha DATE,
    presente BIT,
    estado INT,
    FOREIGN KEY (clase_id) REFERENCES Clase(id),
    FOREIGN KEY (estudiante_id) REFERENCES Estudiante(id)
);
GO

-- Tabla de fotos
CREATE TABLE Foto (
    id INT PRIMARY KEY IDENTITY(1,1),
    persona_id INT NOT NULL,
    tipo_persona NVARCHAR(50) NOT NULL, -- Puede ser 'Estudiante' o 'Docente'
    nombre NVARCHAR(100) NOT NULL,
    direccion NVARCHAR(255), -- Dirección de la foto almacenada
    estado INT
);
GO

-- Procedimiento para insertar fotos desde estudiantes y docentes
CREATE PROCEDURE InsertarFotos
AS
BEGIN
    -- Insertar fotos desde la tabla Estudiante
    INSERT INTO Foto (persona_id, tipo_persona, nombre, direccion, estado)
    SELECT id, 'Estudiante', CONCAT(nombre, ' ', apellido), NULL, estado
    FROM Estudiante;

    -- Insertar fotos desde la tabla Docente
    INSERT INTO Foto (persona_id, tipo_persona, nombre, direccion, estado)
    SELECT id, 'Docente', CONCAT(nombre, ' ', apellido), NULL, estado
    FROM Docente;
END;
GO

-- Insertar datos en la tabla Estudiante
INSERT INTO Estudiante (nombre, apellido, email, foto, estado) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', NULL, 1),
('María', 'González', 'maria.gonzalez@example.com', NULL, 1),
('Carlos', 'Sánchez', 'carlos.sanchez@example.com', NULL, 1),
('Ana', 'Martínez', 'ana.martinez@example.com', NULL, 1),
('Luis', 'Rodríguez', 'luis.rodriguez@example.com', NULL, 1),
('Elena', 'Gómez', 'elena.gomez@example.com', NULL, 1),
('Pedro', 'Díaz', 'pedro.diaz@example.com', NULL, 1),
('Lucía', 'Fernández', 'lucia.fernandez@example.com', NULL, 1),
('Jorge', 'López', 'jorge.lopez@example.com', NULL, 1),
('Laura', 'Morales', 'laura.morales@example.com', NULL, 1);
GO

-- Insertar datos en la tabla Docente
INSERT INTO Docente (nombre, apellido, email, foto, estado) VALUES
('Roberto', 'Navarro', 'roberto.navarro@example.com', NULL, 1),
('Claudia', 'Méndez', 'claudia.mendez@example.com', NULL, 1),
('Miguel', 'Ortiz', 'miguel.ortiz@example.com', NULL, 1),
('Isabel', 'Romero', 'isabel.romero@example.com', NULL, 1),
('Fernando', 'Vega', 'fernando.vega@example.com', NULL, 1),
('Patricia', 'Suárez', 'patricia.suarez@example.com', NULL, 1),
('Antonio', 'Herrera', 'antonio.herrera@example.com', NULL, 1),
('Marta', 'Rubio', 'marta.rubio@example.com', NULL, 1),
('David', 'Paredes', 'david.paredes@example.com', NULL, 1),
('Susana', 'Campos', 'susana.campos@example.com', NULL, 1);
GO

-- Insertar datos en la tabla Carrera
INSERT INTO Carrera (nombre, estado) VALUES
('Ingeniería Informática', 1),
('Ingeniería Civil', 1),
('Medicina', 1),
('Derecho', 1),
('Administración de Empresas', 1),
('Psicología', 1),
('Arquitectura', 1),
('Biología', 1),
('Física', 1),
('Química', 1);
GO

-- Insertar datos en la tabla Materia
INSERT INTO Materia (nombre, carrera_id, estado) VALUES
('Programación', 1, 1),
('Estructuras', 2, 1),
('Anatomía', 3, 1),
('Derecho Constitucional', 4, 1),
('Contabilidad', 5, 1),
('Psicología General', 6, 1),
('Diseño Arquitectónico', 7, 1),
('Genética', 8, 1),
('Física Cuántica', 9, 1),
('Química Orgánica', 10, 1);
GO

-- Insertar datos en la tabla Aula
INSERT INTO Aula (nombre, ubicacion, estado) VALUES
('Aula 101', 'Edificio A, Planta Baja', 1),
('Aula 102', 'Edificio A, Planta Baja', 1),
('Aula 201', 'Edificio A, Planta Alta', 1),
('Aula 202', 'Edificio A, Planta Alta', 1),
('Laboratorio 301', 'Edificio B, Planta Baja', 1),
('Laboratorio 302', 'Edificio B, Planta Baja', 1),
('Aula 401', 'Edificio C, Planta Alta', 1),
('Aula 402', 'Edificio C, Planta Alta', 1),
('Auditorio', 'Edificio D, Planta Baja', 1),
('Sala de Conferencias', 'Edificio D, Planta Alta', 1);
GO

-- Insertar datos en la tabla Clase
INSERT INTO Clase (materia_id, docente_id, aula_id, horario, estado) VALUES
(1, 1, 1, 'Lunes 08:00-10:00', 1),
(2, 2, 2, 'Martes 10:00-12:00', 1),
(3, 3, 3, 'Miércoles 12:00-14:00', 1),
(4, 4, 4, 'Jueves 14:00-16:00', 1),
(5, 5, 5, 'Viernes 16:00-18:00', 1),
(6, 6, 6, 'Lunes 10:00-12:00', 1),
(7, 7, 7, 'Martes 12:00-14:00', 1),
(8, 8, 8, 'Miércoles 14:00-16:00', 1),
(9, 9, 9, 'Jueves 16:00-18:00', 1),
(10, 10, 10, 'Viernes 08:00-10:00', 1);
GO

-- Insertar datos en la tabla Asistencia
INSERT INTO Asistencia (clase_id, estudiante_id, fecha, presente, estado) VALUES
(1, 1, '2023-06-01', 1, 1),
(2, 2, '2023-06-01', 1, 1),
(3, 3, '2023-06-01', 0, 1),
(4, 4, '2023-06-01', 1, 1),
(5, 5, '2023-06-01', 0, 1),
(6, 1, '2023-06-02', 1, 1),
(7, 2, '2023-06-02', 1, 1),
(8, 3, '2023-06-02', 1, 1),
(9, 4, '2023-06-02', 0, 1),
(10, 5, '2023-06-02', 1, 1),
(11, 1, '2023-06-03', 1, 1),
(12, 2, '2023-06-03', 1, 1),
(13, 3, '2023-06-03', 0, 1),
(14, 4, '2023-06-03', 1, 1),
(15, 5, '2023-06-03', 1, 1),
(16, 6, '2023-06-04', 1, 1),
(17, 7, '2023-06-04', 1, 1),
(18, 8, '2023-06-04', 1, 1),
(19, 9, '2023-06-04', 0, 1),
(20, 10, '2023-06-04', 1, 1);
GO
