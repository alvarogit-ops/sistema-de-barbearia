# Cadastrar barbeiros:

from datetime import date

ano_atual = date.today().year

n = int(input("Quantos barbeiros tem na barbearia? "))

lista_principal = []
for cont in range(1, n + 1):
    barbeiro = str(input(f"Digite o nome do {cont} barbeiro: "))
    ano_nasc = int(input("Qual ano de nascimento dele? "))

    idade = ano_atual - ano_nasc
    if idade > 18:
        barbeiros = [barbeiro, idade, ano_nasc]
        lista_principal.append(barbeiros)
    else:
        print("Barbeiro não pode ser menor de idade! ")
        break

    
for barbeiro in lista_principal:
    print(barbeiro)




# 