from time import sleep
import keyboard
import pyttsx3  # Zum Sprechen von Text der eigentlich ein print command war
import random
import json
import threading
import ctypes
import os
import cv2  # Für Bildverarbeitung (OpenCV)
import numpy as np
from mss import mss  # Zum Bildschirm aufnehmen
import open3d as o3d  # Für 3D-Modellverarbeitung
import subprocess  # Zum Starten des Spiels


# Globale Variable, um den Bot-Status zu verfolgen
running = False

class Bot:
    @staticmethod
    def get_enemy_models():
        """Lädt Feindmodelle aus der JSON-Datei."""
        try:
            with open("enemies.json", "r") as file:
                enemies = json.load(file)
                return enemies
        except FileNotFoundError:
            print("Error: enemies.json file not found.")
            return []
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from enemies.json.")
            return []

    @staticmethod
    def capture_screen():
        """Nimmt den aktuellen Bildschirm auf."""
        try:
            with mss() as sct:
                monitor = sct.monitors[1]  # Erster Monitor (kann angepasst werden)
                screen = np.array(sct.grab(monitor))
                return screen
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None

    @staticmethod
    def load_3d_model(model_path):
        """Lädt ein 3D-Modell aus einer Datei."""
        try:
            model = o3d.io.read_triangle_mesh(model_path)
            return model
        except Exception as e:
            print(f"Error loading 3D model from {model_path}: {e}")
            return None  # Rückgabe von None, wenn das Modell nicht geladen werden kann

    @staticmethod
    def analyze_3d_model(screen, model):
        """Analysiert das 3D-Modell im Kontext des Screens."""
        if model is None:
            print("Error: No valid 3D model provided.")
            return False

        try:
            # Annahme: model hat eine Methode, um die Vertices zu erhalten
            vertices = np.asarray(model.vertices)

            # Beispielkameraparameter (diese müssen je nach Spielsituation angepasst werden)
            camera_position = np.array([0, 0, 0])  # Beispielposition der Kamera
            focal_length = 1000  # Brennweite für die Projektion

            # Bilddimensionen
            height, width, _ = screen.shape

            projected_points = []

            # Projektion der 3D-Punkte in 2D-Punkte
            for vertex in vertices:
                # Berechne die 2D-Koordinaten (vereinfachte Projektion)
                x_2d = int((vertex[0] - camera_position[0]) * focal_length / vertex[2]) + width // 2
                y_2d = int((vertex[1] - camera_position[1]) * focal_length / vertex[2]) + height // 2

                # Überprüfe, ob die projizierten Punkte im Bild liegen
                if 0 <= x_2d < width and 0 <= y_2d < height:
                    projected_points.append((x_2d, y_2d))

            # Beispielhafte Sichtbarkeitsprüfung
            for (x, y) in projected_points:
                # Überprüfe den RGB-Wert an der Stelle (x, y)
                pixel_color = screen[y, x]
                if np.all(pixel_color != [0, 0, 0]):  # Beispiel: Überprüfe, ob der Pixel nicht schwarz ist
                    print(f"Model is visible at screen coordinates: ({x}, {y})")
                    return True  # Modell ist sichtbar

            print("Model is not visible.")
            return False  # Modell ist nicht sichtbar
        except Exception as e:
            print(f"Error analyzing 3D model: {e}")
            return False

    @staticmethod
    def detect_enemy_on_screen(screen, enemy_images):
        """Erkennt Feinde auf dem Bildschirm anhand von Bildern."""
        try:
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            for enemy_img in enemy_images:
                result = cv2.matchTemplate(screen_gray, enemy_img, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)

                threshold = 0.8
                if max_val >= threshold:
                    return max_loc
            return None
        except Exception as e:
            print(f"Error detecting enemy on screen: {e}")
            return None

    @staticmethod
    def aim_bot():
        """Hauptlogik des Aimbots, erkennt Feinde und zielt."""
        screen = Bot.capture_screen()
        if screen is None:
            return  # Stoppe, wenn der Screenshot nicht erfolgreich war
        enemies = Bot.get_enemy_models()  # Lädt Feindmodelle
        for enemy in enemies:
            enemy_images = [cv2.imread(img_path, 0) for img_path in enemy["model_paths"]]  # Alle Blickwinkel laden
            enemy_pos = Bot.detect_enemy_on_screen(screen, enemy_images)  # Überprüft, ob ein Feind erkannt wird
            if enemy_pos:
                print(f"Enemy detected at {enemy_pos}, aiming...")
                model = Bot.load_3d_model(enemy["model_path_3d"])  # Neuen Parameter für den 3D-Pfad
                if Bot.analyze_3d_model(screen, model):
                    print("3D model is visible, executing action...")
                    keyboard.mouse.click()  # Simuliere Schuss

    @staticmethod
    def load_cursor_image(cursor_path):
        """Lädt das Cursorbild von der Datei."""
        try:
            if os.path.isfile(cursor_path):
                cursor_handle = ctypes.windll.user32.LoadImageW(
                    None, cursor_path, 2, 0, 0, 0x00000010  # LR_LOADFROMFILE
                )
                return cursor_handle
            else:
                print("Cursor file not found.")
                return None
        except Exception as e:
            print(f"Error loading cursor image: {e}")
            return None

    @staticmethod
    def show_new_crosshair(cursor_path):
        """Zeigt den neuen Cursor an."""
        global running
        while running:
            if keyboard.is_pressed('right click'):
                cursor_handle = Bot.load_cursor_image(cursor_path)
                if cursor_handle:
                    ctypes.windll.user32.SetSystemCursor(cursor_handle)
                Bot.aim_bot()  # Aufruf der Zielen-Funktion
        # Hier wird der Cursor zurückgesetzt, wenn der Thread endet
        ctypes.windll.user32.SetSystemCursor(0)

