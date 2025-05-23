async function enviarPergunta() {
    const user_input = document.getElementById("user-input").value;
    const chatbox = document.getElementById("chat-box");
    const apiKey = 'AIzaSyAmgEdiDfplZqyS-hstOVhIFyISJZn_vso';
    const cx = '622515576b09346c5';

    if (user_input) {
        chatbox.innerHTML += `<div><strong>Você:</strong> ${user_input}</div>`;
        document.getElementById("user-input").value = "";

        let resposta;
        if (user_input.startsWith("wikipedia")) {
            const consulta = user_input.slice(10);
            resposta = await buscarWikipedia(consulta);
        } else if (user_input.startsWith("google")) {
            const consulta = user_input.slice(7);
            resposta = await buscarGoogle(consulta, apiKey, cx);
        } else {
            resposta = await interagir(user_input, apiKey, cx);
        }

        chatbox.innerHTML += `<div><strong>Bot:</strong> ${resposta}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}

async function interagir(user_input, apiKey, cx) {
    try {
        const response = await axios.get('/interagir', {
            params: {
                user_input: user_input,
                apiKey: apiKey,
                cx: cx
            }
        });
        return response.data;
    } catch (error) {
        console.error(error);
        return "Ocorreu um erro ao processar sua solicitação.";
    }
}

async function buscarWikipedia(consulta) {
    try {
        const response = await axios.get('/wikipedia', {
            params: {
                consulta: consulta
            }
        });
        return response.data;
    } catch (error) {
        return "Não foi possível encontrar informações sobre o tópico.";
    }
}

async function buscarGoogle(consulta, apiKey, cx) {
    try {
        const response = await axios.get('/google', {
            params: {
                consulta: consulta,
                apiKey: apiKey,
                cx: cx
            }
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar informações na web:", error);
        return "Ocorreu um erro ao buscar informações na web.";
    }
}
