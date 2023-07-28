from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


STATE_CHOICES = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhatisgarh', 'Chhatisgarh'),
    ('Daman & Diu', 'Daman & Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jarkhand', 'Jarkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punducherry', 'Punducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('TamilNadu', 'TamilNadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
    ('S', 'Shoes'),
    ('W', 'Watch'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
    
class SizeVariant(models.Model):
    size = models.CharField(max_length=20)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default=1)
    
    def __str__(self):
        return str(self.size)
    

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    shoe_sizes = models.ManyToManyField(SizeVariant, related_name='shoe_sizes', blank=True)
    topwear_sizes = models.ManyToManyField(SizeVariant, related_name='topwear_sizes', blank=True)
    bottomwear_sizes = models.ManyToManyField(SizeVariant, related_name='bottomwear_sizes', blank=True)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    
    
class Rating(models.Model):
    RATING_CHOICES = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
            
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Pending")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    
class Contact(models.Model):
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name = ("Contact")
        verbose_name_plural = ("Contacts")

    def __str__(self):
        return self.fullname
