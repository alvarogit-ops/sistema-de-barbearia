## Improve Ui/Ux:

1. Adicionar favicon
2. Rota para logotipo: carregar apenas com static, sem a url



## Full Calendar

dataSelecionada
      ↓
elemento anteriormente selecionado

clicou em outra data
      ↓
remove "data-selecionada" do anterior
      ↓
encontra o novo elemento através de data-date
      ↓
adiciona "data-selecionada"
      ↓
dataSelecionada passa a ser o novo elemento