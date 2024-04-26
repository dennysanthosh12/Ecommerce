from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def scrape_flipkart(product):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.flipkart.com/")

    input_field = driver.find_element(By.CLASS_NAME, "Pke_EE")
    search_button = driver.find_element(By.CLASS_NAME, "_2iLD__")

    input_field.send_keys(product)
    search_button.click()

    # Adding an implicit wait before further actions
    driver.implicitly_wait(2)
    products = []

    for i in range(2):
    # Extracting multiple elements using find_elements
        product_name_classes,product_link_classes,product_price_classes,product_image_classes = [".KzDlHZ",".wjcEIp",".WKTcLC"],[".wjcEIp",".CGtC98",".WKTcLC"],[".Nx9bqj._4b5DiR","._30jeq3._1_WHN1",".Nx9bqj"],["._53J4C-",".DByuf4","#no0123"]
        product_names = []
        product_link = []
        product_prices = []
        image_outer_divs = []
        for classes in product_name_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                product_names.extend(element)
                print(classes)
        for classes in product_link_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                product_link.extend(element)
                print(classes)
        for classes in product_price_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                product_prices.extend(element)
                print(classes)
        for classes in product_image_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                image_outer_divs.extend(element)
                print(classes)
            
            
            
            
  
        ratings_elements = driver.find_elements(By.CLASS_NAME, "XQDdHH")
        
        
        # Creating a list of dictionaries
        

        # Iterating over the elements and creating dictionaries
        # Iterating over the elements and creating dictionaries
        for name, price, rating_element,outer_div,prod_link in zip(product_names, product_prices, ratings_elements,image_outer_divs,product_link):
            rating_text = rating_element.text
            img_src = outer_div.get_attribute('src')
            p_link=prod_link.get_attribute('href')
            product_dict = {'name': name.text, 'price': price.text.replace('₹','').replace(',', ''), 'rating': rating_text+" out of 5", 'image': img_src,'link': p_link}
            products.append(product_dict)

        try:
            next_button = driver.find_element(By.CLASS_NAME,"_1LKTO3")
            next_link = next_button.get_attribute('href')
        except NoSuchElementException:
            break    

        if not next_button.is_displayed():
            break

        driver.get("flipkart.com"+next_link)
        driver.implicitly_wait(2)
    
    driver.quit()
    return products

results = scrape_flipkart("dress")
print(results)