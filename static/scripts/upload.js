$(document).ready(function () {
    // Função para carregar e mostrar a imagem selecionada
    function loadFile(event) {
        var image = $('<img>', {
            src: URL.createObjectURL(event.target.files[0]),
            class: 'w-24 h-24 rounded-full object-cover'
        });

        // Substitui o conteúdo do label pelo elemento de imagem
        var label = $('label[for="upload"]');
        label.empty(); // Limpa o conteúdo atual
        label.append(image); // Adiciona a imagem
    }

    // Ligar a função ao input
    $('#upload').on('change', function(event) {
        loadFile(event); // Chama a função quando o input mudar
    });
});

