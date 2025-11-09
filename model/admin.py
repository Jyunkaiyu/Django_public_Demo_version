from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

# 1. 在這裡，我們從 models 多匯入一個 Product
from .models import Test, client_user, product

class client_user_Inline(admin.StackedInline):
    model = client_user
    can_delete = False
    verbose_name_plural = 'client'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (client_user_Inline,)

admin.site.register(Test)

# 2. 我們在這裡把 Product 註冊到後台
admin.site.register(product)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)