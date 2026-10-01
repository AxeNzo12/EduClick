-- Borrar tablas si ya existen (útil para reiniciar la base de datos en fase de desarrollo)
DROP TABLE IF EXISTS progreso;
DROP TABLE IF EXISTS actividades;
DROP TABLE IF EXISTS materias;
DROP TABLE IF EXISTS usuarios;

-- Tabla de Usuarios (Para almacenar el progreso futuro)
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    grado INTEGER NOT NULL
);

-- Tabla de Materias (Catálogo curricular)
CREATE TABLE materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

-- Tabla de Actividades (Catálogo de ejercicios)
CREATE TABLE actividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id INTEGER NOT NULL,
    grado INTEGER NOT NULL,
    pregunta TEXT NOT NULL,
    opciones TEXT NOT NULL, -- Guardaremos las opciones separadas por comas o en formato JSON
    respuesta_correcta TEXT NOT NULL,
    FOREIGN KEY (materia_id) REFERENCES materias (id)
);

-- Tabla de Progreso (Relación entre usuarios y actividades completadas)
CREATE TABLE progreso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    actividad_id INTEGER NOT NULL,
    completado BOOLEAN DEFAULT 0,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (actividad_id) REFERENCES actividades (id)
);

-- ==========================================
-- INSERCIÓN DE DATOS OFICIALES (CATÁLOGO Y PREGUNTAS)
-- ==========================================

-- Insertar la lista oficial de materias
INSERT INTO materias (nombre) VALUES ('Matemáticas');         -- ID 1
INSERT INTO materias (nombre) VALUES ('Lenguaje');            -- ID 2
INSERT INTO materias (nombre) VALUES ('Geografía');           -- ID 3
INSERT INTO materias (nombre) VALUES ('Inglés');              -- ID 4
INSERT INTO materias (nombre) VALUES ('Ciencias Naturales');  -- ID 5
INSERT INTO materias (nombre) VALUES ('Informática');         -- ID 6
INSERT INTO materias (nombre) VALUES ('Artes');               -- ID 7

-- Banco de preguntas iniciales para Primer Grado (grado = 1)

-- Matemáticas (ID 1)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (1, 1, '¿Cuánto es 5 + 3?', '7,8,9', '8');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (1, 1, 'Si tienes 4 manzanas y te comes 1, ¿cuántas quedan?', '2,3,4', '3');

-- Lenguaje (ID 2)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (2, 1, 'Selecciona la vocal que falta: M _ S A (Mesa)', 'A,E,O', 'E');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (2, 1, '¿Con qué letra empieza la palabra "Gato"?', 'C,G,P', 'G');

-- Geografía (ID 3)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (3, 1, '¿En qué planeta vivimos?', 'Marte,Tierra,Júpiter', 'Tierra');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (3, 1, '¿De qué color es predominantemente el agua en los mapas?', 'Verde,Rojo,Azul', 'Azul');

-- Inglés (ID 4)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (4, 1, '¿Cómo se dice "Rojo" en inglés?', 'Blue,Red,Green', 'Red');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (4, 1, '¿Qué significa la palabra "Cat"?', 'Perro,Gato,Pájaro', 'Gato');

-- Ciencias Naturales (ID 5)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (5, 1, '¿Cuál de estos es un ser vivo?', 'Una roca,Un árbol,El plástico', 'Un árbol');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (5, 1, '¿Qué órgano usamos para respirar?', 'Pulmones,Estómago,Ojos', 'Pulmones');

-- Informática (ID 6)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (6, 1, '¿Qué dispositivo se usa principalmente para mover el cursor en la pantalla?', 'Teclado,Ratón (Mouse),Bocina', 'Ratón (Mouse)');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (6, 1, '¿Dónde se escriben las palabras usando la computadora?', 'Monitor,Teclado,Impresora', 'Teclado');

-- Artes (ID 7)
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (7, 1, '¿Qué color obtenemos al mezclar el azul y el amarillo?', 'Verde,Morado,Naranja', 'Verde');
INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) 
VALUES (7, 1, '¿Cuál de los siguientes es un instrumento musical?', 'Lápiz,Guitarra,Cuaderno', 'Guitarra');

-- Crear un usuario por defecto para el sistema de puntos
INSERT INTO usuarios (nombre, grado) VALUES ('Estudiante 1', 1);