const temaEscuro = window.matchMedia('(prefers-color-scheme: dark)');

        let imagem = document.getElementById('imagem_logotipo')
        let logotipo_claro = document.querySelector(".imagem_logotipo_claro")
        let logotipo_escuro = document.querySelector('.imagem_logotipo_escuro')
        function aplicarTema(escuro) {
            document.documentElement.setAttribute(
                "data-bs-theme",
                escuro ? "dark": "light",
            );
        }

        function alterarLogotipo(escuro){
          imagem.src = escuro ? logotipo_escuro.src : logotipo_claro.src
        }

        alterarLogotipo(temaEscuro.matches)

        aplicarTema(temaEscuro.matches);

        temaEscuro.addEventListener("change", (evento) => {
            aplicarTema(evento.matches);
        });

        //vou selecionar a janela, não a nav
      

        let nav_landing_page = document.querySelector('nav')

        window.addEventListener('scroll', () => {
          if (window.scrollY > 120){
             nav_landing_page.classList.add('fundo-escuro-nav')
          }

          else{
            nav_landing_page.classList.remove('fundo-escuro-nav')
          }
        })