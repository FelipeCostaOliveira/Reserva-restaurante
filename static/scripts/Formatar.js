$(document).ready(function(){
    document.getElementById('tel').addEventListener('input', function(e) {
        var telInput = e.target;
        var telValue = telInput.value.replace(/\D/g, '');  // Remove qualquer caractere não numérico
        var formattedTel = '';
    
        if (telValue.length > 0) {
            formattedTel = '(' + telValue.substring(0, 2);  // Adiciona o DDD
        }
        if (telValue.length >= 3) {
            formattedTel += ') ' + telValue.substring(2, 3);  // Adiciona o primeiro dígito após o DDD
        }
        if (telValue.length >= 4) {
            formattedTel += ' ' + telValue.substring(3, 7);  // Adiciona os próximos 4 dígitos
        }
        if (telValue.length >= 8) {
            formattedTel += '-' + telValue.substring(7, 11);  // Adiciona os últimos 4 dígitos
        }
    
        // Atualiza o valor do campo com a formatação aplicada
        telInput.value = formattedTel;
    });
});
