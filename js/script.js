let botaoTema = document.querySelector('#mudartema')
const body = document.body
const icone = document.querySelector('i')



botaoTema.addEventListener('click', () => {
    body.classList.toggle('dark')

    if (body.classList.contains('dark'))
        icone.classList.replace('bi-moon','bi-sun')
    else{
        icone.classList.replace('bi-sun', 'bi-moon')
    }
})