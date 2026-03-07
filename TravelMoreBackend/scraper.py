from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_title(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        return driver.title
    finally:
        driver.quit()
