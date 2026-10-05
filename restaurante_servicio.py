from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self):
        self.archivo = ArchivoServicio()
        self.usuarios = [Usuario.from_dict(x) for x in self.archivo.cargar("usuarios.json")]
        self.productos = [Producto.from_dict(x) for x in self.archivo.cargar("productos.json")]
        self.ventas = [Venta.from_dict(x) for x in self.archivo.cargar("ventas.json")]
        self._asegurar_administrador()

    def _asegurar_administrador(self):
        if not self.usuarios:
            self.usuarios.append(Usuario("ADM001", "Administrador Principal", "admin", "admin123", "Administrador"))
            self.guardar_usuarios()

    def guardar_usuarios(self):
        self.archivo.guardar("usuarios.json", [u.to_dict() for u in self.usuarios])

    def guardar_productos(self):
        self.archivo.guardar("productos.json", [p.to_dict() for p in self.productos])

    def guardar_ventas(self):
        self.archivo.guardar("ventas.json", [v.to_dict() for v in self.ventas])

    def autenticar(self, usuario, contrasena):
        return next((u for u in self.usuarios if u.usuario == usuario and u.contrasena == contrasena), None)

    def buscar_usuario(self, identificacion):
        return next((u for u in self.usuarios if u.identificacion == identificacion), None)

    def buscar_producto(self, codigo):
        return next((p for p in self.productos if p.codigo == codigo), None)

    def registrar_usuario(self, usuario):
        if not usuario.identificacion or not usuario.nombre or not usuario.usuario or not usuario.contrasena:
            return False, "Complete todos los campos obligatorios."
        if self.buscar_usuario(usuario.identificacion):
            return False, "La identificación ya está registrada."
        if any(u.usuario == usuario.usuario for u in self.usuarios):
            return False, "El nombre de usuario ya está registrado."
        self.usuarios.append(usuario)
        self.guardar_usuarios()
        return True, "Usuario registrado correctamente."

    def actualizar_usuario(self, identificacion_original, datos):
        usuario = self.buscar_usuario(identificacion_original)
        if usuario is None:
            return False, "Seleccione un usuario válido."
        if datos.identificacion != identificacion_original and self.buscar_usuario(datos.identificacion):
            return False, "La nueva identificación ya existe."
        if usuario.rol == "Administrador" and datos.rol != "Administrador":
            return False, "La cuenta administrativa principal no puede cambiarse a otro rol."
        if usuario.rol != "Administrador" and datos.rol == "Administrador":
            return False, "No se pueden crear o convertir usuarios en Administrador desde esta gestión."
        for otro in self.usuarios:
            if otro is not usuario and otro.usuario == datos.usuario:
                return False, "El nombre de usuario ya está registrado."
        usuario.identificacion = datos.identificacion
        usuario.nombre = datos.nombre
        usuario.usuario = datos.usuario
        usuario.contrasena = datos.contrasena
        usuario.rol = datos.rol
        self.guardar_usuarios()
        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(self, identificacion, usuario_actual):
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False, "Seleccione un usuario válido."
        if usuario.identificacion == usuario_actual.identificacion:
            return False, "No puede eliminar la cuenta administrativa actualmente autenticada."
        if usuario.rol == "Administrador":
            return False, "La gestión permite administrar Empleados y Clientes."
        self.usuarios.remove(usuario)
        self.guardar_usuarios()
        return True, "Usuario eliminado correctamente."

    def registrar_producto(self, producto):
        if self.buscar_producto(producto.codigo):
            return False, "El código del producto ya existe."
        self.productos.append(producto)
        self.guardar_productos()
        return True, "Producto registrado correctamente."

    def vender_producto(self, codigo, identificacion, cantidad):
        usuario = self.buscar_usuario(identificacion)
        producto = self.buscar_producto(codigo)
        if usuario is None or producto is None:
            return False, "Usuario o producto no encontrado."
        if cantidad <= 0 or producto.stock < cantidad:
            return False, "Cantidad no válida o stock insuficiente."
        self.ventas.append(Venta(usuario.identificacion, producto.codigo, cantidad))
        producto.stock -= cantidad
        self.guardar_ventas()
        self.guardar_productos()
        return True, "Venta registrada correctamente."
