# from asyncio.events import _Context
from linecache import lazycache
from multiprocessing import context
from multiprocessing.dummy import current_process
from unicodedata import name
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from requests import request
from .models import Test,shopping_cart,product,purchase_record_model,tracking_list,order,client_user
from django.urls import reverse
from django.template import loader
# from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,User_form,PasswordChangeCustomForm
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.messages import get_messages
from datetime import datetime, timedelta,date
from .templates.universal_cpu_rank import unicpurank
from .templates.universal_gpu_rank import unigpurank
import numpy as np
from .templates.cpurank import cpuchallenge
from .templates.gpurank import gpuchallenge
import os
from pathlib import Path
from django.contrib.auth import update_session_auth_hash
BASE_DIR = Path(__file__).resolve().parent.parent
# from django.contrib.postgres.search import SearchVector
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return str(obj)
        return super().default(obj)
# from django.db.models.query_utils import Q
# def index(request):
#   template = loader.get_template('first.html')
#   return HttpResponse(template.render())

# Create your views here.
def index(request):
  search= request.POST.get('search') if request.POST.get('search') else ''
  gender=request.POST.getlist('gender') if request.POST.getlist('gender') else ['girl','boy']
  class_members=Test.objects.filter(name__contains=search,gender__in=gender).values()
  pd=product.objects.all()
  limit=5
  paginator=Paginator(class_members,limit)
  page=request.GET.get('page')
  try:
    class_members=paginator.page(page)
  except PageNotAnInteger:
    class_members=paginator.page(1)
  except EmptyPage:
    class_members=paginator.page(paginator.num_pages)
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'class_members':class_members,
    'gender':gender,
    'search_name':search,
    'user':request.user,
    'shopping_cart_count':count,
    'pd':pd
  }
  return render(request,"first.html",context)
# @login_required(login_url='/login')
def add(request):
  return render(request,"add.html",{})

def add_record(request):
  y = request.POST['name']
  z = request.POST['gender']
  member = Test( name=y,gender=z)
  member.save()  
  return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login1')
def delete(request,id):
  if str(request.user) != 'admin':
    return HttpResponse('你沒有權限')
  member=Test.objects.get(id=id)
  member.delete()
  return HttpResponseRedirect(reverse('index'))
  
def test1(request):
  limit=5
  test=Test.objects.all()
  paginator=Paginator(test,limit)
  
  page=request.GET.get('page')
  try:
    test=paginator.page(page)
  except PageNotAnInteger:
    test=paginator.page(1)
  except EmptyPage:
    test=paginator.page(paginator.num_pages)
  context={
    'test':test
  }
  return render(request,"test1.html",context)
def login_page(request):
  page='login'
  if request.user.is_authenticated:
    return redirect('index')
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    # try:
    #   user=User.objects.get(username=username)
    # except:
    #   messages.error(request,'用戶不存在')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('index')
    else:
      messages.error(request,'用戶或密碼錯誤')
  context={
    'page':page
  }
  return render(request,'login_.html',context)
def logoutUser(request):
  logout(request)
  return redirect('home')

def register_User(request):
  form=RegisterForm()
  # form.label_classes = ('class_a', 'class_b', )
  # form.label_class=('user_txt','password_txt','confirm_password_txt','email_input_bg','phone_txt')
  if request.method == 'POST':
    form=RegisterForm(request.POST)
    if form.is_valid():
      user=form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request,user)
      return redirect('home')
  context={
    'form':form,
  }
  return render(request,'login1.html',context)

def update_user(request):
  
  context={

  }
  return render(request,'profile.html',context)
@login_required(login_url='login1')
def profile(request,pk):
  user=request.user
  firstname= request.POST.get('new_first_name') if request.POST.get('new_first_name') else request.POST.get('first_name') if request.POST.get('first_name') else user.first_name
  lastname= request.POST.get('new_last_name') if request.POST.get('new_last_name') else request.POST.get('last_name') if request.POST.get('last_name') else user.last_name
  email=request.POST.get('new_email') if request.POST.get('new_email') else request.POST.get('email') if request.POST.get('email') else user.email
  
  form=User_form(instance=user)
  if request.POST.get('confirm')=='更改':
    if request.method == 'POST':
      form=User_form(request.POST,instance=user)
      if form.is_valid():
          form.save()
          return redirect('index')
  context={
    'first_name':firstname,
    'last_name':lastname,
    'email':email,
    'form':form,
    'str':['id_username','id_email']
  }
  return render(request,'profile.html',context)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email,'cbf108022@stmail.nptu.edu.tw' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('發生錯誤')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})
