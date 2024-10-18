$(document).ready(function () {
    // Função para carregar e mostrar a imagem selecionada
    function loadFile(event, labelId) {
        var image = $('<img>', {
            src: URL.createObjectURL(event.target.files[0]),
            class: 'w-24 h-24 rounded-full object-cover'
        });

        // Substitui o conteúdo do label pelo elemento de imagem
        var label = $('label[for="' + labelId + '"]');
        label.empty(); // Limpa o conteúdo atual
        label.append(image); // Adiciona a imagem
    }

    // Ligar a função ao input para todos os campos de upload
    $('input[type="file"]').on('change', function(event) {
        var labelId = $(this).attr('id'); // Pega o id do input
        loadFile(event, labelId); // Chama a função passando o id correto
    });
    
});
