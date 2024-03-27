document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("errorModal");
  const span = document.getElementsByClassName("close")[0];

  // Muestra el modal con el mensaje de error
  function showErrorModal(message) {
    document.getElementById("error-message").innerText = message;
    modal.style.display = "flex";
  }

  // Cierra el modal al hacer clic en la "x"
  span.onclick = function () {
    modal.style.display = "none";
  };

  // Cierra el modal si se hace clic fuera de él
  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  };

  // Agrega el evento de mostrar el modal al cargar la página
  const formErrors = "{{ form.errors }}";
  if (formErrors) {
    showErrorModal(formErrors);
  }
});
