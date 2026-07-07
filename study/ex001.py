lista = []
cont = 0
n = int(input("Quantos clientes quer cadastrar? "))

for l in range(n):
    cont = cont + 1
    cliente = str(input(f"Digite o nome do {cont}o cliente: "))
    print(f"Cliente cadastrado com sucesso: {cliente}")

    lista.append(cliente)
for cliente in lista:
    print(f"Clientes cadastrados: {cliente}")