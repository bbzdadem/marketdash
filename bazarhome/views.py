from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()
# Create your views here.
def app(request):
	return render(request, 'bazarhome/app.html')

def deleteSebetItem(request, item_id):
	try:
		ShoppingListItem.objects.get(pk=int(item_id)).delete()
		return HttpResponseRedirect(reverse('sebet', args=(request.user.email,)))
	except ObjectDoesNotExist:
		pass

def increaseQuantity(request, item_id, quantity):
	if quantity:
		print(quantity)
	else:
		quantity = 1
	try:
		item = ShoppingListItem.objects.get(pk = int(item_id))
		user = CustomerUser.objects.get(user = request.user)
		item.quantity = int(quantity)
		item.save()
		return JsonResponse(
			{"item": {
				"mebleg":user.shoppinglist.total(),
				"total":round(item.product.price*item.quantity,2),
				"price":item.product.price, "quantity":item.quantity,
				"id":item.id
				}
			}, status=200)
	except ObjectDoesNotExist:
		return JsonResponse({"error": "Does not exist item"}, status = 404)


def addSebete(request, product_id):
	try:
		customer = CustomerUser.objects.get(user = request.user)
	except:
		pass
	try:
		shoplist = ShoppingList.objects.get(user = customer)
	except ObjectDoesNotExist:
		shoplist = ShoppingList(user = customer)
		shoplist.save()

	try: 
		product = Product.objects.get(pk = int(product_id))
		try:
			item = shoplist.item.get(product = product)
			item.quantity = item.quantity + 1
		except ObjectDoesNotExist:
			item = ShoppingListItem(product = product)
			
		item.save()
		shoplist.item.add(item)
		return HttpResponseRedirect(reverse('market'))
	except ObjectDoesNotExist:
		pass

def sebet(request, email):
	try:
		customer = CustomerUser.objects.get(user = request.user)
		return render(request, 'bazarhome/sebet.html',{
			"user":customer,
			})
	except:
		pass
	

def editProduct(request, email, product_id):
	try:
		user = User.objects.get(email = email)
		admin = SuperMarketAdministratorUser.objects.get(user = user)
		if request.user != user:
			pass
		if request.method == 'POST':
			name = request.POST['name']
			price = request.POST['price']
			category_id = request.POST['category']
			description = request.POST['description']
			image = 'img' in request.FILES and request.FILES['img']
			try:
				product = Product.objects.get(pk = int(product_id))
				product.name = name
				product.price = price
				product.description = description
				product.category = Category.objects.get(pk = int(category_id))
				if image:
					product.image = image
				product.save()
				return HttpResponseRedirect(reverse('dashboard', args=(email,)))
			except ObjectDoesNotExist:
				pass
		else:
			pass

	except ObjectDoesNotExist:
		pass

def market(request):
	if not request.user.is_authenticated:
		return general_login_view(request)
	else:
		try:
			user = CustomerUser.objects.get(user = request.user)
		except ObjectDoesNotExist:
			pass
	query = request.GET.get('q')
	if query:
		products = []
		for product in Product.objects.all():
			if product.category.text.upper() == query.upper() or product.supermarket.supermarket_name.upper() == query.upper():
				products.append(product) 
	else:
		products = Product.objects.all()
		
	return render(request, 'bazarhome/market.html',{
			'products':products,
			"markets": SuperMarketAdministratorUser.objects.all().order_by('-supermarket_name'),
			"categories": Category.objects.all().order_by('-text'),
			"user":user,
		})

def dashboard(request, email):
	if not request.user.is_authenticated:
		return general_login_view(request)
	try:
		user = User.objects.get(email = email)
		admin = SuperMarketAdministratorUser.objects.get(user = user)
		if request.user != user:
			return HttpResponseRedirect(reverse('login'))

		if request.method == 'POST':
			name = request.POST['name']
			price = request.POST['price']
			category_id = request.POST['category']
			description = request.POST['description']
			image = 'img' in request.FILES and request.FILES['img']
			try:
				new_product = Product(
					supermarket = admin,
					description = description,
					name = name,
					price = price,
					category = Category.objects.get(pk = int(category_id)),
					)
				if image:
					new_product.image = image
				new_product.save()
			except:
				pass
		return render(request, "bazarhome/dashboard.html",{
				"user":admin,
				'categories':Category.objects.all().order_by('-text')
			})
	except ObjectDoesNotExist:
		pass



def general_login_view(request):
	return render(request, "bazarhome/login.html")

def customer_login_view(request):
	if request.method == "POST":
		email = request.POST["email"]
		password = request.POST["password"]
		try:
			user = User.objects.get(email = email)
			if CustomerUser.objects.filter(user = user):
				user = authenticate(request, email=email, password=password)
				if user is not None:
					login(request, user)
					return HttpResponseRedirect(reverse('market'))
				else:
					return render(request, "bazarhome/csutomer.html",{
	       			"message": "Email or Password is not correct!",
	       			})
			else:
				return render(request, "bazarhome/csutomer.html",{
       			"message": "No customer account with this email!",
       			})
		except:
			return render(request, "bazarhome/csutomer.html",{
       			"message": "No account with this email!",
       			})
	else:
		return render(request, 'bazarhome/csutomer.html')

def admin_login_view(request):

	if request.method == "POST":
		email = request.POST["email"]
		password = request.POST["password"]

		try:
			user = User.objects.get(email = email)
			if SuperMarketAdministratorUser.objects.filter(user = user):
				user = authenticate(request, email=email, password=password)
				if user is not None:
					login(request, user)
					return HttpResponseRedirect(reverse('dashboard', args=(user.email,)))
				else:
					return render(request, "bazarhome/admin.html",{
	       			"message": "Email or Password is not correct!",
	       			})
			else:
				return render(request, "bazarhome/admin.html",{
       			"message": "No admin account with this email!",
       			})
		except:
			return render(request, "bazarhome/admin.html",{
       			"message": "No account with this email!",
       			})

	else:
		return render(request, 'bazarhome/admin.html')




def register_view(request):
    if request.method == "POST":
        full_name = request.POST["fullname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]
       	
        # Attempt to create new user
        try:
            user = User.objects.create_user(email = email, password = password)
            user.save()
            customer = CustomerUser(user = user, full_name = full_name, phone_number = phone)
            customer.save()
        except IntegrityError:
            return render(request, "bazarhome/register.html", {
                "message": "The mail already registered.",
            })
        login(request, user)
        return HttpResponseRedirect(reverse("market"))
    else:
        return render(request, "bazarhome/register.html")

def logout_view(request):
    logout(request)
    return app(request)
