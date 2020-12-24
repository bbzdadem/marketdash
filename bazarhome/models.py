from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class SuperMarketAdministratorUser(models.Model):
	user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='supermarketadminuser')
	supermarket_name = models.CharField(max_length=100, blank = False, unique=True)
	phone_number = models.CharField(max_length=64, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	full_name = models.CharField(max_length=255)

	def __str__(self):
		return self.supermarket_name

class CustomerUser(models.Model):
	user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='customeruser')
	phone_number = models.CharField(max_length=64, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	full_name = models.CharField(max_length=255)

	def __str__(self):
		return self.full_name	

class Product(models.Model):
	supermarket = models.ForeignKey('SuperMarketAdministratorUser', on_delete=models.CASCADE, related_name='product')
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product')
	name = models.CharField(max_length=255)
	description = models.TextField(blank = True)
	image = models.ImageField(upload_to='Myproduct')
	price = models.FloatField(default=0)

	def __str__(self):
		return self.name


class ShoppingListItem(models.Model):
	product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name = 'shoppinglistitem')
	time = models.DateTimeField(auto_now_add=True)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.product.name} slitem"

	def total(self):
		return round(self.quantity*self.product.price,2)

class ShoppingList(models.Model):
	user = models.OneToOneField('CustomerUser', on_delete=models.CASCADE, related_name='shoppinglist')
	item = models.ManyToManyField('ShoppingListItem', blank = True, related_name = 'shoppinglist')

	def __str__(self):
		return f"{self.user.full_name} shoppinglist"

	def total(self):
		total = 0
		for item in self.item.all():
			total = total + item.quantity*item.product.price
		return f"{round(total, 2)}"


class Category(models.Model):
	text = models.CharField(max_length=65)

	def __str__(self):
		return self.text

class OrderItem(models.Model):
	product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orderitem')
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f"{self.product.name} slitem {self.quantity}"


class Order(models.Model):
	customer = models.ForeignKey('CustomerUser', on_delete=models.CASCADE, related_name='order')
	supermarket = models.ForeignKey('SuperMarketAdministratorUser', on_delete=models.CASCADE, related_name='order')
	item = models.ManyToManyField('OrderItem', blank = True, related_name = 'order')
	address = models.CharField(max_length=255)
	status = models.CharField(max_length=65, default='Ordered')
	ordered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"To {self.customer.full_name}"




