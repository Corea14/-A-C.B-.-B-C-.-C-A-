import os
import pyautogui
import cv2
import numpy as np
import time

# class ConfiguracionImagen:
#     def __init__(self, coordenadas, coordenadas_clic, ruta_imagen):
#         self.coordenadas = coordenadas
#         self.coordenadas_clic = coordenadas_clic
#         self.ruta_imagen = ruta_imagen

class ConfiguracionImagen:
    def __init__(self, coordenadas, coordenadas_clic, ruta_imagen):
        self.coordenadas = coordenadas
        self.coordenadas_clic = coordenadas_clic
        self.ruta_imagen = ruta_imagen
# def estarenpartida():
# Variable para almacenar las coordenadas de la imagen encontrada
coordenadas_imagen_encontrada = None
    
def buscar_imagen(configuracion):
    

    coordenadas = configuracion.coordenadas
    coordenadas_clic_actual = configuracion.coordenadas_clic
    # ruta_imagen = configuracion.ruta_imagen
    # coordenadas = configuracion.coordenadas()
    # coordenadas_clic_actual = configuracion.coordenadas_clic()
    # ruta_imagen = configuracion.ruta_imagen()  # Evaluar la función para obtener la ruta de la imagen
    # Obtener la ruta completa de la imagen a buscar
    ruta_imagen = configuracion.ruta_imagen

    # Cargar la imagen a buscar con el canal alfa
    imagen_a_buscar = cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)

    # Capturar una captura de pantalla de la región de interés
    region_de_interes = pyautogui.screenshot(region=(coordenadas[0], coordenadas[1], coordenadas[2] - coordenadas[0], coordenadas[3] - coordenadas[1]))
    captura_pantalla = np.array(region_de_interes)

    # Convertir la captura de pantalla y la imagen a buscar a escala de grises
    captura_pantalla_gris = cv2.cvtColor(captura_pantalla, cv2.COLOR_BGR2GRAY)
    imagen_a_buscar_gris = cv2.cvtColor(imagen_a_buscar[:, :, :3], cv2.COLOR_BGR2GRAY)

    # Intentar encontrar la imagen en la captura de pantalla
    resultado = cv2.matchTemplate(captura_pantalla_gris, imagen_a_buscar_gris, cv2.TM_CCOEFF_NORMED)
    umbral = 0.8  # Puedes ajustar este umbral según tus necesidades

    ubicaciones = np.where(resultado >= umbral)
    if ubicaciones[0].size > 0:
        coordenadas_imagen_encontrada = (int(ubicaciones[1][0])+5 + coordenadas[0], int(ubicaciones[0][0])+5 + coordenadas[1])  # Convertir a enteros y ajustar a las coordenadas reales
        # Realizar clic del mouse en las coordenadas especificadas
        pyautogui.click(coordenadas_imagen_encontrada)
        return True
    else:
        print("Imagen no encontrada en la región definida.")
        return False

# Configuraciones para buscar la partida
configuracion_partida = ConfiguracionImagen(
    coordenadas=(613, 435, 745, 499),
    coordenadas_clic=(0, 0),
    ruta_imagen= os.path.join("img", "battle.png")
)

# Configuraciones para buscar el globo
configuracion_globo = ConfiguracionImagen(
    coordenadas= (575, 604, 857, 683),
    coordenadas_clic= (603, 400),
    ruta_imagen= os.path.join("img", "globo.png")
)

    


# Establecer el intervalo de tiempo en segundos
intervalo_tiempo = 5

while True:
    if buscar_imagen(configuracion_partida):
        # Se encontró la partida, realizar operaciones específicas
        while True:
            if buscar_imagen(configuracion_globo) and buscar_imagen(configuracion_partida):
                print("GLOBO ENCONTRADO :D")
                
                break  # Rompe el bucle secundario del globo

            time.sleep(1)  # Esperar 1 segundo antes de la próxima iteración del bucle secundario de la partida

        # Volver al bucle principal para buscar el globo
    else:
        print("Partida no encontrada. Esperando el siguiente intervalo de tiempo.")
        time.sleep(intervalo_tiempo)
