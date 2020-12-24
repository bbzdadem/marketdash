from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'price', 'category', 'supermarket')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('customer', 'supermarket', 'address', 'status', 'ordered')


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (_('Privacy info'), {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name','is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)




admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(SuperMarketAdministratorUser)
admin.site.register(CustomerUser)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingListItem)
admin.site.register(ShoppingList)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
