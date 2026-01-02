from django.contrib import admin

# Register your models here.
from .models import Cart, Item, User
from .models import Restaurant

admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Cart)