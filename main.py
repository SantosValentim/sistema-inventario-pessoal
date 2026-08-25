def registrar_produto ():
    nome = input("Insira o nome do produto: ")
    valor = float(input("Insira o valor do produto: "))
    numero_serie = int(input("Insira o número de série do produto: "))
    departamento = input("Insira o departamento do produto: ")
    print(f"Produto registrado com sucesso.")

def depreciacao ():
    escolha = input("Digite: " \
    "1 - Para calcular a depreciação linear (DA) do produto " \
    "2 - Para calcular o valor residual (VR) do produto " \
    "3 - Para calcular a vida útil (VU) do produto ") 

    if escolha == "1":
        vi = float(input("Digite o valor inicial ou da aquisição do produto: "))
        vr = float(input("Digite o valor residual ou de sucata do produto: "))
        vu = int (input("Digite a vida útil do produto: ")) 
        da = (vi-vr)/vu

        print(f"A depreciação do produto é {da}%.")

registrar_produto()
depreciacao()