@login_required(login_url='login1')
def add_product(request):
  pk=request.POST.get('pk')
  try:
    product_=shopping_cart.objects.get(username=User.objects.get(id=request.user.id),product_name=product.objects.get(id=pk))
    # print(product_.counts)
    product_.counts+=1
    product_.save()
  except shopping_cart.DoesNotExist:
    product_=shopping_cart(username=User.objects.get(id=request.user.id),
                        product_name=product.objects.get(id=pk)
                        )
    product_.save()
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  storage = get_messages(request)
  for message in storage:
    print(message)
  return JsonResponse({'count':count})
@login_required(login_url='login1')
@csrf_exempt
def shopping_carts(request):
  user=User.objects.get(id=request.user.id)
  products=user.usernameOf.all()

  # if request.method=='POST':
  if is_ajax(request=request):
    # print(request.POST.get('id'),request.POST.get('select_value'))
    a=1
    if request.POST.get('ch') == 'one':
      for i in products:
        if str(i.id) == request.POST.get('id'):
          print(request.POST.get('id'))
          i.checks=str(request.POST.get('st'))
          i.save()
      pd=user.usernameOf.filter(checks='true')
      sum_t=0
      for i in pd:
        sum_t+=i.counts*i.product_name.price
      return JsonResponse({'sum':sum_t})
    elif request.POST.get('ch') == 'all':
      for i in products:
          i.checks=str(request.POST.get('st'))
          i.save()
      pd=user.usernameOf.filter(checks='true')
      sum_t=0
      for i in pd:
        sum_t+=i.counts*i.product_name.price
      return JsonResponse({'sum':sum_t})
    else:
      total=0
      product=user.usernameOf.filter(id=request.POST.get('id'))
      text_id='text_'+request.POST.get('id')
      if request.POST.get('input_value')=='+':
        a=int(request.POST.get('data'))+1
      if request.POST.get('input_value')=='-':
        a=int(request.POST.get('data'))-1
      if request.POST.get('input_value')=='text':
        a=int(request.POST.get('data'))
      if a<=0:
        a=1   
      for i in product:
        i.counts=a
        total=a*i.product_name.price
        i.save()
      pd=user.usernameOf.filter(checks='true')
      sum_t=0
      for i in pd:
        sum_t+=i.counts*i.product_name.price
      return JsonResponse({'test':a,'id':text_id,'total':total,'sum_id':request.POST.get('id'),'sum':sum_t})
  for i in products:
    i.checks='false'
    i.save()
  context={
    'products':products,
    'count':products.count(),
    'range':range(1,11)

  }
  return render(request,'shopping_cart.html',context)
@login_required(login_url='login1')
def delete_product(request,pk):
  product=shopping_cart.objects.get(id=pk)
  product.delete()
  return HttpResponseRedirect(reverse('shopping_cart'))
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
@csrf_exempt
def add_product2(request):
  a=1
  text_id='text_'+request.POST.get('id')
  if request.POST.get('input_value')=='+':
    a=int(request.POST.get('data'))+1
  if request.POST.get('input_value')=='-':
    a=int(request.POST.get('data'))-1
  if request.POST.get('input_value')=='text':
    a=int(request.POST.get('data'))
  # a=int(request.POST.get('input_value'))+int(request.POST.get('data'))
  # if request.POST.get('id')=='text':
  #   a=request.POST.get('input_value')
  #   print(a)
  return JsonResponse({'test':a,'id':text_id})
def home(request):
  
  ce=product.objects.values('category').distinct()
  top3_pd=product.objects.order_by('-number_of_purchases')[:4]
  tl=tracking_list.objects.filter(username=request.user.id).values_list('product_name',flat=True)
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'shopping_cart_count':count,
    'category':ce,
    'top4_pd':top3_pd,
    'tl':tl
  }
  return render(request,'home.html',context)
