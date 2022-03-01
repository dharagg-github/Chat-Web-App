from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User


# Create your views here.

# Requesting Sign In page
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    return render(request, 'index.html')

# Requesting Sign In page
def login(request):
    return render(request, 'login.html')

# Requesting forget password page
@csrf_exempt
def forget(request):
    return render(request, "forget.html")

# Requesting create account page
@csrf_exempt
def create(request):
    print(request.method)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        Username = request.POST['Username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(Username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account is successfully Created")


        return redirect('/index')


    return render(request, "create.html")

def logout(request):
    pass
