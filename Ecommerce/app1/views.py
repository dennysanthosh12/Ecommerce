
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
from queue import Queue
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Product
from django.urls import reverse
from urllib.parse import urlencode
from selenium.common.exceptions import NoSuchElementException


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                 
                 messages.error(request, 'Wrong Username or Password.')
            
        else:

            messages.error(request, 'Invalid form submission. Please check the form fields.')    
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, 'Username or email already exists.')
                return render(request, 'register.html', {'form': form})
            user = form.save()
            print(f"User registered: {user}")
            auth_login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'username': request.user.username})
    else:
        return redirect('login')

@login_required   
def result(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        results_amazon = scrape_amazon(product_name,driver)
        results_flipkart = scrape_flipkart(product_name,driver)
        driver.quit()

        sort_by = request.POST.get('filter')
        if sort_by == 'low_high':
            results_amazon = sorted(results_amazon, key=lambda x: float(x['price'].replace(',', '')))
            results_flipkart = sorted(results_flipkart, key=lambda x: float(x['price'].replace(',', '')))
        elif sort_by == 'high_low':
            results_amazon = sorted(results_amazon, key=lambda x: float(x['price'].replace(',', '')), reverse=True)
            results_flipkart = sorted(results_flipkart, key=lambda x: float(x['price'].replace(',', '')), reverse=True)
        return render(request, 'home_results.html', {'results_amazon': results_amazon,'results_flipkart': results_flipkart,'username': request.user.username})


def logout_view(request):
    logout(request)
    return redirect('login')

def scrape_amazon(product,driver):
    driver.get("https://www.amazon.in/")
    input_field = driver.find_element(By.ID, "twotabsearchtextbox")
    search_button = driver.find_element(By.ID, "nav-search-submit-button")

    input_field.send_keys(product)
    search_button.click()

    # Adding an implicit wait before further actions
    driver.implicitly_wait(2)
    products = []
    for i in range(2):
    # Extracting multiple elements using find_elements
        product_name_clases,product_image_classes = [".a-size-base-plus.a-color-base.a-text-normal",".a-size-medium.a-color-base.a-text-normal"],[".a-section.aok-relative.s-image-square-aspect",".a-section.aok-relative.s-image-fixed-height",".a-section.aok-relative.s-image-tall-aspect"]
        product_names = []
        image_outer_divs = []
        for classes1 in product_name_clases:
            element1 = driver.find_elements(By.CSS_SELECTOR, classes1)
            if element1:
                product_names.extend(element1)
        for classes2 in product_image_classes:
            element2 = driver.find_elements(By.CSS_SELECTOR, classes2)
            if element2:
                image_outer_divs.extend(element2)
        product_link = driver.find_elements(By.CSS_SELECTOR,".a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
        product_prices = driver.find_elements(By.CLASS_NAME, "a-price-whole")
        ratings_elements = driver.find_elements(By.CSS_SELECTOR, ".a-icon-alt")
        next_button = driver.find_element(By.CSS_SELECTOR,".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
        
        # Creating a list of dictionaries
        

        # Iterating over the elements and creating dictionaries
        # Iterating over the elements and creating dictionaries
        for name, price, rating_element,outer_div,link in zip(product_names, product_prices, ratings_elements,image_outer_divs,product_link):
            rating_text = rating_element.get_attribute('innerHTML')
            img_tag = outer_div.find_element(By.TAG_NAME,"img")
            img_src = img_tag.get_attribute('src')
            p_link = link.get_attribute('href')
            product_dict = {'name': name.text, 'price': price.text.replace('₹','').replace(',', ''), 'rating': rating_text, 'image': img_src,'link': p_link}
            products.append(product_dict)

        if not next_button.is_displayed():
            break    

        next_button.click()
        driver.implicitly_wait(2)

    return products

def scrape_flipkart(product,driver):
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
        for classes in product_link_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                product_link.extend(element)
        for classes in product_price_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                product_prices.extend(element)
        for classes in product_image_classes:
            element = driver.find_elements(By.CSS_SELECTOR,classes)
            if element:
                image_outer_divs.extend(element)
            
            
            
            
  
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
    
    return products

@login_required  
def product(request):
    product = request.GET.dict()
    

    return render(request, 'home_product.html', {'product': product})

@login_required  
def Tracking(request):
    if request.method == 'POST':
        try:
            product = request.GET.dict()
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')
            product_url = request.POST.get('product_url')
            expected_price = request.POST.get('expected_price')
            email = request.POST.get('user_email')
            product_price = float(product_price)
            
            existing_product = Product.objects.filter(product_url=product_url).first()
            if existing_product:
                existing_product.current_price = product_price
                existing_product.expected_price = expected_price
                existing_product.save()
                messages.success(request, 'Product updated successfully!')
            else:
                new_product = Product.objects.create(
                    product_name=product_name,
                    current_price=product_price,
                    product_url=product_url,
                    expected_price=expected_price,
                    email=email,
                    user=request.user
                )
                messages.success(request, 'Product added to tracking successfully!')

            # Serialize the product dictionary into a query string
            product_query_string = urlencode(product)
            
            # Redirect the user to the home page with the product query string
            return redirect(reverse('product') + '?' + product_query_string)

        except Exception as e:
            messages.error(request, f'Error occurred while adding/updating product: {str(e)}')

        # If any errors occur during the process, return a redirect to the product page
        return redirect('product')
    
    else:
        # If the request method is not POST, return a redirect to the product page
        return redirect('product')