import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses TensorFlow logs

# Path to ChromeDriver
CHROMEDRIVER_PATH = r"C:\Users\Victo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Function to generate unique bot names
def generate_unique_names(count=60):
    adjectives = [
        "Clever", "Swift", "Brave", "Loyal", "Happy", "Quick", "Gentle", "Calm",
        "Wise", "Bold", "Eager", "Strong", "Bright", "Charming", "Fancy"
    ]
    nouns = [
        "Fox", "Tiger", "Panda", "Dolphin", "Eagle", "Bear", "Hawk", "Shark",
        "Lion", "Wolf", "Falcon", "Rabbit", "Otter", "Swan", "Rat"
    ]
    names = set()
    while len(names) < count:
        name = f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(10, 99)}"
        names.add(name)
    return list(names)

# Bot deployment function
def deploy_bots(pin, bot_count):
    bot_names = generate_unique_names(bot_count)
    service = Service(CHROMEDRIVER_PATH)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless)
    chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in containers

    drivers = []  # Store all active WebDriver instances

    for i, bot_name in enumerate(bot_names, start=1):
        try:
            print(f"Deploying bot {i}: {bot_name}")
            driver = webdriver.Chrome(service=service, options=chrome_options)
            drivers.append(driver)  # Add the driver to the list to keep it active
            driver.get("https://kahoot.it")
            
            # Enter the game PIN
            pin_field = driver.find_element(By.ID, "game-input")
            pin_field.send_keys(pin)
            pin_field.send_keys(Keys.RETURN)
            time.sleep(2)  # Wait for the nickname field to load
            
            # Enter the nickname
            nickname_field = driver.find_element(By.ID, "nickname")
            nickname_field.send_keys(bot_name)
            
            # Press "OK, go!"
            ok_go_button = driver.find_element(By.CSS_SELECTOR, '[data-functional-selector="join-button-username"]')
            ok_go_button.click()
            
            print(f"Bot {i} with name {bot_name} successfully joined!")
            time.sleep(1)  # Allow time before deploying the next bot
        except Exception as e:
            print(f"Error for bot '{bot_name}': {e}")
            if driver in drivers:
                drivers.remove(driver)  # Remove the driver if it failed to join
            driver.quit()

    # Keep all bots active
    print("All bots have joined and are now active!")
    try:
        while True:
            time.sleep(10)  # Keep the script running to maintain active bots
    except KeyboardInterrupt:
        print("Closing all bots...")
        for driver in drivers:
            driver.quit()

# Main execution
if __name__ == "__main__":
    game_pin = input("Enter the Kahoot Game PIN: ")
    bot_count = int(input("Enter the number of bots to deploy (max 60): "))
    bot_count = min(bot_count, 60)  # Limit to 60 bots
    deploy_bots(game_pin, bot_count)
