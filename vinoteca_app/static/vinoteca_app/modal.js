document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('wine-modal');
    const closeBtn = document.getElementById('close-modal');
    const botones = document.querySelectorAll('.btn-detalle');
    const modalName = document.getElementById('modal-wine-name');
    const modalDesc = document.getElementById('modal-wine-desc');
    const modalPrice = document.getElementById('modal-wine-price');

    botones.forEach(boton => {
        boton.addEventListener('click', () => {
            const name = boton.getAttribute('data-name');
            const desc = boton.getAttribute('data-desc');
            const price = boton.getAttribute('data-price');

            modalName.textContent = name;
            modalDesc.textContent = desc;
            modalPrice.textContent = price;

            modal.classList.add('active');
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});