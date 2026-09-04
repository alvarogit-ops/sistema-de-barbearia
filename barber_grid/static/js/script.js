// Formatação de Data

const data = new Date();

let dias_fevereiro

let ano = data.getFullYear()


const dias_semana = [
     "Domingo",
     "Segunda-feira",
     "Terça-feira",
     "Quarta-feira",
     "Quinta-feira",
     "Sexta-feira",
     "Sábado"
]
const meses = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro",

]

const dia_Semana = dias_semana[data.getDay()]
const dia = String(data.getDate()).padStart(2, "0")
const mes = meses[data.getMonth()]



document.getElementById("data_exibicao").textContent = `${dia_Semana}, ${dia} de ${mes}`








//Tema Escuro
const temaEscuro = window.matchMedia('(prefers-color-scheme: dark)');



function aplicarTema(escuro) {
    if (document.body) {
        document.body.classList.toggle('dark', escuro);
    }

     document.documentElement.classList.toggle(
        "dark",
        escuro ? "dark" : "light"
    );

    
    document.documentElement.setAttribute(
        "data-bs-theme",
        tema
    );
}




aplicarTema(temaEscuro.matches);
temaEscuro.addEventListener('change', (evento) => aplicarTema(evento.matches));


// Ajax

function configurarFormularioAgendamento() {
    const formAgendamento =
        document.getElementById('form-agendamento');

    if (!formAgendamento) {
        return;
    }

    formAgendamento.addEventListener('submit', async function (event) {
        event.preventDefault();

        const botao =
            formAgendamento.querySelector('button[type="submit"]');

        botao.disabled = true;
        botao.textContent = 'Agendando...';

        const dados = new FormData(formAgendamento);

        try {
            const resposta = await fetch(window.location.href, {
                method: 'POST',
                body: dados,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const textoResposta = await resposta.text();

            console.log('Status:', resposta.status);
            console.log('Resposta do servidor:', textoResposta);

            const dadosResposta = JSON.parse(textoResposta);

            if (dadosResposta.sucesso) {
                document.getElementById(
                    'lista-agendamentos'
                ).innerHTML = dadosResposta.lista_html;

                formAgendamento.reset();

                alert(dadosResposta.mensagem);

            } else {
                const container =
                    document.createElement('div');

                container.innerHTML =
                    dadosResposta.form_html;

                const novoFormulario =
                    container.firstElementChild;

                formAgendamento.replaceWith(novoFormulario);

                configurarFormularioAgendamento();
            }

        } catch (erro) {
            console.error(
                'Erro ao realizar agendamento:',
                erro
            );

            alert(
                'Não foi possível realizar o agendamento. Tente novamente.'
            );

        } finally {
            const formularioAtual =
                document.getElementById('form-agendamento');

            if (formularioAtual) {
                const botaoAtual =
                    formularioAtual.querySelector(
                        'button[type="submit"]'
                    );

                if (botaoAtual) {
                    botaoAtual.disabled = false;
                    botaoAtual.textContent = 'Agendar';
                }
            }
        }
    });
}

configurarFormularioAgendamento();