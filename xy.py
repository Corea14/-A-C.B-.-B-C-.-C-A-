import pyautogui

while True:
    x, y = pyautogui.position()
    print(f"Coordenadas: ({x}, {y})")