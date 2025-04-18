// Função para carregar templates reutilizáveis
function loadTemplate(elementId, templatePath) {
    fetch(templatePath)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        })
        .catch(error => console.error('Erro ao carregar template:', error));
}

// Carregar o header e footer
document.addEventListener('DOMContentLoaded', () => {
    loadTemplate('header', '/components/header.html');
    loadTemplate('footer', '/components/footer.html');
    loadTemplate('feedback-section', '/components/feedback.html');
});

document.addEventListener("DOMContentLoaded", () => {
    const backButton = document.getElementById("back-button");

    // Verifique se o botão existe para evitar erros
    if (backButton) {
        // Defina o destino desejado
        const specificPage = "../pernambuco/recife.html"; // Substitua pelo destino correto

        // Atualize o href do botão
        backButton.setAttribute("href", specificPage);
    }
});

const cityData = {
    recife: {
        name: "Recife",

        como_chegar: `
            <h1>Como Chegar a Recife</h1>
            <p>Recife possui um dos maiores aeroportos do Nordeste, o Aeroporto Internacional dos Guararapes...</p>
        `,

        atividades: `
            <h1>Atividades em Recife</h1>
            <ul>
                <li>Visitar o Instituto Ricardo Brennand</li>
                <li>Explorar o Bairro do Recife Antigo</li>
            </ul>
        `,

        dicas: `
            <h1>Dicas para sua viagem a Recife</h1>
            <p>Leve roupas leves e protetor solar, pois Recife é quente durante o ano todo.</p>
        `,

        points: [
            {
                name: "Casa Grande do Engenho das Dunas",
                description: "A casa-grande do Engenho Duas Unas localiza-se no Centro de Jaboatão, na Estrada da Luz, bairro de mesmo nome e às margens do Rio Duas Unas. Muito conhecida como 'casarão' pelo povo, sua arquitetura não deixa mentir sua idade: mais de 100 anos! Constitui-se em uma verdadeira relíquia dos tempos de outrora!",
                image: "/static/images/cidades/casa_grande_engenho_dunas.png"
            },
            {
                name: "Boa Viagem",
                description: "Quem viaja a lazer e quer aproveitar o mar deve visitar Boa Viagem durante a maré baixa para desfrutar das piscinas naturais formadas pelos arrecifes. Para quem está de carro, vale a pena explorar o litoral sul de Pernambuco e conhecer algumas das praias mais famosas do Brasil, como Carneiros e Porto de Galinhas.",
                image: "/static/images/cidades/boa_viagem.png"
            },
            {
                name: "Praia de Boa Viagem",
                description: "A Praia de Boa Viagem é a praia urbana mais famosa da cidade do Recife, capital do estado brasileiro de Pernambuco. Com aproximadamente oito quilômetros (8 km) de extensão, está situada no bairro homônimo, Zona Sul da capital pernambucana, delimitada pela Praia do Pina ao norte e pela Praia de Piedade ao sul. A praia tem águas cristalinas e esverdeadas com areia branca e fina.",
                image: "/static/images/cidades/praia_boa_viagem.png"
            }
        ]
    },
    salvador: {
        name: "Salvador",
        como_chegar: `
            <h1>Como Chegar a Salvador</h1>
            <p>Salvador é acessível por meio do Aeroporto Internacional Deputado Luís Eduardo Magalhães...</p>
        `,
        atividades: `
            <h1>Atividades em Salvador</h1>
            <ul>
                <li>Visitar o Pelourinho</li>
                <li>Subir no Elevador Lacerda</li>
            </ul>
        `,
        dicas: `
            <h1>Dicas para Salvador</h1>
            <p>Prove a culinária local, como acarajé e moqueca baiana.</p>
        `,
        pontos: [
            {
                name: "Pelourinho",
                description: "O coração cultural e histórico de Salvador...",
                image: "/images/cidades/pelourinho.png"
            }
        ]
    }
    // Adicione mais cidades aqui
};

const params = new URLSearchParams(window.location.search);
const cityKey = params.get("cidade") || "recife"; // Padrão: Recife

const city = cityData[cityKey];

if (city) {
    const contentDiv = document.getElementById("content");
    contentDiv.innerHTML = `
        <div class="container">
            <h1 class="cityName">${city.name}</h1>
            <h2 class="points-title">Pontos Turísticos:</h2>
            <div class="points-list">
                ${city.points
                    .map(point => `
                        <div class="group1">
                            <img class="point-image" src="${point.image}" alt="${point.name}">
                            
                            <div class="group2">    
                                <h3 class="point-name">${point.name}</h3>
                                <p class="point-description">${point.description}</p>
                            </div>
                        </div>
                    `)
                    .join('')}
            </div>
        </div>
    `;
} else {
    document.getElementById("content").innerHTML = "<p>Informações não disponíveis para esta cidade.</p>";
}
