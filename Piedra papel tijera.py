import tkinter as tk
import random
from PIL import Image, ImageTk
import time

# Función para obtener la elección de la computadora
def eleccion_computadora():
    opciones = ["piedra", "papel", "tijera"]
    return random.choice(opciones)

# Función para determinar el ganador
def determinar_ganador(jugador, computadora):
    if jugador == computadora:
        return "Empate"
    elif (jugador == "piedra" and computadora == "tijera") or \
         (jugador == "papel" and computadora == "piedra") or \
         (jugador == "tijera" and computadora == "papel"):
        return "Ganaste"
    else:
        return "Perdiste"

# Función para mostrar la imagen correspondiente a la jugada
def mostrar_imagen(jugador, computadora):
    global imagen_ganador, imagen_perdedor, imagen_jugador, imagen_computadora
    
    jugador_img = ImageTk.PhotoImage(Image.open(f"{jugador}.png").resize((150, 150)))
    computadora_img = ImageTk.PhotoImage(Image.open(f"{computadora}.png").resize((150, 150)))

    imagen_jugador.config(image=jugador_img)
    imagen_jugador.image = jugador_img
    imagen_computadora.config(image=computadora_img)
    imagen_computadora.image = computadora_img
    
    if determinar_ganador(jugador, computadora) == "Ganaste":
        imagen_ganador = imagen_jugador
        imagen_perdedor = imagen_computadora
    elif determinar_ganador(jugador, computadora) == "Perdiste":
        imagen_ganador = imagen_computadora
        imagen_perdedor = imagen_jugador
    else:
        imagen_ganador = None
        imagen_perdedor = None

    # Mover imagen ganadora hacia la imagen perdedora
    if imagen_ganador and imagen_perdedor:
        ganador_x, ganador_y = imagen_ganador.winfo_x(), imagen_ganador.winfo_y()
        perdedor_x, perdedor_y = imagen_perdedor.winfo_x(), imagen_perdedor.winfo_y()

        for _ in range(20):
            ventana.update()
            ganador_x += (perdedor_x - ganador_x) / 20
            ganador_y += (perdedor_y - ganador_y) / 20

            imagen_ganador.place(x=int(ganador_x), y=int(ganador_y))
            time.sleep(0.05)

        # Ocultar la imagen perdedora
        imagen_perdedor.place_forget()

    # Volver las imágenes a sus posiciones iniciales después de un breve retraso
    ventana.after(1000, reset_imagenes)

def reset_imagenes():
    imagen_jugador.place(x=100, y=400)
    imagen_computadora.place(x=500, y=400)

# Función para manejar la jugada
def jugar(eleccion):
    comp = eleccion_computadora()
    resultado = determinar_ganador(eleccion, comp)
    resultado_label.config(text=f"Computadora eligió: {comp}\nResultado: {resultado}")
    mostrar_imagen(eleccion, comp)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Piedra, Papel o Tijera")
ventana.geometry("800x600")  # Tamaño aumentado de la ventana

# Etiqueta de instrucciones
instrucciones_label = tk.Label(ventana, text="Elige tu jugada:", font=("Arial", 18))
instrucciones_label.pack(pady=20)

# Botones de jugada
boton_piedra = tk.Button(ventana, text="Piedra", width=10, command=lambda: jugar("piedra"))
boton_piedra.pack(pady=10)

boton_papel = tk.Button(ventana, text="Papel", width=10, command=lambda: jugar("papel"))
boton_papel.pack(pady=10)

boton_tijera = tk.Button(ventana, text="Tijera", width=10, command=lambda: jugar("tijera"))
boton_tijera.pack(pady=10)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="", font=("Arial", 18))
resultado_label.pack(pady=20)

# Etiquetas para mostrar las imágenes
imagen_jugador = tk.Label(ventana)
imagen_jugador.place(x=100, y=400)  # Posición inicial de la imagen del jugador

imagen_computadora = tk.Label(ventana)
imagen_computadora.place(x=500, y=400)  # Posición inicial de la imagen de la computadora

# Ejecutar la ventana
ventana.mainloop()
