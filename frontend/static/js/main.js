document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const fileInput = document.getElementById('fileInput').files;
    
    // Validamos que el usuario realmente haya seleccionado un archivo
    if (fileInput.length === 0) {
        alert("Por favor, selecciona un archivo de imagen.");
        return;
    }
    
    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', fileInput[0]); // [0] extrae el archivo binario real de la lista
    formData.append('album_id', '00000000-0000-0000-0000-000000000000'); 

    try {
        const response = await fetch('/api/v1/photos/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // El backend procesó todo con éxito, refrescamos la vista de Jinja2
            window.location.reload();
        } else {
            // Si el backend responde con un error HTTP (ej: 400, 422 o 500)
            const errorData = await response.json();
            console.error('Error detallado del backend:', errorData);
            alert('ERROR EN EL AMPLIFICADOR: No se pudo procesar el archivo.');
        }
    } catch (error) {
        console.error('Error de red o conexión:', error);
        alert('ERROR DE CONEXIÓN: El servidor no responde.');
    }
});

