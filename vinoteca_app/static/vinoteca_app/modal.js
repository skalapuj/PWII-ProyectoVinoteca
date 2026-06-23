document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('wine-modal');
    const closeBtn = document.getElementById('close-modal');
    const botones = document.querySelectorAll('.btn-detalle');

    // Elementos dentro del modal
    const modalName = document.getElementById('modal-wine-name');
    const modalDesc = document.getElementById('modal-wine-desc');
    const modalPrice = document.getElementById('modal-wine-price');

    // Asignar evento click a cada botón de "Ver Detalles"
    botones.forEach(boton => {
        boton.addEventListener('click', () => {
            // Capturar datos del botón clickeado
            const name = boton.getAttribute('data-name');
            const desc = boton.getAttribute('data-desc');
            const price = boton.getAttribute('data-price');

            // Inyectarlos en el modal
            modalName.textContent = name;
            modalDesc.textContent = desc;
            modalPrice.textContent = price;

            // Mostrar el modal
            modal.classList.add('active');
        });
    });

    // Cerrar con la X
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Cerrar si hacen click afuera de la cajita del modal
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});