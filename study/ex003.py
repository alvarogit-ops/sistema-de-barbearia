#Qual serviço mais caro e o mais barato?
#Qual serviço mais rápido e mais lento?
# Qual o mais equilibrado?

lista = []
n = int(input("Quantos serviços deseja cadastrar? "))

if n == 0:
    print("É mesmo? ")

for s in range(1, n + 1):
    print(f"-----Serviço {s}-----")
    servico = str(input(f"Nome do serviço: "))
    preco = float(input("Preço (R$): "))
    duracao = float(input("Duração (min): "))


    print(f"\033[32mServiço {servico} cadastrado com sucesso!\033[m")
    servicos = [servico, preco, duracao]
    lista.append(servicos)


print(f"Foram {len(lista)} serviços cadastrados: ") #se s fosse 0 aí n faz sentido

for servico in lista:
    print(servico)
    #remover cochetes e virgulas
