from button import click_button
import fake_useragent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import pyperclip


def generate_random_name(min_length=7, max_length=10):
    length = random.randint(min_length, max_length)
    letters = string.ascii_letters
    random_name = ''.join(random.choice(letters) for _ in range(length))
    return random_name


def generate_random_number():
    return random.randint(1, 4)


def get_proxy_list():
    proxy_list = []
    with open('proxy.txt', 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(':')
                if len(parts) == 4:
                    proxy_list.append(parts)
    return proxy_list


def setup_chrome_options(headless):
    options = Options()
    options.add_argument(f'user-agent={UserAgent().random}')
    options.add_extension('wallet.crx')
    options.add_extension('captcha.crx')
    if headless:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    return options


def get_phrases(file_path):
    phrases = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                phrases.append(line.strip().split())
    return phrases


headless_input = input('Включить headless режим? (+/-): ').strip()
headless = headless_input == '+'

proxy_list = get_proxy_list()
phrases = get_phrases('mnemonic.txt')  # Replace with the actual file name

i = 0
while i < len(proxy_list) and i < len(phrases):
    proxy = proxy_list[i]
    phrase = phrases[i]

    try:
        ip, port, login, password = proxy
        print(f"Using proxy {i + 1}/{len(proxy_list)}: {ip}:{port}")

        options = setup_chrome_options(headless)

        proxy_options = {
            'proxy': {
                'http': f'http://{login}:{password}@{ip}:{port}',
                'https': f'https://{login}:{password}@{ip}:{port}',
            }
        }

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
            seleniumwire_options=proxy_options
        )

        driver.implicitly_wait(10)
        useragent = fake_useragent.UserAgent().random
        headers = {'user-agent': useragent}
        sleep(2)

        driver.get("https://www.google.com")
        sleep(2)

        # Close all other tabs and switch to the first one
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()

        driver.switch_to.window(driver.window_handles[0])
        # Perform the desired operations
        driver.get("chrome-extension://dldjpboieedgcmpkchcjcbijingjcgok/index.html")
        sleep(1)
        click_button(driver,
                     selector='/html/body/div/main/div/div/div[3]/article[1]/div[2]',
                     selector_type=By.XPATH)
        click_button(driver,
                     selector='/html/body/div/main/div/div/div[4]/button',
                     selector_type=By.XPATH)
        click_button(driver,
                     selector='/html/body/div/main/div/div/div[5]/button[2]',
                     selector_type=By.XPATH)
        click_button(driver,
                     selector='/html/body/div/main/div/div/div[2]/div[2]/div[1]/footer/button',
                     selector_type=By.XPATH)
        wallet = pyperclip.paste()
        click_button(driver,
                     selector='/html/body/div/main/div/div/div[2]/div[2]/div[3]/button',
                     selector_type=By.XPATH)
        click_button(driver,
                     selector='/html/body/div/main/div/div/div[2]/div[3]/button[2]',
                     selector_type=By.XPATH)
        wallet = pyperclip.paste()
        words = wallet.strip().split()
        print(words)
        i = 0
        sleep(1)
        for i in range(1, 13):
            xpath_main = f'/html/body/div/main/div/div/div[3]/div[1]/div/div/div[{i}]/div/input'
            try:
                input_element = driver.find_element(by=By.XPATH, value=xpath_main)
                input_element.send_keys(words[i - 1])
            except:
                continue
        click_button(driver, selector='/html/body/div/main/div/div/div[3]/div[2]/button[2]',
                             selector_type=By.XPATH)
        click_button(driver, selector='/html/body/div/main/div/form/div/div[3]/div[1]/div[1]/div/div[2]/input',
                     selector_type=By.XPATH, input_value='Qwerrty0987!')
        click_button(driver, selector='/html/body/div/main/div/form/div/div[3]/div[1]/div[2]/div/input',
                     selector_type=By.XPATH, input_value='Qwerrty0987!')
        click_button(driver, selector='/html/body/div/main/div/form/div/div[3]/div[2]/button[2]',
                     selector_type=By.XPATH)
        sleep(5)
        driver.get('chrome-extension://ifibfemgeogfhoebkmokieepdoobkbpo/options/options.html')
        sleep(1)
        driver.find_element(by=By.XPATH,
                            value=('/ html / body / div / div[1] / table / tbody / tr[1] / td[2] / input')).send_keys(
            '1c466eee3cd37266debdc32909fc4a78')
        driver.find_element(by=By.XPATH,
                            value=('/ html / body / div / div[1] / table / tbody / tr[1] / td[3] / button')).click()
        sleep(2)
        alert = driver.switch_to.alert
        print(alert.text)
        alert.accept()
        sleep(1)
        driver.get('https://faucet-testnet.fuel.network/')
        sleep(5)
        driver.get('https://faucet-testnet.fuel.network/')
        sleep(2)
        click_button(driver, selector='/html/body/div[1]/div/div[1]/div[2]/div[1]',
                     selector_type=By.XPATH)
        sleep(1000)



    except Exception as e:
        print(f"An error occurred with proxy {ip}:{port} - {e}")

    i += 1

print("All proxies and mnemonics have been used. Script completed.")
