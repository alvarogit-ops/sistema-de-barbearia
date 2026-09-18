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
