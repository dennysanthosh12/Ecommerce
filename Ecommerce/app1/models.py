from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_url = models.URLField(primary_key=True)
    email = models.EmailField(max_length=254, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
