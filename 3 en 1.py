import os
import subprocess

# Función para limpiar la pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para mostrar el menú con formato especial
def mostrar_menu():
    limpiar_pantalla()
    print("\033[91m" + "="*30 + "\033[0m")  # Línea roja
    print("\033[92m 6 \033[93m e \033[94m n \033[95m 1 \033[0m")  # Letras en colores diferentes
    print("\033[91m" + "="*30 + "\033[0m")  # Línea roja
    print("Seleccione un juego para comenzar:")
    print("1. Snake")
    print("2. Tres en Raya")
    print("3. Piedra, Papel o Tijera")
    print("4. Flappy bird")
    print("5. Space Invaders")
    print("6. Pac-Man")
    print("9. Salir")

# Función para ejecutar el juego Snake
def ejecutar_snake():
    print("Iniciando Snake...")
    subprocess.run(["python", "snake.py"])  # Ejecuta el archivo snake.py

# Función para ejecutar el juego Tres en Raya
def ejecutar_tres_en_raya():
    print("Iniciando Tres en Raya...")
    subprocess.run(["python", "Juego tres en Raya.py"])  # Ejecuta el archivo tres_en_raya.py

# Función para ejecutar el juego Piedra, Papel o Tijera
def ejecutar_piedra_papel_tijera():
    print("Iniciando Piedra, Papel o Tijera...")
    subprocess.run(["python", "Piedra papel tijera.py"])  # Ejecuta el archivo piedra_papel_tijera.py

def ejecutar_Flappy_bird():
    print("Iniciando Flappy Bird...")
    subprocess.run(["python", "Flappy bird.py"]) 

def ejecutar_Space_Invaders():
    print("Iniciando Space Invaders...")
    subprocess.run(["python", "Space Invaders.py"]) 

def ejecutar_Pac_Man():
    print("Iniciando Pac-Man...")
    subprocess.run(["python", "Pac-Man.py"]) 

# Función principal del menú
def menu_principal():
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de la opción: ")

        if opcion == "1":
            ejecutar_snake()
        elif opcion == "2":
            ejecutar_tres_en_raya()
        elif opcion == "3":
            ejecutar_piedra_papel_tijera()
        elif opcion == "4":
            ejecutar_Flappy_bird()
        elif opcion == "5":
            ejecutar_Space_Invaders()
        elif opcion == "6":
            ejecutar_Pac_Man()
        elif opcion == "9":
            print("Gracias por jugar. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
            input("Presione Enter para continuar...")

# Ejecutar el menú principal
menu_principal()
