
// const URL = "http://127.0.0.1:5000/"

// Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"
const URL = "https://gaston2024.pythonanywhere.com/"


// Realizamos la solicitud GET al servidor para obtener todos los Autos.
fetch(URL + 'autos')
    .then(function (response) {
        if (response.ok) {
            //Si la respuesta es exitosa (response.ok), convierte el cuerpo de la respuesta de formato JSON a un objeto JavaScript y pasa estos datos a la siguiente promesa then.
            return response.json();
        } else {
            // Si hubo un error, lanzar explícitamente una excepción para ser "catcheada" más adelante
            throw new Error('Error al obtener los autos.');
        }
    })

    //Esta función maneja los datos convertidos del JSON.
    .then(function (data) {
        let tablaAutos = document.getElementById('tablaAutos'); //Selecciona el elemento del DOM donde se mostrarán los Autos.

        // Iteramos sobre cada Auto y agregamos filas a la tabla
        for (let Auto of data) {
            let fila = document.createElement('tr'); //Crea una nueva fila de tabla (<tr>) para cada Auto.
            fila.innerHTML = '<td align="center">' + Auto.codigo + '</td>' +
                '<td align="center">' + Auto.color + '</td>' +
                '<td align="center">' + Auto.modelo + '</td>' +
                '<td align="center">' + Auto.marca + '</td>' +
                '<td align="center">' + Auto.cantidad + '</td>' +
                '<td align="center">' + Auto.precio + '</td>' +
                // Mostrar miniatura de la imagen
                // '<td><img class="imgAuto" src=../static/imagenes/' + Auto.imagen_url +' alt="Imagen del auto"></td>'

            //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
            //'<td><img src=https://www.pythonanywhere.com/user/USUARIO/files/home/USUARIO/mysite/static/imagenes/' + Auto.imagen_url +' alt="Imagen del Auto" style="width: 100px;"></td>' + '<td align="right">' + Auto.proveedor + '</td>';

            '<td><img src=https://www.pythonanywhere.com/user/gaston2024/files/home/gaston2024/mysite/static/imagenes/' + Auto.imagen_url +' alt="Imagen del auto" style="width: 100px;"></td>';
            //Una vez que se crea la fila con el contenido del Auto, se agrega a la tabla utilizando el método appendChild del elemento tablaAutos.
            tablaAutos.appendChild(fila);
        }
    })

    //Captura y maneja errores, mostrando una alerta en caso de error al obtener los Autos.
    .catch(function (error) {
        // Código para manejar errores
        alert('Error al obtener los autos.');
    });


