const temaEscuro = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (temaEscuro) {
        document.body.classList.add('dark');
}
