from django.urls import path
from . import views
urlpatterns = [
	path('', views.app, name = 'app'),
	path('login/customer', views.customer_login_view, name = 'customerlogin'),
	path('login/admin', views.admin_login_view, name = 'adminlogin'),
	path('login', views.general_login_view, name = 'login'),
	path('register', views.register_view, name = 'register'),
	path('dashboard/<str:email>', views.dashboard, name = 'dashboard'),
	path('sebet/<str:email>', views.sebet, name = 'sebet'),
	path('market', views.market, name = 'market'),
	path('logout', views.logout_view, name = 'logout'),
	path('dashboard/<str:email>/product/<str:product_id>', views.editProduct, name = 'editProduct'),
	path('product/<str:product_id>/addtosebet', views.addSebete, name = 'addSebete'),
	path('item/<str:item_id>/delete', views.deleteSebetItem, name = 'deleteItem'),

	# API
	path('item/<str:item_id>/increase/<str:quantity>', views.increaseQuantity, name = 'increaseQuantity'),
]