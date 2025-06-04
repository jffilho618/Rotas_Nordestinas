// favoritos.js

// Dados das atividades/pontos turísticos
let atividadesData = {};

// Carrega os dados do JSON no HTML
document.addEventListener('DOMContentLoaded', function() {
    // Tenta carregar dados de atividades
    const atividadesScript = document.getElementById('atividades-data');
    if (atividadesScript) {
        atividadesData = JSON.parse(atividadesScript.textContent);
    }
    
    // Tenta carregar dados de pontos turísticos
    const pontosScript = document.getElementById('pontos-data');
    if (pontosScript) {
        const pontosData = JSON.parse(pontosScript.textContent);
        // Combina os dados
        atividadesData = { ...atividadesData, ...pontosData };
    }
    
    // Carrega o estado dos favoritos
    carregarEstadoFavoritos();
});

// Função para alternar favorito
async function toggleFavorite(element) {
    const itemId = element.getAttribute('data-item-id');
    const isFavorited = element.classList.contains('favorited');
    
    if (isFavorited) {
        // Remover dos favoritos
        await removerFavorito(itemId, element);
    } else {
        // Adicionar aos favoritos
        await adicionarFavorito(itemId, element);
    }
}

// Função para adicionar favorito
async function adicionarFavorito(itemId, element) {
    const itemData = atividadesData[itemId];
    
    if (!itemData) {
        console.error('Dados do item não encontrados:', itemId);
        return;
    }
    
    try {
        const response = await fetch('/api/favoritos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Se você estiver usando CSRF protection
            },
            body: JSON.stringify({
                item_id: itemData.id,
                nome: itemData.nome,
                descricao: itemData.descricao,
                imagem: itemData.imagem,
                tipo: itemData.tipo,
                cidade: itemData.cidade
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            element.classList.add('favorited');
            element.classList.remove('bx-star');
            element.classList.add('bxs-star');
            showToast('Adicionado aos favoritos!', 'success');
        } else {
            showToast(result.error || 'Erro ao adicionar favorito', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro de conexão', 'error');
    }
}

// Função para remover favorito
async function removerFavorito(itemId, element) {
    try {
        const response = await fetch(`/api/favoritos/${itemId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCSRFToken() // Se você estiver usando CSRF protection
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            element.classList.remove('favorited');
            element.classList.add('bx-star');
            element.classList.remove('bxs-star');
            showToast('Removido dos favoritos!', 'success');
        } else {
            showToast(result.error || 'Erro ao remover favorito', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showToast('Erro de conexão', 'error');
    }
}

// Função para carregar estado dos favoritos
async function carregarEstadoFavoritos() {
    try {
        const response = await fetch('/api/favoritos');
        const favoritos = await response.json();
        
        if (response.ok) {
            // Marcar itens como favoritados
            favoritos.forEach(favorito => {
                const element = document.querySelector(`[data-item-id="${favorito.item_id}"]`);
                if (element) {
                    element.classList.add('favorited');
                    element.classList.remove('bx-star');
                    element.classList.add('bxs-star');
                }
            });
        }
    } catch (error) {
        console.error('Erro ao carregar favoritos:', error);
    }
}

// Função para obter CSRF token (se necessário)
function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// Função para mostrar toast notifications
function showToast(message, type = 'info') {
    // Cria o elemento toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Adiciona estilos inline se não houver CSS
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 4px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        ${type === 'success' ? 'background-color: #10b981;' : 'background-color: #ef4444;'}
    `;
    
    document.body.appendChild(toast);
    
    // Remove após 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Adiciona estilos para as animações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); }
        to { transform: translateX(100%); }
    }
    
    .favorite-star {
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.2em;
    }
    
    .favorite-star:hover {
        transform: scale(1.1);
        color: #ffd700;
    }
    
    .favorite-star.favorited {
        color: #ffd700;
    }
`;
document.head.appendChild(style);