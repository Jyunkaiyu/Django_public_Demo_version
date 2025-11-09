from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.db.models import Q
def index(request):
  context={}
  context["name"]="hello world!!"
  return render(request,"index.html",context)
def index1(request):
  context={}
  return render(request,"test.html",context)
