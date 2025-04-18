document.addEventListener('DOMContentLoaded', () => {
    const suggestionForm = document.getElementById('suggestionForm');

    suggestionForm.addEventListener('submit', (event) => {
        event.preventDefault();
        if (suggestionForm.checkValidity()) {
            suggestionForm.style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';
            showSuccessToast('Sugestão enviada com sucesso!');
        } else {
            showErrorToast('Por favor, preencha todos os campos obrigatórios.');
        }
    });
});

function goToMainPage() {
    window.location.href = mainUrl; // Usar a variável global
}