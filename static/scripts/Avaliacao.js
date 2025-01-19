$(document).ready(function () {
    let currentRating = 0; // Armazena a avaliação atual
  
    // Evento para destacar estrelas ao passar o mouse
    $("#star-rating .star").on("mouseover", function () {
      const rating = $(this).data("value");
      highlightStars(rating);
    });
  
    // Evento para definir a avaliação ao clicar
    $("#star-rating .star").on("click", function () {
      currentRating = $(this).data("value");
      $("#rating-result").text(`Avaliação: ${currentRating}`);
    });
  
    // Evento para resetar as estrelas ao sair com o mouse
    $("#star-rating .star").on("mouseout", function () {
      resetStars();
      if (currentRating > 0) {
        highlightStars(currentRating);
      }
    });
  
    // Função para destacar estrelas até o índice informado
    function highlightStars(rating) {
      $("#star-rating .star").each(function () {
        if ($(this).data("value") <= rating) {
          $(this).addClass("text-yellow-500");
        } else {
          $(this).removeClass("text-yellow-500");
        }
      });
    }
  
    // Função para resetar todas as estrelas
    function resetStars() {
      $("#star-rating .star").removeClass("text-yellow-500");
    }
  });