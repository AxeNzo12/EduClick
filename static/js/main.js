body: JSON.stringify({
        respuesta: respuestaSeleccionada,
        actividad_id: parseInt(materiaId) // <-- Agrega parseInt() para convertirlo a número
    })