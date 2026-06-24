document.addEventListener('DOMContentLoaded', () => {
    const formRegistro = document.getElementById('form-registro');

    if (formRegistro) {
        formRegistro.addEventListener('submit', function(event) {
            event.preventDefault();

            const passwordInput = formRegistro.querySelector('input[type="password"]');
            const password = passwordInput.value;
            const alerta = document.getElementById('js-alerta-registro');

            if (alerta)
                alerta.className = 'form-alerta';

            passwordInput.classList.remove('input-error');

            const regexPassword = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
            if (!regexPassword.test(password)) {
                if (alerta) {
                    alerta.textContent = 'La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.';
                    alerta.classList.add('alerta-error', 'is-visible');
                }
                passwordInput.classList.add('input-error');
                passwordInput.focus();
                return;
            }

            const datosParaEnviar = new FormData(formRegistro);
            const botonRegistro = formRegistro.querySelector('button[type="submit"]');
            botonRegistro.disabled = true;

            fetch('/registro/', {
                method: 'POST',
                body: datosParaEnviar,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json().then(data => {
                if (!response.ok) throw data;
                return data;
            }))
            .then(data => {
                botonRegistro.disabled = false;
                if (data.status === 'success') {
                    if (alerta) {
                        alerta.textContent = data.message;
                        alerta.classList.add('alerta-exito', 'is-visible');
                    }
                    setTimeout(() => {
                        window.location.href = '/validar-cuenta/';
                    }, 5000);
                }
            })
            .catch(errorData => {
                botonRegistro.disabled = false;
                if (alerta) {
                    alerta.textContent = errorData.message || 'Error al procesar los datos.';
                    alerta.classList.add('alerta-error', 'is-visible');
                }
            });
        });
    }
});