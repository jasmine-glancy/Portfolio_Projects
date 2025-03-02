document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.color-container').forEach(container => {
        container.addEventListener('click', (evt) => {
            evt.currentTarget.classList.toggle('flip')
        });
    });
});

