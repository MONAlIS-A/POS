from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES = (
    ('MC', 'Main Course'),
    ('Ap', 'Appetizers'),
    ('Dr', 'Drinks'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='product image')

    def __str__(self): 
        return str(self.id)
    
# Cart 
class Cart(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user =models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return str(self.product.title)


# Order  
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.PositiveIntegerField(null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order'
    
    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'
    
# Profile
class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    image =models.ImageField(default='avatar.jpg', upload_to='Profile_Images')

    def __str__(self):
        return f' {self.staff.username}- Profile'

