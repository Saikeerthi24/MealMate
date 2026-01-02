from django.http import HttpResponse
from django.shortcuts import render
from .models import Item, Restaurant, User, Cart

# Create your views here.
def index(request):
    return render(request, "index.html")
def open_signin(request):
    return render(request, 'signin.html')

def open_signup(request):
    return render(request, 'signup.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            return HttpResponse("This username is already registered. Please use a different email.")

        user = User(username=username, password=password, email=email, mobile=mobile, address=address)
        user.save()
        #return HttpResponse("Sign up Successful")
        #return HttpResponse(f"Username : {username} password : {password} email {email} mobile {mobile} address {address}")
        return render(request, "signin.html") 

    else:
        return HttpResponse("Invalid Response")
    
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(username, password)

    try:
        User.objects.get(username = username, password = password)
        if username == 'admin':
            return render(request, 'admin_home.html')
        else:
            restaurantList = Restaurant.objects.all()
            return render(request, 'customer_home.html',{"restaurantList" : restaurantList, "username" : username})

    except User.DoesNotExist:
        return render(request, 'fail.html')
def open_add_restaurant(request):
    return render(request, 'add_restaurant.html')
def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
            
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
        return HttpResponse("Successfully Added !")
        return render(request, 'admin_home.html')
def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})
def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant" : restaurant})
def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})
def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'update_menu.html',{"itemList" : itemList, "restaurant" : restaurant})
def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    #return render(request, 'admin_home.html')
    return HttpResponse("Item added successfully!")
def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    #return HttpResponse("Items collected")
    return render(request, 'customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restaurant, 
                     "username":username})
def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'show_restaurants.html',{"restaurantList" : restaurantList})
def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = User.objects.get(username = username)
    cart, created = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    return HttpResponse('added to cart')
def show_cart(request, username):
    customer = User.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0


    return render(request, 'cart.html',{"itemList" : items, "total_price" : total_price, "username":username})