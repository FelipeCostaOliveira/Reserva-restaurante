const btn = document.getElementById("menubutton");
const menu = document.getElementById("menu");
const Minhaimagem = document.getElementById("imagem");

btn.addEventListener("click", () => {
    if (menu.classList.contains("hidden")) {
        menu.classList.toggle("hidden");
        menu.classList.add("bg-tranparent");
        Minhaimagem.src = "static/assets/cancel.svg";
    } else {
        menu.classList.add("hidden");
        Minhaimagem.src = "static/assets/menu.svg";
    }
});

$(document).ready(function() {
    // Obtém o caminho da URL atual
    var currentPath = window.location.pathname;
    
    // Itera sobre cada link no menu
    $('ul li a').each(function() {
        // Obtém o caminho do href do link
        var linkPath = $(this).attr('href');
        console.log(linkPath);
        
        // Verifica se o caminho do href corresponde ao caminho atual
        if (currentPath === linkPath) {
            $(this).parent().addClass('text-yellow-600');
        }
    });
});