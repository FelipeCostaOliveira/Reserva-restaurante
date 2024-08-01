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
