# Buscar clientes usando a busca binária

# não dá lista ordenada: lista_clientes = ["João", "Marcos", "Vitor", "Gabriel", "André"]
lista_clientes = ["João", "Marcos", "Vitor", "Gabriel", "André"]
lista_clientes = sorted(lista_clientes)
inicio = 0
fim = len(lista_clientes) - 1 #X len(lista_clientes - 1)
cliente = str(input("Pesquisar cliente: "))
encontrado = False
qtd = 0



while inicio <= fim:
    meio = (inicio + fim) // 2
    if cliente == lista_clientes[meio]:
        encontrado = True
        print(lista_clientes[meio]) #só imprime ao invés de encontrar e não fora
        break
    else:
        if cliente > lista_clientes[meio]: #se for só meio, fica: joão > 3?
            inicio = meio + 1
        else:
            fim = meio - 1
else:
    print("Não encontrado")
#sem break aqui