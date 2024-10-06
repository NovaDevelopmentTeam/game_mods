# import zone
from time import sleep
import keyboard

# defining zone
running = False

class Bot:
    @staticmethod
    def press_space(): # presses some keys to optimize your movement in Warframe
        for _ in range(2):
            keyboard.press('space')
            sleep(0.25)
            keyboard.press('space')
        keyboard.press('shift')

    @staticmethod
    def scan_for_keys(): # scans for if you press ctrl and w at the same time that the press_space function starts
        global running
        while running:
            if keyboard.is_pressed('ctrl') and keyboard.is_pressed('w'):
                Bot.press_space()
                
                
# main
running = True

Bot.scan_for_keys() # initializes the bot