def login1(request):
  page='login'
  if request.user.is_authenticated:
    return redirect('home')
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('home')
    else:
      messages.error(request,'用戶或密碼錯誤')
  context={
    'page':page,
    'text_color':[]
  }
  return render(request,'login1.html',context)
def member_center(request):
  context={

  }
  return render(request,'member_centre.html',context)
def member_profile(request):
  user=User.objects.get(id=request.user.id)
  firstname=user.first_name
  email=user.email
  # firstname= request.POST.get('new_first_name') if request.POST.get('new_first_name') else request.POST.get('first_name') if request.POST.get('first_name') else user.first_name
  # phone= request.POST.get('new_phone') if request.POST.get('new_phone') else request.POST.get('phone') if request.POST.get('phone') else user.client_user.phone
  # email=request.POST.get('new_email') if request.POST.get('new_email') else request.POST.get('email') if request.POST.get('email') else user.email
  try:
    phone= request.POST.get('new_phone') if request.POST.get('new_phone') else request.POST.get('phone') if request.POST.get('phone') else user.client_user.phone
  except client_user.DoesNotExist:
    phone=''
  form=User_form(instance=user)
  if request.POST.get('confirm')=='更改':
    if request.method == 'POST':
      user.first_name=firstname
      user.email=email
      user.save()
      try:
        client_phone=client_user.objects.get(user=request.user)
        client_phone.phone=phone
        client_phone.save()
      except:
        client_phone=client_user(phone=phone,user=request.user)
        client_phone.save()
      form=User_form(request.POST,instance=user)
      if form.is_valid():
          form.save()
          return redirect('home')
      
  context={
    'first_name':firstname,
    'phone':phone,
    'email':email,
    'form':form,
    'str':['id_username','id_email']
  }
  return render(request,'member_profile.html',context)
def product_page(request,pk):
  pd=product.objects.get(id=pk)
  tl=tracking_list.objects.filter(username=request.user.id).values_list('product_name',flat=True)

  if is_ajax(request=request):
    pd=product.objects.get(id=request.POST.get('id'))
    if str(pd.category) == 'CPU':
      name_1=pd.product_name
      name_2=request.POST.get('name_2')
      result=unicpurank(name_1,name_2)
      result=result.scrape()
      return HttpResponse(json.dumps(result[0],ensure_ascii=False,default=default_dump))
    elif str(pd.category) == 'GPU':
      name_1=pd.product_name
      name_2=request.POST.get('name_2')
      result=unigpurank(name_1,name_2)
      result=result.scrape()
      
      return HttpResponse(json.dumps(result[0],ensure_ascii=False,default=default_dump))
    else:
      result=''
      return HttpResponse("")
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  f=pd.product_name
  f=f.replace(' ','_')
  context={
    'pd_name':'images/'+f+'.png',
    'pd':pd,
    'details':pd.Details,
    'tl':tl,
    'count':count,
  }
  return render(request,'product.html',context)
def buy(request):
  user=User.objects.get(id=request.user.id)
  products=user.usernameOf.all()
  all_product=product.objects.all()
  sum_price=0
  for i in all_product:
    for l in products:
      if i.id==l.product_name.id:
        sum_price+=l.counts*i.price
        i.number_of_purchases+=1
        i.save()
  for i in products:
    pr=purchase_record_model(username=i.username,product_name=i.product_name)
    pr.save()
  subject = "購買成功"
  c={
    'pd':products,
    'total':sum_price,
    'user_name':user.first_name
  }
  email_template_name="buy.html"
  email=render_to_string(email_template_name,c)
  send_mail(subject, email,'cbf108022@stmail.nptu.edu.tw' , [user.email], fail_silently=False,html_message=email)
  products.delete()
  return render(request,'shopping_cart.html',{})
def category(request,pk):
  ce=product.objects.values('category').distinct()
  pd=product.objects.filter(category=pk)
  tl=tracking_list.objects.filter(username=request.user.id).values_list('product_name',flat=True)
  
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'shopping_cart_count':count,
    'pd':pd,
    'pk':pk,
    'first_ce':ce[0],
    'category':ce[1:],
    'tl':tl
  }
  return render(request,'category.html',context)
