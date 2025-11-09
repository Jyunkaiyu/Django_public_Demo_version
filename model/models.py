from email.policy import default
from operator import mod
from django.db import models
from django.contrib.auth.models import User,BaseUserManager, AbstractBaseUser
from django.db.models import CharField
from django.db.models.functions import Lower
from datetime import datetime
CharField.register_lookup(Lower)
# Create your models here.
class client_user(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone=models.CharField(max_length=20,default='')
  USERNAME_FIELD = 'username'
class Test(models.Model):
  name=models.CharField(max_length=20)
  gender=models.CharField(max_length=10)

class discount(models.Model):
  name=models.CharField(max_length=20)
  Discount=models.IntegerField(default=1)

class product(models.Model):
  product_name=models.CharField(max_length=30)
  category=models.CharField(max_length=30)
  describe=models.CharField(max_length=10000)
  price=models.IntegerField(default=0)
  dsc=models.ForeignKey(discount,on_delete=models.CASCADE,related_name='discountOf',default='',blank=True,null=True)
  number_of_purchases=models.IntegerField(default=0)
  Details=models.CharField(default='',max_length=1000)
  search_label=models.CharField(max_length=100,default='')
  def __str__(self):
        return self.product_name
  
class shopping_cart(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='usernameOf')
  product_name=models.ForeignKey(product,on_delete=models.SET_NULL,null = True,related_name='product_nameOf')
  created=models.DateTimeField(auto_now_add=True)
  counts=models.IntegerField(default=1)
  checks=models.CharField(default='',max_length=10)
class purchase_record_model(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pr_usernameOf')
  product_name=models.ForeignKey(product,on_delete=models.SET_NULL,null = True,related_name='pr_product_nameOf')
  created=models.DateTimeField(auto_now_add=True)
class tracking_list(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tl_usernameOf')
  product_name=models.ForeignKey(product,on_delete=models.SET_NULL,null = True,related_name='tl_product_nameOf')
  created=models.DateTimeField(auto_now_add=True)
class order(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='od_usernameOf')
  product_name=models.ForeignKey(product,on_delete=models.SET_NULL,null = True,related_name='od_product_nameOf')
  order_number=models.IntegerField(default='')
  address=models.CharField(max_length=50)
  state=models.CharField(max_length=10)
  piker=models.CharField(max_length=100,default='')
  category=models.CharField(max_length=10,default='')
  phone=models.CharField(max_length=10,default='')
  counts=models.IntegerField(default=0)
  total=models.IntegerField(default=0)
  created=models.DateTimeField()
class Search(models.Lookup):
   lookup_name = 'search'

   def as_mysql(self, compiler, connection):
       lhs, lhs_params = self.process_lhs(compiler, connection)
       rhs, rhs_params = self.process_rhs(compiler, connection)
       params = lhs_params + rhs_params
       return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params

models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)