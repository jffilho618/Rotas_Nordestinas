function renderSidebar() {
    const optionsContainer = document.querySelector('#userSidebar .options-container');
    const bottomButtons = document.querySelector('#userSidebar .bottom-buttons');
    
    optionsContainer.innerHTML = isPro
        ? `
            <div class="option"><i class="bx bx-home"></i><span>Início</span></div>
            <div class="option"><i class="bx bx-search"></i><span>Buscar Destinos Avançado</span></div>
            <div class="option"><i class="bx bx-star"></i><span>Meus Favoritos</span></div>
            <div class="option" id="editProfileButton"><i class="bx bx-user"></i><span>Meu Perfil Personalizado</span></div>
            <div class="option" id="suggestionButton"><i class="bx bx-comment-detail"></i><span>Sugerir Rota Avançado</span></div>
            <div class="option"><i class="bx bx-list-ul"></i><span>Minhas Publicações</span></div>
            <div class="option"><i class="bx bx-bar-chart"></i><span>Estatísticas</span></div>
            <div class="option"><i class="bx bx-heart"></i><span>Avaliar Destinos</span></div>
        `
        : `
            <div class="option"><i class="bx bx-search"></i><span>Buscar Destinos</span></div>
            <div class="option"><i class="bx bx-star"></i><span>Meus Favoritos</span></div>
            <div class="option" id="editProfileButton"><i class="bx bx-user"></i><span>Meu Perfil</span></div>
            <div class="option" id="suggestionButton"><i class="bx bx-comment-detail"></i><span>Sugerir Rota</span></div>
            <div class="option"><i class="bx bx-list-ul"></i><span>Minhas Publicações</span></div>
            <div class="option"><i class="bx bx-heart"></i><span>Avaliar Destinos</span></div>
            <div class="option"><i class="bx bx-crown"></i><span>Tornar-se PRO</span></div>
        `;
}

document.addEventListener('DOMContentLoaded', () => {
    renderSidebar();

    // Selecionar elementos
    const menuButton = document.getElementById('menuButton');
    const closeButton = document.getElementById('closeButton');
    const userSidebar = document.getElementById('userSidebar');
    const userSidebarWrapper = document.getElementById('userSidebarWrapper');
    const editProfileButton = document.getElementById('editProfileButton');
    const suggestionButton = document.getElementById('suggestionButton');
    const options = document.querySelectorAll('#userSidebar .option');
    const supportButton = document.querySelector('#userSidebar .support-button');

    // Abrir sidebar do usuário
    menuButton.addEventListener('click', () => {
        userSidebarWrapper.classList.add('open');
        userSidebar.classList.add('open');
    });

    // Fechar sidebar do usuário
    closeButton.addEventListener('click', () => {
        userSidebarWrapper.classList.remove('open');
        userSidebar.classList.remove('open');
        showSuccessToast('Logout realizado com sucesso!');
    });

    // Fechar sidebar ao clicar fora
    userSidebarWrapper.addEventListener('click', (event) => {
        if (!userSidebar.contains(event.target)) {
            userSidebarWrapper.classList.remove('open');
            userSidebar.classList.remove('open');
        }
    });

    // Abrir sidebar de edição de perfil
    editProfileButton.addEventListener('click', () => {
        openSidebar('editProfileSidebar');
    });

    // Abrir sidebar de sugestão
    suggestionButton.addEventListener('click', () => {
        openSidebar('suggestionSidebar');
    });

    // Ações para outras opções
    options.forEach(option => {
        if (!option.id) { // Ignorar opções com ações específicas (editProfile, suggestion)
            option.addEventListener('click', () => {
                showSuccessToast(`${option.querySelector('span').textContent} selecionado!`);
            });
        }
    });

    // Ação para o botão Suporte
    supportButton.addEventListener('click', () => {
        showSuccessToast('Suporte selecionado!');
    });

    // Lógica do formulário de edição de perfil
    const editProfileForm = document.getElementById('editProfileForm');
    editProfileForm.addEventListener('submit', (event) => {
        event.preventDefault();
        if (editProfileForm.checkValidity()) {
            showSuccessToast('Perfil atualizado com sucesso!');
            setTimeout(() => closeSidebar('editProfileSidebar'), 2000);
        } else {
            showErrorToast('Por favor, preencha todos os campos obrigatórios.');
        }
    });

    // Lógica do formulário de sugestão
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

function openSidebar(id) {
    const sidebar = document.getElementById(id);
    if (sidebar && !sidebar.classList.contains('open')) {
        sidebar.classList.add('open');
    }
}

function closeSidebar(id) {
    const sidebar = document.getElementById(id);
    if (sidebar && sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
    }
}

function goToHomePage() {
    window.location.href = "{{ url_for('home') }}";
}