var cadastroData = {};

function saveStep1() {
    cadastroData.nome = document.getElementById('nome').value;
    cadastroData.sobrenome = document.getElementById('sobrenome').value;
    cadastroData.email = document.getElementById('email').value;
    cadastroData.telefone = document.getElementById('telefone').value;
}

function saveStep3() {
    cadastroData.usuario = document.getElementById('usuario').value;
    cadastroData.senha = document.getElementById('password').value;
}

function finalizarCadastro() {
    console.log('Dados do cadastro:', cadastroData);
    fetch('/cadastro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cadastroData)
    })
    .then(response => {
        if (response.ok) {
            // talvez alguma resposta pode ser posta aqui
        } else {
            alert('Erro no cadastro.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro no envio do cadastro.');
    });
}
