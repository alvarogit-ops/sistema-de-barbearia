
lista_clientes = [["João", 18, "Corte"],["José", 22, "Barba"],[ "Pietro", 16, "Corte"]]
qtd = 0
cliente = str(input("Pesquisar cliente: ")).strip().capitalize()
encontrado = False

while qtd < len(lista_clientes):
    #print(lista_clientes)
  
    if cliente == lista_clientes[qtd][0]:
        print(lista_clientes[qtd])
        encontrado = True
    qtd = qtd + 1 #se tiver antes, vai dar index out of range pq de 0,1,2 vai em 3 q n existe.
    break

if encontrado == False:
    print("Cliente não encontrado")
   
        
   
       