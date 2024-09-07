#representar un ítem
class Item:
    def __init__(self, id_item, descripcion, volumen):
        self.id_item = id_item
        self.descripcion = descripcion
        self.volumen = volumen  # Volumen ocupado por el ítem en m³

    def __str__(self):
        return f"Item ID: {self.id_item}, Descripción: {self.descripcion}, Volumen: {self.volumen} m³"


# representar un almacén
class Almacen:
    def __init__(self, id_almacen, nombre, altura, anchura, largura):
        self.id_almacen = id_almacen
        self.nombre = nombre
        self.altura = altura
        self.anchura = anchura
        self.largura = largura
        self.capacidad_total = self.altura * self.anchura * self.largura  #Volumen total en m3
        self.capacidad_ocupada = 0
        self.items = []  #Items guardados

    def capacidad_disponible(self):
        #Calcula la capacidad disponible (teniendo en cuenta que debe quedar el 20% libre)
        return self.capacidad_total * 0.80 - self.capacidad_ocupada

    def agregar_item(self, item):
        if self.capacidad_disponible() >= item.volumen:
            self.items.append(item)
            self.capacidad_ocupada += item.volumen
            print(f"Item {item.descripcion} agregado al almacén {self.nombre}.")
        else:
            print(f"No hay suficiente espacio disponible en el almacén {self.nombre} para el item {item.descripcion}.")

    def retirar_item(self, id_item):
        for item in self.items:
            if item.id_item == id_item:
                self.items.remove(item)
                self.capacidad_ocupada -= item.volumen
                print(f"Item {item.descripcion} retirado del almacén {self.nombre}.")
                return
        print(f"Item con ID {id_item} no encontrado en el almacén {self.nombre}.")

    def mostrar_items(self):
        if not self.items:
            print(f"El almacén {self.nombre} no tiene ítems almacenados.")
        else:
            print(f"Ítems en el almacén {self.nombre}:")
            for item in self.items:
                print(item)

    def __str__(self):
        return f"Almacén ID: {self.id_almacen}, Nombre: {self.nombre}, Capacidad Total: {self.capacidad_total} m³, Capacidad Disponible: {self.capacidad_disponible()} m³"


#Gestionar los almacenes
class GestionAlmacenes:
    def __init__(self):
        self.almacenes = []

    def agregar_almacen(self, almacen):
        self.almacenes.append(almacen)
        print(f"Almacén {almacen.nombre} agregado.")

    def obtener_almacen_por_id(self, id_almacen):
        for almacen in self.almacenes:
            if almacen.id_almacen == id_almacen:
                return almacen
        print(f"Almacén con ID {id_almacen} no encontrado.")
        return None

    def mostrar_almacenes(self):
        if not self.almacenes:
            print("No hay almacenes registrados.")
        else:
            for almacen in self.almacenes:
                print(almacen)

    def mostrar_items_por_almacen(self, id_almacen):
        almacen = self.obtener_almacen_por_id(id_almacen)
        if almacen:
            almacen.mostrar_items()

    def mostrar_todos_los_items(self):
        if not self.almacenes:
            print("No hay ítems registrados en ningún almacén.")
        else:
            for almacen in self.almacenes:
                almacen.mostrar_items()

import os

#When limpiar consola
def limpiar_consola():
    if os.name == 'nt':  
        os.system('cls')



#Menu
def menu():
    gestion = GestionAlmacenes()

    #AAlmacenes
    gestion.agregar_almacen(Almacen(1, "Almacén Santo Domingo", 10, 20, 30))  #Altura,Anchura,Largo
    gestion.agregar_almacen(Almacen(2, "Almacén Santiago", 8, 15, 25))  

    while True:
        limpiar_consola()  #Opciones menu
        print("\n--- Menú de Gestión de Almacenes ---")
        print("1. Ver todos los almacenes")
        print("2. Ver ítems en un almacén específico")
        print("3. Agregar un ítem a un almacén")
        print("4. Eliminar un ítem de un almacén")
        print("5. Ver todos los ítems en todos los almacenes")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        limpiar_consola()  #When limpiar consola parte 2

        if opcion == '1':
            gestion.mostrar_almacenes()

        elif opcion == '2':
            id_almacen = int(input("Ingrese el ID del almacén: "))
            gestion.mostrar_items_por_almacen(id_almacen)

        elif opcion == '3':
            id_almacen = int(input("Ingrese el ID del almacén: "))
            almacen = gestion.obtener_almacen_por_id(id_almacen)
            if almacen:
                id_item = int(input("Ingrese el ID del ítem: "))
                descripcion = input("Ingrese la descripción del ítem: ")
                volumen = float(input("Ingrese el volumen del ítem (en metros cúbicos): "))
                item = Item(id_item, descripcion, volumen)
                almacen.agregar_item(item)

        elif opcion == '4':
            id_almacen = int(input("Ingrese el ID del almacén: "))
            almacen = gestion.obtener_almacen_por_id(id_almacen)
            if almacen:
                id_item = int(input("Ingrese el ID del ítem a eliminar: "))
                almacen.retirar_item(id_item)

        elif opcion == '5':
            gestion.mostrar_todos_los_items()

        elif opcion == '6':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

        input("\nPresione Enter para continuar...")
menu()
