import math
import os

class Producto:
    def __init__(self, nombre, precio, cantidad):
        """
        Inicializa un objeto Producto con el nombre, precio y cantidad proporcionados.

        Args:
            nombre (str): El nombre del producto.
            precio (float): El precio del producto.
            cantidad (int): La cantidad del producto.

        Raises:
            ValueError: Si el nombre está vacío, el precio no es un número mayor o igual que cero, o la cantidad no es un número entero mayor o igual que cero.
        """

        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if nombre.lower() == "none":
            raise ValueError("El nombre no puede ser 'None'.")

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.") from None

        if not math.isfinite(precio) or precio < 0:
            raise ValueError("El precio debe ser un número finito mayor o igual que cero.")

        self.nombre = nombre
        self.precio = precio
        self.cantidad = _parse_cantidad(cantidad)

    def actualizar_precio(self, nuevo_precio):
        """
        Actualiza el precio del producto con el nuevo precio proporcionado.

        Args:
            nuevo_precio (float): El nuevo precio del producto.

        Raises:
            ValueError: Si el nuevo precio no es un número válido, finito o mayor o igual que cero.
        """
        try:
            nuevo_precio = float(nuevo_precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.") from None

        if not math.isfinite(nuevo_precio) or nuevo_precio < 0:
            raise ValueError("El precio debe ser un número finito mayor o igual que cero.")

        self.precio = nuevo_precio

    def actualizar_cantidad(self, nueva_cantidad):
        """
        Actualiza la cantidad del producto con la nueva cantidad proporcionada.

        Args:
            nueva_cantidad (int): La nueva cantidad del producto.

        Raises:
            ValueError: Si la nueva cantidad no es un número entero mayor o igual que cero.
        """
        self.cantidad = _parse_cantidad(nueva_cantidad)

    def calcular_valor_total(self):
        return self.precio * self.cantidad

    def __str__(self):
        return (
            f"{self.nombre} | Precio: ${self.precio:.2f} | "
            f"Cantidad: {self.cantidad} | Total: ${self.calcular_valor_total():.2f}"
        )


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar objetos de tipo Producto.")

        if self.buscar_producto(producto.nombre) is not None:
            raise ValueError(f"Ya existe un producto con el nombre '{producto.nombre}'.")

        self.productos.append(producto)

    def buscar_producto(self, nombre):
        nombre = str(nombre).strip().lower()
        return next((p for p in self.productos if p.nombre.lower() == nombre), None)

    def calcular_valor_inventario(self):
        return sum(producto.calcular_valor_total() for producto in self.productos)

    def listar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
            return

        print("\n--- Productos en el inventario ---")
        for i, producto in enumerate(self.productos, start=1):
            print(f"{i}. {producto}")

def _parse_cantidad(cantidad):
    if isinstance(cantidad, bool):
        raise ValueError("La cantidad debe ser un número entero válido.")

    try:
        valor = float(cantidad)
    except (TypeError, ValueError):
        raise ValueError("La cantidad debe ser un número entero válido.") from None

    if not math.isfinite(valor) or not valor.is_integer():
        raise ValueError("La cantidad debe ser un número entero válido.")

    cantidad = int(valor)
    if cantidad < 0:
        raise ValueError("La cantidad debe ser mayor o igual a cero.")

    return cantidad

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPresione Enter para continuar...")

def opcion_agregar(inventario):
    while True:
        nombre = input("Nombre del producto (o 'q' para el menú): ").strip()
        if nombre.lower() == "q":
            return
        if not nombre:
            print("El nombre no puede estar vacío. Intente nuevamente.")
            continue
        if nombre.lower() == "none":
            print("El nombre no puede ser 'None'. Intente nuevamente.")
            continue
        if inventario.buscar_producto(nombre) is not None:
            print(f"Ya existe un producto con el nombre '{nombre}'. Intente con otro.")
            continue
        break

    while True:
        precio_ingresado = input("Precio (o 'q' para el menú): ").strip()
        if precio_ingresado.lower() == "q":
            return
        try:
            precio = float(precio_ingresado)
        except ValueError:
            print("El precio debe ser un número válido. Intente nuevamente.")
            continue
        if not math.isfinite(precio) or precio < 0:
            print("El precio debe ser un número finito mayor o igual que cero. Intente nuevamente.")
            continue
        break

    while True:
        cantidad_ingresada = input("Cantidad (o 'q' para el menú): ").strip()
        if cantidad_ingresada.lower() == "q":
            return
        try:
            cantidad = _parse_cantidad(cantidad_ingresada)
            break
        except ValueError as e:
            print(f"{e} Intente nuevamente.")

    try:
        producto = Producto(nombre, precio, cantidad)
        inventario.agregar_producto(producto)
        print(f"Producto '{producto.nombre}' agregado correctamente.")
    except (ValueError, TypeError) as e:
        print(f"Error al agregar producto: {e}")

def opcion_buscar(inventario):
    while True:
        try:
            nombre = input("Nombre del producto a buscar (o 'q' para el menú): ").strip()
            if nombre.lower() == "q":
                return

            if not nombre:
                raise ValueError("El nombre no puede estar vacío.")

            producto = inventario.buscar_producto(nombre)
            if producto is None:
                print(f"Producto '{nombre}' no encontrado.")
                print("Intente nuevamente o escriba 'q'.")
                continue

            print(f"Producto encontrado: {producto}")
            return
        except ValueError as e:
            print(f"Error en la búsqueda: {e}")
            print("Intente nuevamente o escriba 'q'.")


def menu_principal(inventario):
    while True:
        limpiar_pantalla()
        print("===== Sistema de Inventario =====")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Calcular valor total del inventario")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()


        limpiar_pantalla()
        if opcion == "1":
            opcion_agregar(inventario)
            pausar()

        elif opcion == "2":
            opcion_buscar(inventario)
            pausar()

        elif opcion == "3":
            inventario.listar_productos()
            pausar()

        elif opcion == "4":
            try:
                total = inventario.calcular_valor_inventario()
                print(f"Valor total del inventario: ${total:.2f}")
            except Exception as e:
                print(f"Error al calcular el valor del inventario: {e}")
            pausar()

        elif opcion == "5":
            print("¡Hasta luego!")
            pausar()
            break

        else:
            print("Opción inválida. Intente nuevamente.")
            pausar()


if __name__ == "__main__":
    inventario = Inventario()
    menu_principal(inventario)