def stop_bot():
    """Stoppt den Bot und setzt den Cursor zurück."""
    global running
    running = False
    print("Bot stopped. Stopping aimbot function (could take a few seconds)...")
    sleep(random.uniform(2, 5))
    print("Aimbot function stopped.")
    sleep(1)
    print("Crosshair cursor resetting (could take a few seconds)...")
    ctypes.windll.user32.SetSystemCursor(0)
    sleep(random.uniform(2, 5))
    print("Crosshair cursor reset.")

def start_warframe():
    """Startet das Warframe-Spiel über den Epic Games Launcher."""
    try:
        subprocess.Popen(["C:\\Program Files\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe"])  # Passe den Pfad an, falls nötig
        sleep(10)  # Wartezeit, um sicherzustellen, dass der Launcher startet
    except Exception as e:
        print(f"Error starting Warframe: {e}")

def wait_for_login():
    """Warte auf die Benutzereingabe und pausiert den Bot während des Logins."""
    global running

    pyttsx3.speak("Please log in to Warframe.")
    
    # Warte darauf, dass der Benutzer seine Anmeldedaten eingibt
    try:
        keyboard.wait('enter')  # Warte auf Drücken der Enter-Taste nach dem Login
        pyttsx3.speak("Login detected. Waiting for 1 minute to choose a mission...")
        sleep(60)  # Warte 1 Minute nach dem Login
    except Exception as e:
        print(f"Error during login wait: {e}")

# Hauptfunktion
def main():
    global running
    cursor_path = 'crosshair.ico'
    running = True

    # Starte Warframe
    start_warframe()

    # Warte auf die Benutzereingabe, um den Bot zu pausieren
    wait_for_login()

    # Erstelle einen Thread für den Cursor
    crosshair_thread = threading.Thread(target=Bot.show_new_crosshair, args=(cursor_path,))
    crosshair_thread.start()

    try:
        while running:
            sleep(1)
    except KeyboardInterrupt:
        stop_bot()
        running = False  # Setze running auf False, um den Thread zu beenden
        crosshair_thread.join()  # Warte darauf, dass der Thread vollständig endet


if __name__ == "__main__":
    pyttsx3.speak("Starting Warframe Aimbot...")
    main()
