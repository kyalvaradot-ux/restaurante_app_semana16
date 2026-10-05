class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = str(codigo).strip()
        self.nombre = str(nombre).strip()
        self.precio = float(precio)
        self.stock = int(stock)

    def to_dict(self):
        return {"codigo": self.codigo, "nombre": self.nombre, "precio": self.precio, "stock": self.stock}

    @classmethod
    def from_dict(cls, data):
        return cls(data["codigo"], data["nombre"], data["precio"], data.get("stock", 0))
