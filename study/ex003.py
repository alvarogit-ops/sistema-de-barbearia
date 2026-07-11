#Qual serviço mais caro e o mais barato?
#Qual serviço mais rápido e mais lento?
# Qual o mais equilibrado?

maior_duracao = 0
menor_duracao = 0 #não existe duração menor que 0
mais_caro = 0
mais_barato = 0 #não existe valor de dinheiro menor que 0
servico_maior_duracao = ""
servico_menor_duracao = ""
servico_mais_caro = ""
servico_mais_barato = "" #*
servico_pior_beneficio = ""
servico_melhor_beneficio = ""
proporcao = 0
maior_proporcao = 0
menor_proporcao = 0

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

    #Mais caro e mais barato, maior duração e menor duração não pode ser uma única condição
    if s == 1:
        maior_duracao = duracao
        servico_maior_duracao = servico
        servico_mais_caro = servico
        mais_caro = preco
        maior_proporcao = proporcao
        servico_pior_beneficio = servico


    if duracao > maior_duracao and preco > mais_caro:
        maior_duracao = duracao
        mais_caro = preco
        servico_maior_duracao = servico
        servico_mais_caro = servico
      
    else:
        menor_duracao = duracao
        mais_barato = preco
        servico_menor_duracao = servico
        servico_mais_barato = servico
    
    #Como resolver maior proporção e menor proporção de tempo e dinheiro?
        if proporcao < maior_proporcao: 
            proporcao = preco / duracao #40/50 = 0.08
            servico_melhor_beneficio = servico
        else:
            pass


  




print(f"Foram {len(lista)} serviços cadastrados: ") #se s fosse 0 aí n faz sentido

for servico in lista:
    print(servico)
    #remover cochetes e virgulas

print(f"O serviço com  menor duração é {servico_menor_duracao} com {menor_duracao:.0f}min")
print(f"O serviço com maior duração é {servico_maior_duracao} com {maior_duracao:.0f}min")
print(f"O serviço mais caro é {servico_mais_caro} custando R${mais_caro:.0f}")
print(f"O serviço mais barato é {servico_mais_barato} custando R${mais_barato:.0f}")
print(f"O serviço com melhor custo benefício é {servico_melhor_beneficio}")