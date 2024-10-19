function confirmDelete(restauranteId) {
    const confirmation = confirm("Tem certeza que deseja deletar este restaurante?");
    if (confirmation) {
        // Se o usuário confirmar, redireciona para a rota de deleção com o ID do restaurante
        window.location.href = `/deletarRestaurante?restaurante_id=${restauranteId}`;
    }
}