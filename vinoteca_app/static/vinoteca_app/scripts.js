document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('form-contacto');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const feedbackBox = document.getElementById('error-message');

    if (formulario) {
        formulario.addEventListener('submit', function(event) {
            event.preventDefault();
            if (feedbackBox) feedbackBox.style.display = 'none';
            const vNombre = validarNombre();
            const vEmail = validarEmail();
            const vMensaje = validarMensaje();

            if (!vNombre || !vEmail || !vMensaje) {
                return;
            }

            const datosParaEnviar = new FormData(formulario);
            const botonEnviar = formulario.querySelector('.btn-reserva');

            botonEnviar.disabled = true;

            fetch('/contacto/', {
                method: 'POST',
                body: datosParaEnviar,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) throw data;
                    botonEnviar.disabled = false;
                    return data;
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    mostrarFeedback(data.message, true);
                    formulario.reset();
                    botonEnviar.disabled = false;
                }
            })
            .catch(errorData => {
                let mensajeError = "El servidor rechazó los datos:\n";
                if (errorData && errorData.errors) {
                    for (let campo in errorData.errors) {
                        mensajeError += `- ${campo}: ${errorData.errors[campo]}\n`;
                    }
                } else {
                    mensajeError += "Hubo un error crítico en el servidor.";
                }
                mostrarFeedback(mensajeError, false);
                botonEnviar.disabled = false;
            });
        });
    }
});

// ==========================================================================
// FUNCIONES AUXILIARES DE VALIDACIÓN
// ==========================================================================
function validarNombre() {
    const name = document.getElementById('nombre');
    const errName = document.getElementById('error-message');
    if (name.value.trim() === '') {
        errName.textContent = 'Por favor, ingresá tu nombre.';
        errName.style.display = 'block';
        return false;
    }
    errName.style.display = 'none';
    return true;
}

function validarEmail() {
    const email = document.getElementById('email');
    const errEmail = document.getElementById('error-message');
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!regexEmail.test(email.value.trim())) {
        errEmail.textContent = 'Ingresá un correo electrónico válido.';
        errEmail.style.display = 'block';
        return false;
    }
    errEmail.style.display = 'none';
    return true;
}

function validarMensaje() {
    const message = document.getElementById('mensaje');
    const errMessage = document.getElementById('error-message');
    if (message.value.trim().length < 10) {
        errMessage.textContent = 'El mensaje debe tener al menos 10 caracteres.';
        errMessage.style.display = 'block';
        return false;
    }
    errMessage.style.display = 'none';
    return true;
}

function mostrarFeedback(mensaje, esExito) {
    const feedbackBox = document.getElementById('error-message');
    if (!feedbackBox) return;
    feedbackBox.textContent = mensaje;
    if (esExito) {
        feedbackBox.classList.remove('error-msg');
        feedbackBox.classList.add('ok-msg');
    } else {
        feedbackBox.classList.remove('ok-msg');
        feedbackBox.classList.add('error-msg');
    }
    feedbackBox.style.display = 'block';
    
    setTimeout(() => {
        feedbackBox.style.display = 'none';
        feedbackBox.textContent = '';
        feedbackBox.classList.remove('ok-msg', 'error-msg');
    }, 5000);
}