import os
from time import sleep

# Import the required modules to interact with the mouse and keyboard
import pyautogui

# Import the required modules to capture and analyze screenshots
import mss

# Import the required modules to analyse and compare screenshots
from PIL import Image, ImageChops


# Set the desired monitor number

monitor_number = 0  # Replace with the desired monitor number


# Function to capture a screenshot of the specified monitor
def capture_screenshot(monitor_number=0):
    # Get the dimensions of the specified monitor
    monitor = mss.Monitor(monitor_number)
    width, height = monitor.width, monitor.height
    
    # Create a new MSS screen capture object
    with mss.mss() as sct:
        # Set the capture area to the specified monitor
        sct.monitor = monitor_number
        
        # Capture the screenshot and save it as a PNG file
        sct_img = sct.grab(sct.monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=f'screenshot_{monitor_number}.png')
        
        # Return the path to the saved screenshot file
        return os.path.abspath(f'screenshot_{monitor_number}.png')

# Example usage: Capture a screenshot of the primary monitor
screenshot_path = capture_screenshot(monitor_number)
print(f"Screenshot captured successfully: {screenshot_path}")

# Function to analyze the captured screenshot
def analyze_screenshot(screenshot_path):
    # Load the screenshot image using Pillow
    from PIL import Image
    
    # Open the screenshot image
    img = Image.open(screenshot_path)
    
    # Convert the image to grayscale
    grayscale_img = img.convert('L')
    
    # Save the grayscale screenshot as a PNG file
    grayscale_img.save('grayscale_screenshot.png')
    
    # Return the path to the saved grayscale screenshot file
    return os.path.abspath('grayscale_screenshot.png')

# Example usage: Analyze the grayscale screenshot

grayscale_screenshot_path = analyze_screenshot(screenshot_path)
print(f"Grayscale screenshot analyzed successfully: {grayscale_screenshot_path}")

def compare_screenshots(screenshot_path1, screenshot_path2):
    # sets the number of clicks the bot did to 0:
    clicked = 0  # Counter for the number of times the code inputs have been clicked
    clicked2 = 0  # Counter for the number of times codes have been inserted in the game because there are several codes in the game

    # Replace the coordinates with the desired coordinates for your game's alert popup coordinates:

    # Sets the coordinates for the first input of the code input box of the game:
    X = 100  # Replace with the desired X coordinate for the code input button of the code input box
    Y = 200  # Replace with the desired Y coordinate for the code input button of the code input box

    # Set the coordinates for the second input of the code input box of the game:
    X2 = 300  # Replace with the desired X2 coordinate for the code input button of the code input box
    Y2 = 400  # Replace with the desired Y2 coordinate for the code input button of the code input box

    # Set the coordinates for the third input of the code input box of the game:
    X3 = 500  # Replace with the desired X3 coordinate for the code input button of the code input box
    Y3 = 600  # Replace with the desired Y3 coordinate for the code input button of the code input box

    # Set the coordinates for the fourth input of the code input box of the game:
    X4 = 700  # Replace with the desired X4 coordinate for the code input button of the code input box
    Y4 = 800  # Replace with the desired Y4 coordinate for the code input button of the code input box

    # Set the coordinates for the code submission button of the code input box of the game:
    X5 = 900  # Replace with the desired X5 coordinate for the submission button
    Y5 = 1000  # Replace with the desired Y5 coordinate for the submission button


    # If no differences are found, click on the alert popup coordinates to simulate a successful code execution
    # Load the screenshots using Pillow
    img1 = Image.open(screenshot_path1)
    img2 = Image.open(screenshot_path2)

    # Compare the screenshots using the Pillow library
    diff = ImageChops.difference(img1, img2)

    # Save the difference image as a PNG file
    diff.save('diff_screenshot.png')

    if diff.getbbox() is None:
        print("No differences found between the screenshots.")
        pyautogui.alert(title="No differences found", message="No differences found between the screenshots.")

        # You will have to update the amount of clicks to the correct number of clicks you need:
        pyautogui.click(x=X, y=Y)
        clicked += 1
        print(f"Clicked {clicked} times.")
        pyautogui.click(x=X2, y=Y2)
        clicked += 1
        print(f"Clicked {clicked} times.")
        pyautogui.click(x=X3, y=Y3)
        clicked += 1
        print(f"Clicked {clicked} times.")
        pyautogui.click(x=X4, y=Y4)
        clicked += 1
        print(f"Clicked {clicked} times.")

        if clicked >= 4:
            pyautogui.click(x=X5, y=Y5) # click the code submission button after 4 clicks to submit the code to the game
            cleanup()
            clicked = 0 # reset the counter after 4 clicks
            print(f"Clicked submit {clicked2} times. That means that the program submitted the code to the input in the game.")
        elif clicked < 4:
            print("Please try again.")
            sleep(1)  # sleep for a little time to avoid lagging
            cleanup()
            clicked = 0  # reset the counter after 4 clicks
        else:
            print(f"Unknown error occurred while comparing screenshots.")
            sleep(1)  # sleep for a little time to avoid lagging
            cleanup()
            clicked = 0 # reset the counter after 4 clicks
    elif diff.getbbox() is not None:
        print("Differences found between the screenshots.")
        pyautogui.alert(title="Differences found", message="Differences found between the screenshots.")
        cleanup()
        compare_screenshots(screenshot_path, grayscale_screenshot_path)
    else:
        print("An error occurred while comparing screenshots.")
        sleep(1)  # sleep for a little time to avoid lagging
        cleanup()
        clicked = 0 # reset the counter after 4 clicks

    # Return the path to the saved difference image file
    return os.path.abspath('diff_screenshot.png')


