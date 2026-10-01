import sqlite3
import os

os.makedirs('database', exist_ok=True)
conexion = sqlite3.connect('database/educlick.db')
cursor = conexion.cursor()

# Limpiar e inicializar tablas (las triples comillas son vitales aquí)
cursor.executescript("""
DROP TABLE IF EXISTS progreso;
DROP TABLE IF EXISTS actividades;
DROP TABLE IF EXISTS materias;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, grado INTEGER NOT NULL);
CREATE TABLE materias (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, icono TEXT NOT NULL);
CREATE TABLE actividades (id INTEGER PRIMARY KEY AUTOINCREMENT, materia_id INTEGER NOT NULL, grado INTEGER NOT NULL, pregunta TEXT NOT NULL, opciones TEXT NOT NULL, respuesta_correcta TEXT NOT NULL, FOREIGN KEY (materia_id) REFERENCES materias (id));
CREATE TABLE progreso (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario_id INTEGER NOT NULL, actividad_id INTEGER NOT NULL, completado INTEGER NOT NULL, FOREIGN KEY (usuario_id) REFERENCES usuarios (id), FOREIGN KEY (actividad_id) REFERENCES actividades (id));
""")

# 1. Insertar las 7 materias solicitadas
materias = [
    ('Matemáticas', '🧮'), ('Lenguas', '📖'), ('Geografía', '🌍'), 
    ('Inglés', '🇺🇸'), ('Ciencias Naturales', '🔬'), ('Informática', '💻'), ('Artes', '🎨')
]
cursor.executemany('INSERT INTO materias (nombre, icono) VALUES (?, ?)', materias)

