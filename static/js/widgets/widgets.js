document.addEventListener("DOMContentLoaded", function () {
  // Función para manejar los clics en los marcadores
  function handleMarkerClick(rangeMarkers) {
    rangeMarkers.forEach(function (marker) {
      marker.addEventListener("click", function () {
        // Restablecer estilos en todos los marcadores
        rangeMarkers.forEach(function (otherMarker) {
          otherMarker.style.backgroundColor = "";
          otherMarker.style.color = "";
        });

        // Aplicar estilos al marcador clicado
        this.style.backgroundColor = "red";
        this.style.color = "white";

        // Actualizar el campo del formulario
        var inputId = this.getAttribute("for");
        var inputValue = this.getAttribute("nv-val");
        var input = document.getElementById(inputId);
        if (input) {
          input.value = inputValue;
        }
      });
    });
  }

  // Seleccionar y manejar clics para la primera clase de marcadores
  var rangeMarkers1 = document.querySelectorAll(".range-marker-recomendar_mitsubishi");
  handleMarkerClick(rangeMarkers1);

  // Seleccionar y manejar clics para la segunda clase de marcadores
  var rangeMarkers2 = document.querySelectorAll(".range-marker-calificacion_programacion_cita");
  handleMarkerClick(rangeMarkers2);

  // Seleccionar y manejar clics para la segunda clase de marcadores
  var rangeMarkers3 = document.querySelectorAll(".range-marker-calificacion_atencion_asesor");
  handleMarkerClick(rangeMarkers3);

  // Seleccionar y manejar clics para la segunda clase de marcadores
  var rangeMarkers4 = document.querySelectorAll(".range-marker-calificacion_instalaciones");
  handleMarkerClick(rangeMarkers4);

  // Seleccionar y manejar clics para la segunda clase de marcadores
  var rangeMarkers5 = document.querySelectorAll(".range-marker-calificacion_entrega_general");
  handleMarkerClick(rangeMarkers5);

  var rangeMarkers6 = document.querySelectorAll(".range-marker-calificacion_servicio_general");
  handleMarkerClick(rangeMarkers6);
});