# Example usage: Compare the grayscale screenshots

diff_screenshot_path = compare_screenshots(grayscale_screenshot_path, screenshot_path)
print(f"Difference screenshot compared successfully: {diff_screenshot_path}")

def cleanup():
    try:
        # Attempt to remove the screenshots from the filesystem
        # Remove the screenshots from the filesystem
        for screenshot in ['screenshot_0.png', 'grayscale_screenshot.png', 'diff_screenshot.png']:
            if os.path.exists(screenshot):
                os.remove(screenshot)
                print(f"Screenshot removing: {screenshot}")
                if not os.path.exists(screenshot):
                    print(f"Screenshot removed successfully: {screenshot}")
                elif os.path.exists(screenshot):
                    print(f"Error: Unable to remove {screenshot}. Are you in the correct directory?")
                    sleep(1) # sleep for a little time to avoid lagging
                    cleanup()
                else:
                    print(f"Unknown error occurred while removing screenshots.")
                    sleep(1) # sleep for a little time to avoid lagging
                    cleanup()
            elif not os.path.exists(screenshot):
                print(f"No screenshot found: {screenshot}")
                sleep(1) # sleep for a little time to avoid lagging
                cleanup()
            else:
                print(f"Error: Unable to remove {screenshot}. Are you in the correct directory?")
                sleep(1) # sleep for a little time to avoid lagging
                cleanup()
    except Exception as e:
        print(f"An error occurred while processing screenshots: {str(e)}")
        sleep(1) # sleep for a little time to avoid lagging
        cleanup()

if __name__ == "__main__":
    # Example usage: Capture, analyze, and compare screenshots of the primary monitor
    screenshot_path = capture_screenshot(monitor_number) # Capture the screenshot of the monitor
    grayscale_screenshot_path = analyze_screenshot(screenshot_path) # Analyze the screenshot of the monitor
    diff_screenshot_path = compare_screenshots(grayscale_screenshot_path, screenshot_path) # Compare the screenshot of the monitor against the image it should see
    print(f"All screenshots processed successfully: {screenshot_path}, {grayscale_screenshot_path}, {diff_screenshot_path}")
    sleep(1) # sleep for a little time to avoid lagging
    cleanup() # remove the screenshots from the filesystem after processing
