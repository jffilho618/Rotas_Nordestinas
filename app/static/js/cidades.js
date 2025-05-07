// Função para carregar templates reutilizáveis usando fetch
function loadTemplate(elementId, templatePath) {
    fetch(templatePath)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            const element = document.getElementById(elementId);
            if (element) {
                element.innerHTML = html;
            } else {
                console.error(`Elemento com ID ${elementId} não encontrado`);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar template:', error);
        });
}

// Carregar o header, footer e feedback
document.addEventListener('DOMContentLoaded', () => {
    // Usar a rota do Flask para carregar os componentes
    loadTemplate('header', '/components/header.html');
    loadTemplate('footer', '/components/footer.html');
});