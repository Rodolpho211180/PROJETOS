const api = "/api/favoritos";

async function carregar() {

    const resposta = await fetch(api);
    const favoritos = await resposta.json();

    const dashboard = document.getElementById("dashboard");

    dashboard.innerHTML = "";

    favoritos.forEach(f => {

        const dominio = new URL(f.url).hostname;
        const favicon =
            "https://www.google.com/s2/favicons?sz=128&domain=" + dominio;

        dashboard.innerHTML += `
            <div class="card">

                <img src="${favicon}">

                <h3>${f.nome}</h3>

                <p>${f.grupo}</p>

                <a href="${f.url}" target="_blank">
                    ${f.url}
                </a>

                <div class="acoes">

                    <button onclick="window.open('${f.url}','_blank')">
                        Abrir
                    </button>

                    <button onclick="remover(${f.id})">
                        Remover
                    </button>

                </div>

            </div>
        `;

    });

}

async function adicionar(){

    const nome = document.getElementById("nome").value;
    const url = document.getElementById("url").value;
    const grupo = document.getElementById("grupo").value;

    await fetch(api,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            nome,
            url,
            grupo
        })
    });

    carregar();
}

async function remover(id){

    await fetch(api + "/" + id,{
        method:"DELETE"
    });

    carregar();
}

window.onload = carregar;