# 2. Batería de preguntas de demostración
# 2. Batería masiva de preguntas (3 por cada grado en cada una de las 7 materias)
actividades = [
    # ================= MATEMÁTICAS (Materia 1) =================
    # Grado 1
    (1, 1, '¿Cuánto es 5 + 3?', '7,8,9', '8'),
    (1, 1, '¿Cuánto es 10 - 4?', '5,6,7', '6'),
    (1, 1, '¿Qué número sigue: 1, 2, 3, __?', '4,5,6', '4'),
    # Grado 2
    (1, 2, '¿Cuánto es 15 + 20?', '30,35,40', '35'),
    (1, 2, 'Si tienes 12 dulces y te comes 4, ¿cuántos quedan?', '6,8,10', '8'),
    (1, 2, '¿Cuánto es 2 veces 5?', '10,12,15', '10'),
    # Grado 3
    (1, 3, '¿Cuánto es 8 x 4?', '24,32,36', '32'),
    (1, 3, '¿Cuánto es 45 - 15?', '20,30,40', '30'),
    (1, 3, '¿Cuántos minutos hay en 1 hora?', '30,60,100', '60'),
    # Grado 4
    (1, 4, '¿Cuánto es 120 / 4?', '30,40,50', '30'),
    (1, 4, '¿Qué fracción es la mitad de un pastel?', '1/2,1/3,1/4', '1/2'),
    (1, 4, '¿Cuál es el área de un cuadrado de lado 5 cm?', '10 cm,20 cm,25 cm', '25 cm'),
    # Grado 5
    (1, 5, '¿Cuánto es 0.5 + 0.5?', '0.10,1.0,1.5', '1.0'),
    (1, 5, 'Si 1 kg cuesta $20, ¿cuánto cuestan 3.5 kg?', '$60,$70,$80', '$70'),
    (1, 5, '¿Cuántos grados tiene un círculo completo?', '180,360,90', '360'),
    # Grado 6
    (1, 6, 'Resuelve: 5 + 3 x 2', '16,11,10', '11'),
    (1, 6, '¿Cuál es el 20% de 100?', '10,20,50', '20'),
    (1, 6, 'Si x + 5 = 12, ¿cuánto vale x?', '5,6,7', '7'),

    # ================= LENGUAS (Materia 2) =================
    # Grado 1
    (2, 1, '¿Qué vocal falta en: P _ RRO?', 'A,E,I', 'E'),
    (2, 1, '¿Con qué letra empieza la palabra ÁRBOL?', 'A,E,O', 'A'),
    (2, 1, '¿Qué es un gato?', 'Una planta,Un animal,Un objeto', 'Un animal'),
    # Grado 2
    (2, 2, '¿Cuál es el sinónimo de FELIZ?', 'Triste,Contento,Enojado', 'Contento'),
    (2, 2, '¿Cuántas sílabas tiene CA-SA?', '1,2,3', '2'),
    (2, 2, '¿Qué hace el perro?', 'Maúlla,Ladra,Canta', 'Ladra'),
    # Grado 3
    (2, 3, '¿Cuál es el sujeto en "El niño juega"?', 'El,niño,juega', 'niño'),
    (2, 3, 'Elige el verbo en esta lista:', 'Correr,Mesa,Rojo', 'Correr'),
    (2, 3, '¿Qué tipo de palabra es "Bonito"?', 'Sustantivo,Verbo,Adjetivo', 'Adjetivo'),
    # Grado 4
    (2, 4, '¿Cuál de estas es una palabra aguda?', 'Camión,Árbol,Mesa', 'Camión'),
    (2, 4, '¿Cuál es el antónimo de LUZ?', 'Día,Oscuridad,Sol', 'Oscuridad'),
    (2, 4, '¿Qué signo usamos para preguntar?', '¡ !,¿ ?,( )', '¿ ?'),
    # Grado 5
    (2, 5, 'Identifica el nexo en "Rápido pero seguro":', 'Rápido,pero,seguro', 'pero'),
    (2, 5, '¿Qué tipo de texto es un cuento?', 'Informativo,Narrativo,Científico', 'Narrativo'),
    (2, 5, 'Palabra escrita correctamente:', 'Haser,Hacer,Aser', 'Hacer'),
    # Grado 6
    (2, 6, '¿Qué es una metáfora?', 'Una burla,Una rima,Una comparación', 'Una comparación'),
    (2, 6, '¿Cuál lleva tilde por ser esdrújula?', 'Musica,Música,Musicá', 'Música'),
    (2, 6, 'Elige el pronombre personal:', 'Yo,Ayer,Mucho', 'Yo'),

    # ================= GEOGRAFÍA (Materia 3) =================
    # Grado 1
    (3, 1, '¿En qué planeta vivimos?', 'Marte,Tierra,Venus', 'Tierra'),
    (3, 1, '¿Qué sale de día?', 'La Luna,Las estrellas,El Sol', 'El Sol'),
    (3, 1, '¿De qué color vemos los mares en un mapa?', 'Verde,Azul,Rojo', 'Azul'),
    # Grado 2
    (3, 2, '¿Cuál de estos es un punto cardinal?', 'Norte,Centro,Lado', 'Norte'),
    (3, 2, '¿Qué usamos para protegernos de la lluvia?', 'Lentes de sol,Paraguas,Gorra', 'Paraguas'),
    (3, 2, '¿Dónde hay más árboles?', 'En el bosque,En la ciudad,En el desierto', 'En el bosque'),
    # Grado 3
    (3, 3, '¿En qué país vivimos?', 'España,México,Brasil', 'México'),
    (3, 3, '¿Cuál es un océano?', 'Pacífico,Amazonas,Nilo', 'Pacífico'),
    (3, 3, 'Representación plana de la Tierra:', 'Globo terráqueo,Mapa,Foto', 'Mapa'),
    # Grado 4
    (3, 4, 'Continente más grande del mundo:', 'América,Asia,Europa', 'Asia'),
    (3, 4, '¿Cómo se llama a la forma de la superficie terrestre?', 'Clima,Relieve,Fauna', 'Relieve'),
    (3, 4, 'Frontera norte de México:', 'Guatemala,Canadá,Estados Unidos', 'Estados Unidos'),
    # Grado 5
    (3, 5, 'Movimiento de la Tierra alrededor del Sol:', 'Rotación,Traslación,Vibración', 'Traslación'),
    (3, 5, '¿Qué es la migración?', 'Cuidar animales,Moverse de país a país,Contaminar', 'Moverse de país a país'),
    (3, 5, 'Capital de Francia:', 'Londres,París,Madrid', 'París'),
    # Grado 6
    (3, 6, '¿Para qué sirven los husos horarios?', 'Medir la lluvia,Determinar la hora,Medir distancias', 'Determinar la hora'),
    (3, 6, 'Línea imaginaria que divide la Tierra por la mitad:', 'Ecuador,Meridiano,Trópico', 'Ecuador'),
    (3, 6, 'Principal bloque económico de América del Norte:', 'T-MEC,Unión Europea,Mercosur', 'T-MEC'),

    # ================= INGLÉS (Materia 4) =================
    # Grado 1
    (4, 1, '¿Cómo se dice "Rojo" en inglés?', 'Blue,Red,Green', 'Red'),
    (4, 1, '¿Cómo se dice "Hola"?', 'Bye,Hello,Please', 'Hello'),
    (4, 1, '¿Qué animal es un "Dog"?', 'Gato,Perro,Pájaro', 'Perro'),
    # Grado 2
    (4, 2, 'Número "Tres" en inglés:', 'Two,Three,Four', 'Three'),
    (4, 2, '¿Qué color es "Yellow"?', 'Amarillo,Rojo,Verde', 'Amarillo'),
    (4, 2, '¿Qué parte del cuerpo es "Head"?', 'Mano,Pie,Cabeza', 'Cabeza'),
    # Grado 3
    (4, 3, 'Traduce "The cat is black":', 'El gato es blanco,El perro es negro,El gato es negro', 'El gato es negro'),
    (4, 3, '¿Qué significa "Good morning"?', 'Buenas tardes,Buenos días,Buenas noches', 'Buenos días'),
    (4, 3, '¿Cómo se dice "Manzana"?', 'Apple,Banana,Orange', 'Apple'),
    # Grado 4
    (4, 4, 'Completa: "I ___ a student"', 'am,is,are', 'am'),
    (4, 4, '¿Qué día es "Monday"?', 'Lunes,Martes,Miércoles', 'Lunes'),
    (4, 4, 'Traduce "I like to play":', 'Me gusta dormir,Me gusta jugar,Yo puedo correr', 'Me gusta jugar'),
    # Grado 5
    (4, 5, 'El plural de "Child" (Niño) es:', 'Childs,Children,Childrens', 'Children'),
    (4, 5, '¿Qué haces en la "Kitchen"?', 'Dormir,Cocinar,Bañarte', 'Cocinar'),
    (4, 5, 'Completa: "She ___ playing soccer"', 'am,is,are', 'is'),
    # Grado 6
    (4, 6, 'Pasado del verbo "Go" (Ir):', 'Went,Goed,Gone', 'Went'),
    (4, 6, '¿Qué significa "Always"?', 'Nunca,A veces,Siempre', 'Siempre'),
    (4, 6, 'Pregunta correcta:', 'You are happy?,Are you happy?,Are happy you?', 'Are you happy?'),

    # ================= CIENCIAS NATURALES (Materia 5) =================
    # Grado 1
    (5, 1, '¿Cuál de estos tiene vida?', 'Roca,Planta,Agua', 'Planta'),
    (5, 1, '¿Con qué parte del cuerpo podemos ver?', 'Ojos,Orejas,Manos', 'Ojos'),
    (5, 1, '¿De dónde sacan agua las plantas?', 'Del viento,De la raíz,Del sol', 'De la raíz'),
    # Grado 2
    (5, 2, '¿Qué animal es el mejor amigo del hombre?', 'Gato,Perro,Pez', 'Perro'),
    (5, 2, '¿Qué nos da la vaca?', 'Huevos,Leche,Lana', 'Leche'),
    (5, 2, '¿Qué necesitan las plantas para vivir?', 'Sol y agua,Juguetes,Oscuridad', 'Sol y agua'),
    # Grado 3
    (5, 3, 'El hielo es agua en estado:', 'Líquido,Sólido,Gas', 'Sólido'),
    (5, 3, 'Animal que come solo plantas:', 'Carnívoro,Herbívoro,Omnívoro', 'Herbívoro'),
    (5, 3, '¿Por dónde respiran los peces?', 'Pulmones,Nariz,Branquias', 'Branquias'),
    # Grado 4
    (5, 4, 'Nuestra galaxia se llama:', 'Andrómeda,Vía Láctea,Sistema Solar', 'Vía Láctea'),
    (5, 4, 'El conjunto de huesos forma el:', 'Sistema nervioso,Esqueleto,Sistema digestivo', 'Esqueleto'),
    (5, 4, 'Movimiento del corazón para bombear sangre:', 'Respiración,Latido,Digestión', 'Latido'),
    # Grado 5
    (5, 5, 'Gas que respiramos los humanos para vivir:', 'Oxígeno,Dióxido de carbono,Helio', 'Oxígeno'),
    (5, 5, 'Conjunto de seres vivos y su medio ambiente:', 'Población,Ecosistema,Ciudad', 'Ecosistema'),
    (5, 5, 'El agua y el aceite forman una mezcla:', 'Homogénea,Heterogénea,Pura', 'Heterogénea'),
    # Grado 6
    (5, 6, 'Unidad más pequeña que forma a los seres vivos:', 'Órgano,Tejido,Célula', 'Célula'),
    (5, 6, 'Fuerza que atrae los objetos hacia el suelo:', 'Magnetismo,Gravedad,Fricción', 'Gravedad'),
    (5, 6, 'Ejemplo de energía renovable:', 'Petróleo,Carbón,Solar', 'Solar'),

    # ================= INFORMÁTICA (Materia 6) =================
    # Grado 1
    (6, 1, '¿Qué usamos para mover la flechita en la pantalla?', 'El teclado,El mouse,La bocina', 'El mouse'),
    (6, 1, '¿Dónde vemos las imágenes de la computadora?', 'En el teclado,En el monitor,En los cables', 'En el monitor'),
    (6, 1, 'Para escuchar música en la PC usamos:', 'Bocinas,Mouse,Pantalla', 'Bocinas'),
    # Grado 2
    (6, 2, '¿Qué usamos para escribir letras y números en la PC?', 'Mouse,Teclado,Cámara', 'Teclado'),
    (6, 2, 'Cuando terminas de usar la PC debes:', 'Dejarla prendida,Apagarla,Desconectarla', 'Apagarla'),
    (6, 2, '¿En qué botón hacemos clic para apagar Windows?', 'Botón Inicio,En la hora,En el volumen', 'Botón Inicio'),
    # Grado 3
    (6, 3, 'Red mundial que conecta las computadoras:', 'WiFi,Internet,Bluetooth', 'Internet'),
    (6, 3, 'Programa para navegar por Internet:', 'Word,Chrome,Paint', 'Chrome'),
    (6, 3, 'Si te equivocas al escribir, borras con:', 'Enter,Espacio,Retroceso', 'Retroceso'),
    # Grado 4
    (6, 4, 'Microsoft Word sirve principalmente para:', 'Hacer dibujos,Escribir textos,Jugar', 'Escribir textos'),
    (6, 4, '¿Qué significa guardar un archivo?', 'Borrarlo,Conservarlo para después,Imprimirlo', 'Conservarlo para después'),
    (6, 4, 'La carpeta amarilla en la PC sirve para:', 'Organizar archivos,Borrar virus,Navegar', 'Organizar archivos'),
    # Grado 5
    (6, 5, '¿Qué debes hacer con tus contraseñas?', 'Compartirlas,Anotarlas en público,Mantenerlas en secreto', 'Mantenerlas en secreto'),
    (6, 5, '¿Qué programa usas para hacer presentaciones con diapositivas?', 'Excel,PowerPoint,Paint', 'PowerPoint'),
    (6, 5, 'El "Cerebro" de la computadora se llama:', 'Disco Duro,Procesador,Memoria RAM', 'Procesador'),
    # Grado 6
    (6, 6, 'Atajo de teclado para COPIAR un texto:', 'Ctrl + C,Ctrl + V,Ctrl + X', 'Ctrl + C'),
    (6, 6, 'Las partes físicas de la computadora (lo que se toca) son el:', 'Software,Hardware,Malware', 'Hardware'),
    (6, 6, 'Las aplicaciones y programas de la PC son el:', 'Software,Hardware,Virus', 'Software'),

    # ================= ARTES (Materia 7) =================
    # Grado 1
    (7, 1, '¿Con qué herramienta puedes pintar en papel?', 'Tijeras,Pincel,Pegamento', 'Pincel'),
    (7, 1, 'Si dibujas un Sol, ¿de qué color lo pintas normalmente?', 'Azul,Amarillo,Morado', 'Amarillo'),
    (7, 1, 'Arte de mover el cuerpo al ritmo de la música:', 'Pintura,Danza,Escultura', 'Danza'),
    # Grado 2
    (7, 2, 'Si mezclas amarillo y azul, ¿qué color obtienes?', 'Rojo,Verde,Naranja', 'Verde'),
    (7, 2, '¿Cuál de estos es un instrumento musical?', 'Guitarra,Silla,Lápiz', 'Guitarra'),
    (7, 2, '¿Con qué hacemos figuras de plastilina?', 'Con los pies,Con las manos,Con los ojos', 'Con las manos'),
    # Grado 3
    (7, 3, 'Si mezclas rojo y amarillo, ¿qué color obtienes?', 'Morado,Naranja,Verde', 'Naranja'),
    (7, 3, 'Persona que escribe y toca canciones:', 'Pintor,Escultor,Músico', 'Músico'),
    (7, 3, '¿Qué material se usa mucho en la escultura tradicional?', 'Agua,Barro,Aire', 'Barro'),
    # Grado 4
    (7, 4, 'Famoso pintor que hizo "La Mona Lisa":', 'Picasso,Da Vinci,Van Gogh', 'Da Vinci'),
    (7, 4, 'Lugar donde los actores presentan una obra en vivo:', 'Teatro,Cine,Estadio', 'Teatro'),
    (7, 4, 'Instrumento de viento:', 'Batería,Flauta,Guitarra', 'Flauta'),
    # Grado 5
    (7, 5, 'El arte de crear edificios y casas hermosas se llama:', 'Pintura,Arquitectura,Danza', 'Arquitectura'),
    (7, 5, '¿Qué son el Do, Re, Mi, Fa, Sol, La, Si?', 'Colores,Notas musicales,Pinceles', 'Notas musicales'),
    (7, 5, 'Pintor mexicano famoso por sus murales:', 'Diego Rivera,Salvador Dalí,Claude Monet', 'Diego Rivera'),
    # Grado 6
    (7, 6, 'Arte que captura imágenes con una cámara:', 'Fotografía,Escultura,Música', 'Fotografía'),
    (7, 6, '¿A qué arte se le conoce como el "Séptimo arte"?', 'Cine,Teatro,Pintura', 'Cine'),
    (7, 6, 'Estilo donde el pintor usa figuras geométricas (como cubos):', 'Realismo,Cubismo,Impresionismo', 'Cubismo')
]
cursor.executemany('INSERT INTO actividades (materia_id, grado, pregunta, opciones, respuesta_correcta) VALUES (?, ?, ?, ?, ?)', actividades)

conexion.commit()
conexion.close()
print("¡Éxito! Base de datos reiniciada con 6 grados, 7 materias y preguntas listas.")