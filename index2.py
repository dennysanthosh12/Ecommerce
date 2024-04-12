from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def scrape_product_details(product_url):
    def amazon(product_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(product_url)
        price_element = driver.find_element(By.CLASS_NAME, "a-price-whole")
        price = price_element.get_attribute("innerText").strip()
        print("price: "+ price)
        return price

    def flipkart(product_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(product_url)
        price_element = driver.find_element(By.CSS_SELECTOR, "._30jeq3._16Jk6d")
        price = price_element.get_attribute("innerText").strip()
        return price

    if product_url.startswith("https://www.flipkart.com"):
        price = float(flipkart(product_url).replace('₹','').replace(',','').replace('\n', '').replace('.', ''))
        print(price)
        return price
    elif product_url.startswith("https://www.amazon.in"):
        price = float(amazon(product_url).replace('₹','').replace(',','').replace('\n', '').replace('.', ''))
        print(price)
        return price
    else:
        return -1



product_url = "https://www.amazon.in/Plastic-Cricket-inches-Premium-Groups/dp/B09WVXMG96/ref=sr_1_1?keywords=cricket%20bat" 
price = scrape_product_details(product_url)
print(price)