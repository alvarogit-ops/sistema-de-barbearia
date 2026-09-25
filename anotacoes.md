## Documentações utilizadas

* `Bootstrap 5.3 - Getting Started: JavaScript`
* `Bootstrap 5.3 - Collapse`
* `Bootstrap 5.3 - Color modes`
* `MDN - Window: matchMedia() method`
* `Django Project - Using the Django authentication system`

## O que cada código representa

### Setup

#### Navbar e navegação

* `navbar-expand-lg` — controla a partir de qual tamanho de tela a navbar fica expandida.
* `navbar-toggler` — representa o botão do menu em telas menores.
* `data-bs-toggle="collapse"` — utiliza o sistema de `Collapse` do Bootstrap.
* `data-bs-target` — indica qual elemento será controlado pelo botão.
* `active` — classe do Bootstrap utilizada para indicar o item de navegação ativo.
* `request.resolver_match.url_name` — permite verificar o nome da URL atual no Django.

#### Tema claro/escuro

* `window.matchMedia('(prefers-color-scheme: dark)')` — verifica a preferência de tema do sistema.
* `.matches` — verifica se a condição da media query está sendo correspondida.
* `document.documentElement` — seleciona o elemento `<html>` da página.
* `setAttribute("data-bs-theme", "dark")` — define o modo de cor do Bootstrap no elemento `<html>`.
* `addEventListener("change", ...)` — permite reagir quando a preferência de tema do sistema muda.

#### Manipulação do DOM

* `document.querySelector()` — seleciona um elemento do documento utilizando um seletor CSS.
* `document.getElementById()` — seleciona um elemento do documento pelo seu `id`.
* `.src` — permite acessar ou alterar o endereço da imagem de um elemento `<img>`.
