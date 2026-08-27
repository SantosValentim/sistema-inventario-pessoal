"""
Sistema de Inventário Pessoal
Funcionalidades:
- Cadastro, listagem, filtro, alteração e exclusão de produtos
- Cálculo de depreciação linear, valor residual e vida útil
- Persistência dos dados em arquivo JSON
"""

import json
import os
from datetime import datetime

class InventarioPessoal():
    """Classe principal do sistema de inventário."""
    
    def __init__(self):
        self.arquivo = "inventario.json"
        self.produtos = []
        self.carregar_dados()
        
    def carregar_dados(self):
        """Carrega os produtos salvos no arquivo JSON (se existir)."""
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                self.produtos = json.load(f)
            print("Dados carregados com sucesso!")
        else:
            self.produtos = []
            print("Nenhum arquivo encontrado. Começando com inventário vazio.")
    
    def salvar_dados(self):
        """Salva a lista de produtos no arquivo JSON."""
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.produtos, f, ensure_ascii=False, indent=4)
        print("Dados salvos com sucesso!")
    
    def escolha(self):
        """Exibe o menu principal e direciona para as funcionalidades."""
        while True:
            print("\nBem-vindo ao Inventário Pessoal!\n")
            escolha = input("Digite:\n"
                                "1 - Para registrar produto\n"
                                "2 - Para listar produtos\n"
                                "3 - Para filtrar os produtos\n"
                                "4 - Para calcular a depreciação, valor residual ou vida útil do produto\n"
                                "5 - Para alterar um produto\n"
                                "6 - Para excluir um produto\n"
                                "0 - Para sair\n").strip()
            if escolha == "0":
                print("\nSaindo do sistema...\n")
                break
            elif escolha == "1":
                self.registrar_produto()
            elif escolha == "2":
                self.listar_produto()
            elif escolha == "3":
                self.filtrar_produto()
            elif escolha == "4":
                self.calculo()
            elif escolha == "5":
                self.alterar_produto()
            elif escolha == "6":
                self.excluir_produto()
            else:
                print("Opção inválida!\n")
            
    def pedir_texto(self, mensagem):
        """Solicita um texto não vazio ao usuário."""
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("\nErro: Este campo não pode ficar em branco.\n")
    
    def pedir_valor(self, mensagem):
        """Solicita um valor numérico maior que zero."""
        while True:
            try:
                valor = float(input(mensagem).strip())
                if valor > 0:
                    return valor
                print("\nErro: O valor deve ser maior que zero.\n")
            except ValueError:
                print("\nErro: Digite um número válido.\n")
        
    def registrar_produto(self):
        """Cadastra um novo produto com validação dos campos."""
        print("\nREGISTRAR PRODUTO\n")
        nome = self.pedir_texto("Nome do produto: ")
        valor = self.pedir_valor("Valor do produto: R$ ")
        
        while True:
            numero_serie = self.pedir_texto("Número de série: ")
            if any(p["numero_serie"] == numero_serie for p in self.produtos):
                print("\nJá existe um produto com esse número de série.\n")
            else:
                break
        departamento = self.pedir_texto("Departamento/Local: ")
        data_registro = datetime.now().strftime("%d/%m/%Y às %H:%M:%S") # Pega a data e a hora do computador
            
        produto = {"nome": nome,
                "valor": valor,
                "numero_serie": numero_serie,
                "departamento": departamento,
                "data_registro": data_registro
                }
        
        self.produtos.append(produto)
        self.salvar_dados()
        
        print("\nProduto registrado com sucesso.\n"
            f"Nome: {nome}\n"
            f"Valor: R$ {valor:.2f}\n"
            f"Número de série: {numero_serie}\n"
            f"Departamento: {departamento}\n"
            f"Data: {data_registro}")
    
    
    def listar_produto(self):
        """Lista os produtos com diferentes opções de ordenação."""
        if not self.produtos:
            print("\nNão tem nenhum produto registrado ainda.\n")
            return
        
        # Menu de opções da lista
        while True:
            print("\nCOMO DESEJA LISTAR OS PRODUTOS? \n")
            escolha = input("Digite:\n"
                        "1 - Ordem de registro (primeiro ao último)\n"
                        "2 - Ordem de registro (último ao primeiro)\n"
                        "3 - Nome (A-Z)\n"
                        "4 - Nome (Z-A)\n"
                        "5 - Valor (menor ao maior)\n"
                        "6 - Valor (maior ao menor)\n"
                        "0 - Voltar\n").strip()
            
            if escolha == "0":
                return
            elif escolha == "1":
                produtos_ordenados = self.produtos
                titulo = "ORDEM DE REGISTRO (PRIMEIRO AO ÚLTIMO):"
            elif escolha == "2":
                produtos_ordenados = list(reversed(self.produtos))
                titulo = "ORDEM DE REGISTRO (ÚLTIMO AO PRIMEIRO):"
            elif escolha == "3":
                produtos_ordenados = sorted(self.produtos, key=lambda p: p["nome"].lower())
                titulo = "LISTA DE PRODUTOS DE A-Z:"
            elif escolha == "4":
                produtos_ordenados = sorted(self.produtos, key=lambda p: p["nome"].lower(), reverse=True)
                titulo = "LISTA DE PRODUTOS DE Z-A:"       
            elif escolha == "5":
                produtos_ordenados = sorted(self.produtos, key=lambda p: p["valor"])
                titulo = "LISTA DE PRODUTOS DO MENOR AO MAIOR VALOR:"
            elif escolha == "6":
                produtos_ordenados = sorted(self.produtos, key=lambda p: p["valor"], reverse=True)
                titulo = "LISTA DE PRODUTOS DO MAIOR AO MENOR VALOR:"
            else:
                print("Opção inválida!")
                return
            
            # Imprime a lista
            print(f"\n{titulo}\n")
            for i, p in enumerate(produtos_ordenados, start=1):
                print(f"\n[{i}] {p['nome']}\n"
                    f"    Valor: R$ {p['valor']:.2f}\n"
                    f"    Número de série: {p['numero_serie']}\n"
                    f"    Departamento: {p['departamento']}\n"
                    f"    Data: {p['data_registro']}\n")
            
    def filtrar_produto(self):
        """Filtra produtos por nome, departamento, valor, data ou hora."""
        if not self.produtos:
            print("\nNão tem nenhum produto registrado ainda.\n")
            return
        print("FILTRAR PRODUTOS\n"
              "(Deixe em branco e pressione ENTER para ignorar o critério)\n")
        
        nome = input("Insira o nome (ou parte dele): ").strip().lower()
        departamento = input("Insira o departamento (ou parte dele): ").strip().lower()
        valor_min = input("Valor mínimo: ").strip()
        valor_max = input("Valor máximo: ").strip()
        data = input("Data (dia/mês/ano): ").strip()
        hora = input("Hora (hora, hora:, hora:minuto ou hora:minuto:segundo): ").strip().lower()
        
        resultados = self.produtos.copy()
        
        if nome:
            resultados = [p for p in resultados if nome in p["nome"].lower()]
        
        if valor_min:
            try:
                valor_min = float(valor_min)
                if valor_min < 0:
                    print("Valor mínimo não pode ser menor que zero. Ignorando esse filtro.")
                else:
                    resultados = [p for p in resultados if p["valor"] >= valor_min]
            except ValueError:
                print("Valor mínimo inválido. Ignorando esse filtro.")
        if valor_max:
            try:
                valor_max = float(valor_max)
                if valor_max < 0:
                    print("Valor máximo não pode ser menor que zero. Ignorando esse filtro.")
                else:
                    resultados = [p for p in resultados if p["valor"] <= valor_max]
            except ValueError:
                print("Valor máximo inválido. Ignorando esse filtro.")
        if departamento:
            resultados = [p for p in resultados if departamento in p["departamento"].lower()]
        if data:
            resultados = [p for p in resultados if data in p["data_registro"].lower()]
        if hora:
            resultados = [p for p in resultados if hora in p["data_registro"].lower()]
          
        if not resultados:
            print("\n Nenhum produto encontrado. \n")
            return

        print(f"\n{len(resultados)} PRODUTO(S) ENCONTRADO(S)\n")
        for i, p in enumerate(resultados, start=1):
            print(f"\n[{i}] {p['nome']}\n"
                f"    Valor: R$ {p['valor']:.2f}\n"
                f"    Número de série: {p['numero_serie']}\n"
                f"    Departamento: {p['departamento']}\n"
                f"    Data: {p['data_registro']}\n")
                        
    def calculo(self):
        """Realiza cálculos de depreciação linear, valor residual e vida útil."""
        while True:
            print("Cálculo de Depreciação.\n")
            escolha = input("Digite: \n" 
                            "1 - Calcular a depreciação linear (DA) do produto \n"
                            "2 - Calcular o valor residual (VR) do produto \n" 
                            "3 - Calcular a vida útil (VU) do produto \n"
                            "0 - Voltar\n").strip() 

            if escolha == "0":
                return
            try:
                if escolha == "1":
                    # Fórmula: DA = (Valor Inicial - Valor Residual) / Vida Útil
                    vi = float(input("Valor inicial (aquisição): R$ "))
                    vr = float(input("Valor residual: R$ "))
                    vu = int(input("Vida útil (anos): ")) 

                    if vu == 0:
                        print("Erro: A vida útil não pode ser zero.\n")
                        return
                    
                    da = (vi-vr)/vu
                    print(f"\nA depreciação linear anual do produto é R$ {da:.2f}.\n")

                elif escolha == "2":
                    # Fórmula: VR = Valor Inicial - (Depreciação Anual × Vida Útil)
                    vi = float(input("Valor inicial (aquisição): R$ "))
                    da = float(input("Digite a depreciação linear do produto: R$ "))
                    vu = int(input("Vida útil (anos): "))
                    vr = vi - (da * vu)
                    print(f"O valor residual do produto é R$ {vr:.2f}.\n")

                elif escolha == "3":
                    # Fórmula: VU = (Valor Inicial - Valor Residual) / Depreciação Anual
                    vi = float(input("Valor inicial (aquisição): R$ "))
                    vr = float(input("Valor residual: R$ "))
                    da = float(input("Depreciação linear anual: R$ "))
                    
                    if da == 0:
                        print("Erro: A depreciação não pode ser zero.\n")
                        return

                    vu = (vi - vr)/da
                    ano_texto = "ano" if vu < 2 else "anos"
                    print(f"\nA vida útil é de aproximadamente {vu:.2f} {ano_texto}.\n")
                    
                else:
                    print("Opção inválida!\n")
            
            except ValueError:
                print("Erro: Digite apenas números válidos.\n")

    def alterar_produto(self):
        """Altera os dados de um produto existente a partir do número de série."""
        if not self.produtos:
            print("\nNão tem nenhum produto registrado ainda.\n")
            return
        
        serial = input("\nDigite o número de série do produto que deseja alterar: ").strip()
        produto_encontrado = None
        
        for p in self.produtos:
            if p["numero_serie"] == serial:
                produto_encontrado = p
                break
        if not produto_encontrado:
            print("\n Produto não encontrado.\n")
            return
        
        print(f"\n DADOS ATUAIS DO PRODUTO:\n"
                f"Nome: {produto_encontrado['nome']}\n"
                f"Valor: R$ {produto_encontrado['valor']:.2f}\n"
                f"Número de série: {produto_encontrado['numero_serie']}\n"
                f"Departamento: {produto_encontrado['departamento']}\n"
                f"Data: {produto_encontrado['data_registro']}\n")
        
        escolha = input("O que deseja alterar?\n"
                        "1 - Nome\n"
                        "2 - Valor\n"
                        "3 - Número de série\n"
                        "4 - Departamento\n"
                        "0 - Cancelar\n").strip()
        
        if escolha == "0":
            print("Alteração cancelada.\n")
            return
        
        if escolha == "1":
            produto_encontrado["nome"] = self.pedir_texto("Novo nome: ")
            self.salvar_dados()
            print("\nNome alterado com sucesso!\n")
                
        elif escolha == "2":
            produto_encontrado["valor"] = self.pedir_valor("Novo valor: R$ ")
            self.salvar_dados()
            print("Valor alterado com sucesso!\n")
                 
        elif escolha == "3":
            while True:
                novo_serial = self.pedir_texto("Novo número de série: ")
                # Verifica se o novo serial já pertence a outro produto
                if any(p["numero_serie"] == novo_serial for p in self.produtos if p != produto_encontrado):
                    print("Já existe um produto com esse número de série.\n")
                else:
                    produto_encontrado["numero_serie"] = novo_serial
                    self.salvar_dados()
                    print("Número de série alterado com sucesso!\n")
                    break
        
        elif escolha == "4":
            produto_encontrado["departamento"] = self.pedir_texto("Novo departamento: ")
            self.salvar_dados()
            print("Departamento alterado com sucesso!\n")
        
        else:
            print("Opção inválida\n")

    def excluir_produto(self):
        """Exclui um produto a partir do número de série (com confirmação)."""
        if not self.produtos:
            print("\nNão tem nenhum produto registrado ainda.\n")
            return
        
        serial = input("\nDigite o número de série do produto que deseja excluir: ").strip()
        produto_encontrado = None
        
        for p in self.produtos:
            if p["numero_serie"] == serial:
                produto_encontrado = p
                break
        if not produto_encontrado:
            print("\n Produto não encontrado.\n")
            return
        
        print(f"\nPRODUTO ENCONTRADO:\n"
                f"Nome: {produto_encontrado['nome']}\n"
                f"Valor: R$ {produto_encontrado['valor']:.2f}\n"
                f"Número de série: {produto_encontrado['numero_serie']}\n"
                f"Departamento: {produto_encontrado['departamento']}\n"
                f"Data: {produto_encontrado['data_registro']}\n")
        
        confirmacao = input("\nTem certeza que deseja excluir o produto? (S/N)\n").lower()
        if confirmacao == "s":
            self.produtos.remove(produto_encontrado)
            self.salvar_dados()
            print("\nProduto excluído com sucesso!\n")
        else:
            print("\nExclusão cancelada.\n")

# Inicia o sistema
meu_inventario = InventarioPessoal()
meu_inventario.escolha()