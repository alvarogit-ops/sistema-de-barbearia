const temaEscuro = window.matchMedia('(prefers-color-scheme: dark)');

function aplicarTema(escuro) {
    document.documentElement.classList.toggle('dark', escuro);
    if (document.body) {
        document.body.classList.toggle('dark', escuro);
    }
}

aplicarTema(temaEscuro.matches);
temaEscuro.addEventListener('change', (evento) => aplicarTema(evento.matches));
