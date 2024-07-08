
//const URL = "http://127.0.0.1:5000/"

//Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"
const URL = "https://gaston2024.pythonanywhere.com/"

// Obtiene el contenido del inventario
function obtenerAutos() {
    fetch(URL + 'autos') // Realiza una solicitud GET al servidor y obtener la lista de Autos.
        .then(response => {
            // Si es exitosa (response.ok), convierte los datos de la respuesta de formato JSON a un objeto JavaScript.
            if (response.ok) { return response.json(); }
        })
        // Asigna los datos de los Autos obtenidos a la propiedad Autos del estado.
        .then(data => {
            const AutosTable = document.getElementById('Autos-table').getElementsByTagName('tbody')[0];
            AutosTable.innerHTML = ''; // Limpia la tabla antes de insertar nuevos datos
            data.forEach(auto => {
                const row = AutosTable.insertRow();
                row.innerHTML = `
                            <td align="center">${auto.codigo}</td>
                            <td align="center">${auto.color}</td>
                            <td align="center">${auto.modelo}</td>
                            <td align="center">${auto.marca}</td>
                            <td align="center">${auto.cantidad}</td>
                            <td align="center">${auto.precio}</td>
                            <td align="center"><button onclick="eliminarAuto('${auto.codigo}')">Eliminar</button></td>
                        `;
            });
        })
        // Captura y maneja errores, mostrando una alerta en caso de error al obtener los Autos.
        .catch(error => {
            console.log('Error:', error);
            alert('Error al obtener los Autos.');
        });
}

// Se utiliza para eliminar un Auto.
function eliminarAuto(codigo) {
    // Se muestra un diálogo de confirmación. Si el usuario confirma, se realiza una solicitud DELETE al servidor a través de fetch(URL + 'Autos/${codigo}', {method: 'DELETE' }).
    if (confirm('¿Estás seguro de que quieres eliminar este Auto?')) {
        fetch(URL + `autos/${codigo}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    // Si es exitosa (response.ok), elimina el Auto y da mensaje de ok.
                    obtenerAutos(); // Vuelve a obtener la lista de Autos para actualizar la tabla.
                    alert('Auto eliminado correctamente.');
                }
            })
            // En caso de error, mostramos una alerta con un mensaje de error.
            .catch(error => {
                alert(error.message);
            });
    }
}

// Cuando la página se carga, llama a obtenerAutos para cargar la lista de Autos.
document.addEventListener('DOMContentLoaded', obtenerAutos);
