from time import sleep as wait
import pyautogui as pg
import random
import keyboard
import threading
import pygame
import mss
import numpy as np

# Note: This script is a simple example to demonstrate how it would work to walk, rotate the camera, and swing a sword in a game.
 # In a real-world scenario, you would need to use a more advanced library like Pygame or PyAutoGUI to interact with the game's window.
 # Also, this script doesn't account for any potential issues like collisions or obstacles, so it's not suitable for a full-fledged game.
 # To make it more realistic, you might need to implement a pathfinding algorithm or use a more advanced game engine.
 # Also, keep in mind that this script won't work if the game window is not focused or in the foreground.
 # To fix this, you can use the `pyautogui.switch_to_window()` function to switch to the game window before running the script.
 # And make sure to call `pyautogui.close()` to close the game window after the script finishes running.
 # Also, remember to install the necessary libraries by running `pip install mss numpy keyboard pygame` before running the script.
 # This script assumes that you have the necessary permissions to control the game's window and capture the screen.
 # If you encounter any issues, please let me know, and I'll do my best to help.
 # Enjoy your gameplay!

running = False

# Variables for controlling the bot's actions
move_x = 100  # Example value
move_y = 100  # Example value

# Fighter class with sword swinging and running around functionality
class Fighter:

    @staticmethod
    def sword_swing():
        while running:  # Keep looping while the program is running
            pg.hotkey("E", interval=random.uniform(0.5, 0.8))  # Swinging sword
            wait(random.uniform(0.5, 1))  # Simulate delay between swings

    @staticmethod
    def run_around():
        while running:  # Keep looping while the program is running
            pg.hotkey("W")  # Walking forward
            pg.move(xOffset=move_x, yOffset=move_y)  # Moving camera around
            wait(random.uniform(0.5, 1))  # Simulate delay in movement

# Main function to start the stream
# Screen recording function to capture and stream to Pygame window
def live_screen_stream():
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Live Screen Stream")
    
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}

    while running:
        # Capture the screen
        sct_img = sct.grab(monitor)
        img_array = np.array(sct_img)
        img_rgb = img_array[:, :, :3]

        # Convert image to Pygame surface
        screen_surface = pygame.surfarray.make_surface(np.rot90(img_rgb))
        window.blit(pygame.transform.scale(screen_surface, (screen_width, screen_height)), (0, 0))

        # Update the display
        pygame.display.update()

    pygame.quit()

# Start threads for both actions (sword swinging, running) and screen recording
def start_threads():
    global running
    running = True

    # Create threads for each action
    thread_1 = threading.Thread(target=Fighter.sword_swing)
    thread_2 = threading.Thread(target=Fighter.run_around)
    thread_3 = threading.Thread(target=live_screen_stream)  # Screen recording thread
    
    # Start all threads
    thread_1.start()
    thread_2.start()
    thread_3.start()

    # Join threads (if needed, but in most cases, this is not required if you want them to run concurrently)
    thread_1.join()
    thread_2.join()
    thread_3.join()

# Main
if __name__ == "__main__":
    start_threads()

    # Main loop to check for quit key
    while running:
        if keyboard.is_pressed('q'):
            running = False
            print("Exiting...")
            wait(random.uniform(3, 6))  # Simulate some delay before quitting
            break
