document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchForm').addEventListener('submit', function (event) {
        event.preventDefault(); 

        var numeroOrden = document.getElementById('numero_orden').value;
        var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        // Realizar la petición AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', getSurveyModalUrl, true);
        xhr.setRequestHeader('enctype', 'multipart/form-data');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);

                    if (response.modal_content) {

                        document.getElementById('modalBody').innerHTML = response.modal_content;

                        $('#surveyModal').modal('show');
                    } else {
                        console.error('Error al obtener la encuesta:', response.error);
                        alert('Ocurrió un error al obtener la encuesta.');
                    }
                } else {

                    console.error('Error al obtener la encuesta:', xhr.status);
                    alert('No se ha encontrado el número de encuesta\n\n Error:', xhr.status);
                }
            }
        };

        var formData = new FormData();
        formData.append('numero_orden', numeroOrden);

        console.log('Número de orden: ' + numeroOrden)
        console.log('Tipo: ' + typeof numeroOrden)
        xhr.send(formData);
    });
});

function descargarCSV() {

    var fechaInicio = document.getElementById('fecha_inicio').value;
    var fechaFin = document.getElementById('fecha_fin').value;
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    var params = new URLSearchParams();
    params.append('fecha_inicio', fechaInicio);
    params.append('fecha_fin', fechaFin);
    params.append('sucursal', sucursal);
    params.append('csrfmiddlewaretoken', csrfToken);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', downloadFilteredDataUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var blob = new Blob([xhr.response], { type: 'text/csv' });

                saveAs(blob, 'datos_encuestas.csv');
                alert('Archivo CSV descargado con éxito.');
            } else {

                console.error('Error al descargar el archivo CSV.');
                alert('Error al descargar el archivo CSV.');
            }
        }
    };
    xhr.send(params.toString()); 
}



function descargarPDF() {

    console.log('Accedio a la funcion descargarPDF')

    var numeroOrden2 = document.getElementById('numero_orden').value;
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    var params = new URLSearchParams();
    params.append('numero_orden', numeroOrden2);
    params.append('csrfmiddlewaretoken', csrfToken);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', dowloadOrderPDF, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var blob = new Blob([xhr.response], { type: 'application/pdf' });

                saveAs(blob, `Encuesta_orden_${numeroOrden2}.pdf`);
                alert('Archivo PDF descargado con éxito.');
            } else {

                alert('Error al descargar el archivo PDF.');
            }
        }
    };
    xhr.send(params.toString()); 
    
}