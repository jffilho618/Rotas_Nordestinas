const idExtantModals = [
    'login', 
    'forgotPassword', 
    'informarCodigo', 
    'alterarSenha', 
    'sucesso',
    'cadastro1',
    'cadastro2',
    'cadastro3',
    'cadastro4',
    'cadastro5',
    'cadastro_C1',
    'cadastro_C2',
    'cadastro_C3',
    'cadastro_C4',
    'cadastro_C5',
    'cadastro_C6',
];

function openModal(modalPath) {
    const modalId = modalPath.split('/').pop();
    const activeModal = document.getElementById(modalId);
    const overlay = document.getElementById('overlay');

    overlay.classList.add('active');

    const currentModal = document.querySelector('.modal.show');
    if (currentModal) {
        currentModal.classList.remove('show');
    }

    if (activeModal) {
        activeModal.classList.add('show');
    } else {
        fetch(`/modais/${modalPath}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar o modal: ${modalPath}`);
                }
                return response.text();
            })
            .then(data => {
                const modalContainer = document.createElement('div');
                modalContainer.innerHTML = data;
                document.body.appendChild(modalContainer);

                const newModal = document.getElementById(modalId);
                if (newModal) {
                    newModal.classList.add('show');
                }

                // Lógica para cadastro_C5
                if (modalId === 'cadastro_C5') {
                    const form = document.getElementById('cadastroForm_C5');
                    if (form) {
                        form.addEventListener('submit', function(event) {
                            event.preventDefault();
                            if (form.checkValidity()) {
                                showSuccessToast('Cadastro de colaborador concluído com sucesso!');
                                setTimeout(() => closeModal('cadastro_C5'), 3000);
                            } else {
                                showErrorToast('Por favor, aceite os termos e condições.');
                            }
                        });
                    }
                }

                // Lógica para cadastro4
                if (modalId === 'cadastro4') {
                    const form = document.getElementById('cadastroForm4');
                    if (form) {
                        form.addEventListener('submit', function(event) {
                            event.preventDefault();
                            if (form.checkValidity()) {
                                showSuccessToast('Cadastro concluído com sucesso!');
                                setTimeout(() => closeModal('cadastro4'), 3000);
                            } else {
                                showErrorToast('Por favor, aceite os termos e condições.');
                            }
                        });
                    }
                }

                // Lógica para login
                if (modalId === 'login') {
                    const form = document.getElementById('loginForm');
                    if (form) {
                        form.addEventListener('submit', async function(event) {
                            event.preventDefault();
                            if (form.checkValidity()) {
                                const formData = new FormData(form);
                
                                try {
                                    const response = await fetch('/login', {
                                        method: 'POST',
                                        body: formData
                                    });
                
                                    const result = await response.json();
                
                                    if (result.success) {
                                        showSuccessToast(result.mensagem);
                                        setTimeout(() => {
                                            closeModal('login');
                                            window.location.href = '/main'; // Redireciona para a rota principal
                                        }, 2000);
                                    } else {
                                        showErrorToast(result.mensagem);
                                    }
                                } catch (error) {
                                    console.error('Erro na requisição de login:', error);
                                    showErrorToast('Erro ao tentar logar. Tente novamente.');
                                }
                
                            } else {
                                showErrorToast('Por favor, preencha todos os campos.');
                            }
                        });
                    }
                }
                
            })
            .catch(error => console.error(error));
    }
}

function closeModal(modalId) {
    const overlay = document.getElementById('overlay');
    const modals = modalId
        ? [document.getElementById(modalId)]
        : document.querySelectorAll('.modal.show');

    modals.forEach(modal => {
        if (modal) {
            modal.classList.remove('show');
        }
    });

    setTimeout(() => {
        if (!document.querySelector('.modal.show')) {
            overlay.classList.remove('active');
        }
    }, 300);
}

document.addEventListener('click', (e) => {
    const modal = e.target.closest('.modal');
    const overlayClicked = e.target.id === 'overlay';
    if (!modal && overlayClicked) {
        closeModal();
    }
});