import json
from pathlib import Path


class ArchivoServicio:
    def __init__(self, carpeta_datos=None):
        self.carpeta = Path(carpeta_datos) if carpeta_datos else Path(__file__).resolve().parent.parent / "datos"
        self.carpeta.mkdir(parents=True, exist_ok=True)

    def cargar(self, nombre, predeterminado=None):
        ruta = self.carpeta / nombre
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return [] if predeterminado is None else predeterminado
        except json.JSONDecodeError as exc:
            raise ValueError(f"El archivo {nombre} contiene JSON inválido.") from exc
        except PermissionError as exc:
            raise PermissionError(f"No hay permisos para leer {nombre}.") from exc

    def guardar(self, nombre, datos):
        ruta = self.carpeta / nombre
        try:
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
        except PermissionError as exc:
            raise PermissionError(f"No hay permisos para escribir {nombre}.") from exc
