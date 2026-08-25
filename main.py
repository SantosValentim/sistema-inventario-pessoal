def registrar_produto ():
    nome = input("Insira o nome do produto: ")
    valor = float(input("Insira o valor do produto: "))
    numero_serie = int(input("Insira o número de série do produto: "))
    departamento = input("Insira o departamento do produto: ")
    print("Produto registrado com sucesso.\n"
          f"Nome:{nome}\n"
          f"Valor: {valor}\n"
          f"Número de série: {numero_serie}\n"
          f"Departamento: {departamento}\n")

def calculo ():
    print("Cálculo de Depreciação.\n")
    escolha = input("Digite: \n" 
    "1 - Para calcular a depreciação linear (DA) do produto \n"
    "2 - Para calcular o valor residual (VR) do produto \n" 
    "3 - Para calcular a vida útil (VU) do produto \n") 

    if escolha == "1":
        vi = float(input("Digite o valor inicial ou da aquisição do produto: "))
        vr = float(input("Digite o valor residual do produto: "))
        vu = int (input("Digite a vida útil do produto: ")) 

        if vu == 0:
            print("Erro: A vida útil não pode ser zero.\n")
            return
        da = (vi-vr)/vu
        print(f"A depreciação linear do produto é R$ {da:.2f}.")

    if escolha == "2":
        vi = float(input("Digite o valor inicial ou de aquisição do produto: "))
        da = float(input("Digite a depreciação linear do produto: "))
        vu = int (input("Digite a vida útil do produto: ")) 
        vr = vi - (da * vu)
        print(f"O valor residual do produto é R$ {vr:.2f}.")

    if escolha == "3":
        vi = float(input("Digite o valor inicial ou de aquisição do produto: "))
        vr = float(input("Digite o valor residual do produto: "))
        da = float(input("Digite a depreciação linear do produto: "))
        vu = (vi - vr)/da
        
        if da == 0:
            print ("Erro: A depreciação não pode ser zero. ")
            return
        
        if vu >= 2:
            print(f"A vida útil do produto é de aproximadamente {vu:.2f} anos.")
        else:
            print(f"A vida útil do produto é de aproximadamente {vu:.2f} ano.")

    else:
        print("Opção inválida!\n")

registrar_produto()
calculo()