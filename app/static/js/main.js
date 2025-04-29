

document.addEventListener('DOMContentLoaded', () => {

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

    // Fechar sidebar com o botão "Sair"
    closeButton.addEventListener('click', () => {
        userSidebarWrapper.classList.remove('open');
        userSidebar.classList.remove('open');
        showSuccessToast('Logout realizado com sucesso!');
    });

    // Fechar sidebar com o "X"
    closeXButton.addEventListener('click', () => {
        userSidebarWrapper.classList.remove('open');
        userSidebar.classList.remove('open');
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