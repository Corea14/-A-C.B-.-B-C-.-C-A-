import os
import pyautogui
import cv2
import numpy as np
import time

# Obtener la ruta completa de la imagen a buscar
ruta_imagen = os.path.join("img", "globo.png")

# Cargar la imagen a buscar directamente en escala de grises
imagen_a_buscar = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

# Coordenadas de las esquinas del rectángulo (esquina superior izquierda y esquina inferior derecha)
x1, y1 = 575, 604
x2, y2 = 857, 683

# Establecer el intervalo de tiempo en segundos
intervalo_tiempo = 5

# Variable para almacenar las coordenadas de la imagen encontrada
coordenadas_imagen_encontrada = None

def buscar_imagen():
    global coordenadas_imagen_encontrada  # Usamos la variable global

    try:
        # Capturar una captura de pantalla de la región de interés
        region_de_interes = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        captura_pantalla = np.array(region_de_interes)

        # Convertir la captura de pantalla a escala de grises y asegurarse de que tiene la profundidad adecuada
        captura_pantalla = cv2.cvtColor(captura_pantalla, cv2.COLOR_RGB2BGR)
        captura_pantalla_gris = cv2.cvtColor(captura_pantalla, cv2.COLOR_BGR2GRAY)

        # Intentar encontrar la imagen en la captura de pantalla
        resultado = cv2.matchTemplate(captura_pantalla_gris, imagen_a_buscar, cv2.TM_CCOEFF_NORMED)
        umbral = 0.8

        ubicaciones = np.where(resultado >= umbral)
        if ubicaciones[0].size > 0:
            # Almacenar las coordenadas de la esquina superior izquierda de la imagen encontrada
            coordenadas_imagen_encontrada = (int(ubicaciones[1][0])+5 + x1, int(ubicaciones[0][0])+5 + y1)  # Convertir a enteros y ajustar a las coordenadas reales
            
            print(f"Imagen encontrada en la región definida. Coordenadas: {coordenadas_imagen_encontrada}. Realizando clic del mouse.")
            pyautogui.click(coordenadas_imagen_encontrada)  # Hacer clic en las coordenadas encontradas
            mensaje = "Imagen encontrada"
        else:
            print("Imagen no encontrada en la región definida.")
            coordenadas_imagen_encontrada = None
            mensaje = "Imagen no encontrada"

        

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        while True:
            buscar_imagen()
            time.sleep(intervalo_tiempo)
    except KeyboardInterrupt:
        print("\nPrograma detenido por el usuario.")