@login_required(login_url='login1')
def purchase_record(request):
  # 取得購買清單
  # startdate = datetime.today()
  # enddate = startdate - timedelta(days=30)
  # pr=purchase_record_model.objects.filter(created__lte=enddate)
  # pr.delete()
  # user=User.objects.get(id=request.user.id)
  # pr=user.pr_usernameOf.all()
  total_order=order.objects.filter(username=request.user.id).values_list('order_number').distinct()
  context={
    'pr':total_order
  }
  return render(request,'purchase_record.html',context)
@login_required(login_url='login1')
def tracking_list_page(request):
  user=User.objects.get(id=request.user.id)
  tl=user.tl_usernameOf.all()
  context={
    'tl':tl
  }
  return render(request,'tracking_list.html',context)
@csrf_exempt
@login_required(login_url='login1')
def add_tl(request):
  if is_ajax(request=request):
    pk=request.POST.get('pk')
    a=''
    try:
      tl_=tracking_list.objects.get(username=User.objects.get(id=request.user.id),product_name=product.objects.get(id=pk))
      tl_.delete()
      a='delete'
    except tracking_list.DoesNotExist:
      tl_=tracking_list(username=User.objects.get(id=request.user.id),
                          product_name=product.objects.get(id=pk)
                          )
      tl_.save()
      a='add'
    storage = get_messages(request)
    for message in storage:
      print(message)
    return JsonResponse({'data':a,'pk':pk})
@login_required(login_url='login1')
def delete_tl(request,pk):
  tl=tracking_list.objects.get(id=pk)
  tl.delete()
  return HttpResponseRedirect(reverse('tracking_list'))

def Screening(agendas):
    q=Q()
    for agen in agendas:
        # q.add(Q(**{agen}), Q.OR)
        q |= Q(product_name__icontains = agen)| Q(category__icontains=agen) | Q(search_label__icontains=agen)
        # q.add(Q(product_name__icontains=agen) | Q(category__icontains=agen),Q.OR)
    od=product.objects.filter(q)
    return od
@csrf_exempt
def a(request):
  request.GET.get('search') if request.GET.get('search') else ''
  q=request.GET.get('q') if request.GET.get('q') else ''
  pd=product.objects.get(id=1)
  if is_ajax(request=request):
    pd=product.objects.get(id=request.POST.get('id'))
    if str(pd.category) == 'CPU':
      name_1=pd.product_name
      name_2=request.POST.get('cpu_name2')
      result=unicpurank(name_1,name_2)
      result=result.scrape()
      return HttpResponse(json.dumps(result[0],ensure_ascii=False,default=default_dump))
    elif str(pd.category) == 'GPU':
      name_1=pd.product_name
      name_2=request.POST.get('gpu_name2')
      print(name_1,name_2)
      result=unigpurank(name_1,name_2)
      result=result.scrape()
      
      return HttpResponse(json.dumps(result[0],ensure_ascii=False,default=default_dump))
    else:
      result=''
      return HttpResponse("")
   
  # pd=product.objects.filter(product_name__search=q)
  # pd=product.objects.annotate(
  #   search=SearchVector('product_name')
  # ).filter(search=q)
  context={
    'pd':pd,
    'q':q,
  }
  return render(request,'a.html',context)
def default_dump(obj):
  if isinstance(obj,(np.integer,np.floating,np.bool_)):
    return obj.item()
  elif isinstance(obj,np.ndarray):
    return obj.tolist()
  else:
    return obj
@login_required(login_url='login1')
def check_out(request):
  user=User.objects.get(id=request.user.id)
  pd=user.usernameOf.filter(checks='true')
  total=0
  for i in pd:
    total+=i.product_name.price*i.counts
  try:
    phone= request.POST.get('new_phone') if request.POST.get('new_phone') else request.POST.get('phone') if request.POST.get('phone') else user.client_user.phone
  except client_user.DoesNotExist:
    phone=''
  context={
    'pd':pd,
    'name':user.first_name,
    'phone':phone,
    'total':total,
    'counts':pd.count()
  }
  return render(request,'checkout.html',context)
