let intervalId = null; // Para controlar o intervalo

// Função para buscar o valor do back-end
function fetchValue() {
    fetch('/get_text', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            // Atualiza o valor no front-end
            document.getElementById('transcription-box').innerText = data.valor;
        })
        .catch(error => console.error('Erro ao buscar valor:', error));
}

// Função que requisita o get_text a cada 1 segundo
function startFetching() {
    if (intervalId === null) {  // Verifica se o intervalo já está ativo
        alert("Iniciando Busca de Transcrição");
        intervalId = setInterval(fetchValue, 1000);
    }
}

// Função que para o intervalo de requisições
function stopFetching() {
    if (intervalId !== null) {
        clearInterval(intervalId); // Para o intervalo
        intervalId = null; // Reseta o intervalId
        alert("Busca de Transcrição Finalizada!");
    }
}

// Função para limpar o valor do back-end
function cleanText() {
    fetch('/clean_text')
        .then(response => response.json())
        .then(data => {
            // Atualiza o valor no front-end
            document.getElementById('transcription-box').innerText = data.valor;
            alert("O Texto da Transcrição foi limpo!");
        })
        .catch(error => console.error('Erro ao limpar valor:', error));
}

// Gera requisição de inicio de transcrição
function startTranscription() {
    fetch('/start_transcription', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Exibe mensagem de transcrição iniciada
            alert(data.message);
        })
        .catch(error => console.error('Erro ao iniciar transcrição:', error));
}

// Gera requisição que finaliza transcrição
function stopTranscription() {
    fetch('/stop_transcription', {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Exibe mensagem de transcrição finalizada
            alert(data.message);
        })
        .catch(error => console.error('Erro ao finalizar transcrição:', error));
}