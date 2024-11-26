class Produto:
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def atualizar_quantidade(self, quantidade_vendida):
        self.quantidade -= quantidade_vendida

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} - {self.quantidade} em estoque"


class Cliente:
    def __init__(self, nome, documento):
        self.nome = nome
        self.documento = documento
        self.carrinho = Carrinho()

    def adicionar_produto_ao_carrinho(self, produto, quantidade):
        self.carrinho.adicionar_produto(produto, quantidade)

    def visualizar_carrinho(self):
        return self.carrinho

    def __str__(self):
        return f"{self.nome} - {self.documento}"


class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_produto(self, produto, quantidade):
        if produto.quantidade >= quantidade:
            produto.atualizar_quantidade(quantidade)
            self.itens.append((produto, quantidade))
        else:
            print(f"Quantidade insuficiente de {produto.nome}. Estoque disponível: {produto.quantidade}")

    def calcular_total(self):
        total = sum(produto.preco * quantidade for produto, quantidade in self.itens)
        return total

    def __str__(self):
        detalhes = "\n".join(
            [f"{produto.nome} - {quantidade} unidade(s) - R${produto.preco * quantidade:.2f}" for produto, quantidade in self.itens]
        )
        total = self.calcular_total()
        return f"Carrinho:\n{detalhes}\nTotal: R${total:.2f}"


class Supermercado:
    def __init__(self):
        self.produtos = []
        self.clientes = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def buscar_produto(self, nome):
        for produto in self.produtos:
            if produto.nome.lower() == nome.lower():
                return produto
        return None

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def realizar_venda(self, cliente):
        total = cliente.carrinho.calcular_total()
        print(f"\n{cliente.nome}, o total da sua compra é R${total:.2f}")
        print("Obrigado pela sua compra!")
        cliente.carrinho = Carrinho()  # Limpa o carrinho após a venda

    def visualizar_produtos(self):
        for produto in self.produtos:
            print(produto)


class Terminal:
    @staticmethod
    def mostrar_menu_principal():
        print("\nMENU PRINCIPAL")
        print("1 - Cadastrar cliente")
        print("2 - Adicionar produto")
        print("3 - Visualizar produtos")
        print("4 - Adicionar produto ao carrinho")
        print("5 - Finalizar compra")
        print("6 - Sair")
        return int(input("Escolha a sua opção: "))

    @staticmethod
    def mostrar_menu_busca_produto():
        nome = input("Digite o nome do produto: ")
        return nome

    @staticmethod
    def mostrar_menu_cliente():
        nome = input("Digite o nome do cliente: ")
        documento = input("Digite o CPF do cliente: ")
        return nome, documento

    @staticmethod
    def mostrar_quantidade():
        quantidade = int(input("Quantas unidades deseja adicionar? "))
        return quantidade


def main():
    supermercado = Supermercado()

    while True:
        opcao = Terminal.mostrar_menu_principal()

        if opcao == 1:
            nome_cliente, documento_cliente = Terminal.mostrar_menu_cliente()
            cliente = Cliente(nome_cliente, documento_cliente)
            supermercado.registrar_cliente(cliente)
            print(f"Cliente {nome_cliente} registrado com sucesso!")

        elif opcao == 2:
            nome_produto = input("Digite o nome do produto: ")
            preco_produto = float(input("Digite o preço do produto: R$"))
            quantidade_produto = int(input("Digite a quantidade do produto: "))
            produto = Produto(nome_produto, preco_produto, quantidade_produto)
            supermercado.adicionar_produto(produto)
            print(f"Produto {nome_produto} adicionado ao estoque!")

        elif opcao == 3:
            print("\nProdutos disponíveis:")
            supermercado.visualizar_produtos()

        elif opcao == 4:
            nome_produto = Terminal.mostrar_menu_busca_produto()
            produto = supermercado.buscar_produto(nome_produto)

            if produto:
                quantidade = Terminal.mostrar_quantidade()
                if quantidade <= produto.quantidade:
                    cliente_nome = input("Digite o nome do cliente para adicionar ao carrinho: ")
                    cliente_obj = next((c for c in supermercado.clientes if c.nome == cliente_nome), None)
                    if cliente_obj:
                        cliente_obj.adicionar_produto_ao_carrinho(produto, quantidade)
                        print(f"{quantidade} unidade(s) de {produto.nome} adicionada(s) ao carrinho de {cliente_nome}.")
                    else:
                        print("Cliente não encontrado!")
                else:
                    print(f"Estoque insuficiente! Temos apenas {produto.quantidade} unidades.")
            else:
                print("Produto não encontrado!")

        elif opcao == 5:
            nome_cliente = input("Digite o nome do cliente para finalizar a compra: ")
            cliente_obj = next((c for c in supermercado.clientes if c.nome == nome_cliente), None)

            if cliente_obj:
                supermercado.realizar_venda(cliente_obj)
            else:
                print("Cliente não encontrado!")

        elif opcao == 6:
            print("Saindo... Até logo!")
            break


if __name__ == "__main__":
    main()