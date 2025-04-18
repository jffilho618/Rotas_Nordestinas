function showToast(message, type = 'success') {
    const container = document.getElementById('rotas-toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `rotas-toast ${type}`;
    
    const icon = document.createElement('img');
    icon.className = 'rotas-toast-icon';
    icon.src = type === 'success' 
        ? '/static/images/icons/success.svg'
        : '/static/images/icons/error.svg';
    icon.alt = type === 'success' ? 'Sucesso' : 'Erro';

    const messageDiv = document.createElement('div');
    messageDiv.className = 'rotas-toast-message';
    messageDiv.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(messageDiv);
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    setTimeout(() => {
        toast.style.animation = 'rotasFadeOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function showSuccessToast(message) {
    showToast(message, 'success');
}

function showErrorToast(message) {
    showToast(message, 'error');
}