// FUNÇÃO PARA MOSTRAR MENSAGEM 
function mostrarAlerta(mensagem, corTexto, corFundo, tempo) {
    // Criar um elemento de alerta
    let alerta = document.createElement("div");
    alerta.innerHTML = mensagem.replace(/\n/g, "<br>"); // Substituir '\n' por '<br>'
    alerta.style.position = "fixed";
    alerta.style.top = "40px";
    alerta.style.left = "50%";
    alerta.style.transform = "translateX(-50%)";
    alerta.style.backgroundColor = corFundo;
    alerta.style.fontSize = "20px";
    alerta.style.color = corTexto;
    alerta.style.padding = "20px";
    alerta.style.borderRadius = "10px";
    alerta.style.zIndex = "1000";
    
    document.body.appendChild(alerta);

    // Fechar o alerta após o tempo especificado
    setTimeout(() => {
        alerta.remove();
    }, tempo * 1000); // Converter segundos para milissegundos
}


// FUNÇÃO PARA COLOCAR O PONTO DO MILHAR NOS NUMEROS
function formatarMilhares(element) {
    let valor = element.value.replace(/[^0-9]/g, '');
    if (valor.length > 3) {
        valor = parseInt(valor).toLocaleString('pt-BR');
    }
    element.value = valor;
}

// FUNÇÃO PARA MOSTRAR CONTEÚDO DO FORMDATA
function mostrarFormData(fD) {
    for (let [key, value] of fD.entries()) {
        window.alert(`${key}: ${value}`);
    }
}

// FUNÇÃO PARA FAZER BEEP
function beepRon(duracao, frequencia, volume) {
    const contexto = new (window.AudioContext || window.webkitAudioContext)();
    const oscilador = contexto.createOscillator();
    const ganho = contexto.createGain();

    oscilador.type = "sine"; // Tipo de onda (pode testar "square", "triangle", "sawtooth")
    oscilador.frequency.value = frequencia; // Frequência do beep (440Hz é padrão)
    ganho.gain.value = volume;

    oscilador.connect(ganho);
    ganho.connect(contexto.destination);

    oscilador.start();
    setTimeout(() => {
        oscilador.stop();
        contexto.close();
    }, duracao); // Tempo em milissegundos (1s = 1000ms)
}
