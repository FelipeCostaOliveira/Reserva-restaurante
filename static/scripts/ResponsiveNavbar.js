// Manipulação do menu e botão
const btn = document.getElementById("menubutton");
const menu = document.getElementById("menu");
const Minhaimagem = document.getElementById("imagem");

btn.addEventListener("click", () => {
    if (menu.classList.contains("hidden")) {
        menu.classList.remove("hidden");
        menu.classList.add("bg-transparent", "border-b-2", "border-[#E7A80E]");
        Minhaimagem.src = "static/assets/cancel.svg";
    } else {
        menu.classList.add("hidden");
        menu.classList.remove("bg-transparent", "border-b-2", "border-[#E7A80E]");
        Minhaimagem.src = "static/assets/menu.svg";
    }
});

// Detecção da URL atual e atualização do menu
$(document).ready(function() {
    // Obtém o caminho da URL atual sem parâmetros de consulta
    var currentPath = window.location.pathname;

    // Itera sobre cada link no menu
    $('ul li a').each(function() {
        var linkPath = $(this).attr('href');

        // Verifica se o caminho do href corresponde ao caminho atual
        if (currentPath === linkPath) {
            $(this).parent().addClass('text-yellow-400'); // Adiciona a classe ao item do menu correspondente
        }
    });
});
