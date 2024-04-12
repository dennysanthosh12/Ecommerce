
# app1/management/commands/update_product_prices.py
import time
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from app1.models import Product
from app1.scraping_utils import scrape_product_details

class Command(BaseCommand):
    help = 'Updates product prices and sends email notifications'

    def handle(self, *args, **options):
        while True:
            try:
                products = Product.objects.all()
                for product in products:
                    price = scrape_product_details(product.product_url)
                    if price:
                        current_price = price
                        product.current_price = current_price
                        product.save()
                        
                        if int(current_price) <= int(product.expected_price):
                            send_mail(
                                'Price Alert',
                                f'The price of {product.product_name} has fallen below the expected price!\n\nCurrent Price: ₹{current_price}\nExpected Price: ₹{product.expected_price}\nProduct URL: {product.product_url}',
                                's8602120@gmail.com',
                                [product.email],
                                fail_silently=False,
                            )
                            product.delete()
                time.sleep(60)  
            except Exception as e:
                self.stderr.write(f'Error occurred: {e}')
