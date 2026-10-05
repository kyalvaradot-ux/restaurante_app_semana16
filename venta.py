class Venta:
    def __init__(self, usuario_id, producto_codigo, cantidad):
        self.usuario_id = str(usuario_id)
        self.producto_codigo = str(producto_codigo)
        self.cantidad = int(cantidad)

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["usuario_id"], data["producto_codigo"], data["cantidad"])