@csrf_exempt
@login_required(login_url='login1')
def save_order(request):
  user=User.objects.get(id=request.user.id)
  if is_ajax(request=request):
    a=request.POST.getlist('chk_id[]')
    max_od_number=order.objects.filter(username=request.user.id).order_by('-order_number')[0].order_number if order.objects.filter(username=request.user.id).order_by('-order_number') else 0
    name=request.POST.get('name')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    cate=request.POST.get('cate')
    total=request.POST.get('total')
    pd=shopping_cart.objects.filter(checks='true')
    b=''
    
    for i in pd:
      od=order(username=User.objects.get(id=request.user.id),product_name=product.objects.get(id=i.product_name.id),order_number=max_od_number+1,address=address,state='待出貨',piker=name,category=cate,phone=phone,counts=i.counts,total=total,created=date.today())
      od.save()
      i.delete()
      b='success'
      # od=order()
    return JsonResponse({'data':b})
  context={
    'name':user.first_name,
    'phone':user.client_user.phone,
  }
  return render(request,'checkout.html',context)
@login_required(login_url='login1')
def delete_check(request,pk):
  product=shopping_cart.objects.get(id=pk)
  product.delete()
  return HttpResponseRedirect(reverse('shopping_cart'))
@login_required(login_url='login1')
def admin_order_tracking(request):
  od_tl=order.objects.all()
  total_order=order.objects.values_list('order_number','piker','address').distinct()
  context={
    'od_tl':od_tl,
    't_o':total_order
  }
  return render(request,'admin_order_tracking.html',context)
@login_required(login_url='login1')
def admin_order_tracking_detail(request,pk):
  detail=order.objects.filter(order_number=pk,username=request.user.id)
  context={
    'detail':detail
  }
  return render(request,'detail.html',context)
@csrf_exempt
@login_required(login_url='login1')
def update_state(request):
  if is_ajax(request):
    state=request.POST.get('state')
    order_number=request.POST.get('order_number')
    od=order.objects.filter(order_number=order_number)
    for i in od:
      i.state=state
      i.save()
    return JsonResponse({'state':state})
  return render(request,'detail.html',context)
@login_required(login_url='login1')
def user_order_tracking(request):
  total_order=order.objects.filter(username=request.user.id).values_list('order_number','piker','address').distinct()
  context={
    't_o':total_order
  }
  return render(request,'user_order_tracking.html',context)
@csrf_exempt
def send_email_(request):
  od=order.objects.filter(order_number=request.POST.get('od'),username=request.user.id)
  user=User.objects.get(id=request.user.id)
  subject = "到貨通知"
  c={
    'pd':od,
    'total':od[0].total,
    'user_name':user.first_name
  }
  email_template_name="notice.html"
  email=render_to_string(email_template_name,c)
  send_mail(subject, email,'cbf108022@stmail.nptu.edu.tw' , [user.email], fail_silently=False,html_message=email)
  return JsonResponse({})
def search(request):
  tl=tracking_list.objects.filter(username=request.user.id).values_list('product_name',flat=True)
  request.GET.get('search') if request.GET.get('search') else ''
  q=request.GET.get('q') if request.GET.get('q') else ''
  pd=Screening(str(q).split())
  # print(product.objects.filter(product_name__search=q))
  try:
    user=User.objects.get(id=request.user.id)
    products=user.usernameOf.all()
    count=products.count()
  except User.DoesNotExist:
    count=0
  context={
    'pd':pd,
    'q':q,
    'tl':tl,
    'shopping_cart_count':count,
  }
  return render(request,'search.html',context)
def cpu_rank(request):
  Cpu = cpuchallenge(request.POST.get("cpu_name1"))

  context = {
        "cpuranks":Cpu.scrape()
    }
  return render(request, "cpurank.html", context)

def cp (request):
  return render(request,"product_new.html")

def gpu_rank(request):
  Gpu = gpuchallenge(request.POST.get("gpu_name1"))

  context = {
        "gpuranks":Gpu.scrape()
    }
  return render(request, "gpurank.html", context)
def Line_robot(request):
  return render(request,'robot.html',{})
@login_required(login_url='login1')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'change_password.html', {'form': form})