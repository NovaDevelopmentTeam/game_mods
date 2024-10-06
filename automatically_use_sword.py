from time import sleep as wait
import pyautogui as pg
import random
import keyboard
import threading

# Variables for controlling the bot's actions

running = False

move_x = 100  # Example value
move_y = 100  # Example value

# creating threads for fighter class
class Fighter:
    
    @staticmethod # static method to simulate sword swinging
    def sword_swing():
        while running:  # Keep looping while the program is running
            pg.hotkey("E", interval=random.uniform(0.5, 0.8))  # swinging sword (like Gram)
            wait(random.uniform(0.5, 1))  # Adding a wait to simulate a delay between swings
    
    @staticmethod # static method to simulate camera movement and walking around
    def run_around():
        while running:  # Keep looping while the program is running
            pg.hotkey("W")  # walking forward
            pg.move(xOffset=move_x, yOffset=move_y)  # moving camera around in a circle slowly
            wait(random.uniform(0.5, 1))  # Adding a wait to simulate a delay in movement

# Start threads for both actions
def start_threads():
    thread_1 = threading.Thread(target=Fighter.sword_swing)
    thread_2 = threading.Thread(target=Fighter.run_around)
    
    # Start both threads
    thread_1.start()
    thread_2.start()

    # Join the threads to ensure they continue running
    thread_1.join()
    thread_2.join()

running = True

# Main
if __name__ == "__main__":
    start_threads()

    # Main loop to check for quit key
    while running:
        if keyboard.is_pressed('q'):
            running = False
            print("Exiting...")
            wait(random.uniform(3, 6))
            break

# Note: This script is a simple example to demonstrate how it would work to walk, rotate the camera, and swing a sword in a game.
 # In a real-world scenario, you would need to use a more advanced library like Pygame or PyAutoGUI to interact with the game's window.
 # Also, this script doesn't account for any potential issues like collisions or obstacles, so it's not suitable for a full-fledged game.
 # To make it more realistic, you might need to implement a pathfinding algorithm or use a more advanced game engine.
 # Also, keep in mind that this script won't work if the game window is not focused or in the foreground.
 # To fix this, you can use the `pyautogui.switch_to_window()` function to switch to the game window before running the script.
 # And make sure to call `pyautogui.close()` to close the game window after the script finishes running.