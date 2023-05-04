class Comanda:
    def __init__(self, idProduct, quantity, price):
        self.idProduct = idProduct
        self.quantity = quantity
        self.price = price

    def totalPrice(self):
        total = self.quantity * self.price
        print("total=" + str(total))
        return total
