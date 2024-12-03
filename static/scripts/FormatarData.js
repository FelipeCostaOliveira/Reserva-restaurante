$(document).ready(function () {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('data');
    if (dateInput) {
        dateInput.setAttribute('min', today);
    } else {
        console.warn('Elemento com id "data" não encontrado.');
    }
});
