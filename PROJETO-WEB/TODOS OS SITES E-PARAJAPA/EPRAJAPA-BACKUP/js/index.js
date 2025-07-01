
const botoesCarrossel = document.querySelectorAll('.botao');

const imagens = document.querySelectorAll('.imagem');

botoesCarrossel.forEach((botao, indice) => {
    botao.addEventListener('click', () =>{

    destivarBotaoSelecionado();

        selecionarBotaoCarrocel(botao);
    
            esconderImagemAtiva();
        
                mostrarImagemDeFundo(indice);
    })
})
function mostrarImagemDeFundo(indice) {
    imagens[indice].classList.add('ativa');
}

function selecionarBotaoCarrocel(botao) {
    botao.classList.add('selecionado');
}

function esconderImagemAtiva() {
    const imagemAtiva = document.querySelector('.ativa');
    imagemAtiva.classList.remove('ativa');
}

function destivarBotaoSelecionado() {
    const botaoSelecionado = document.querySelector('.selecionado');
    botaoSelecionado.classList.remove('selecionado');
}

const imgs = document.getElementById("img");

const img = document.querySelectorAll("#img img");

let idx =0;

function carrosel(){
    idx++;
        if (idx > img.length - 1){

            idx = 0;
        }
}

 setInterval(carrosel, 7000);
