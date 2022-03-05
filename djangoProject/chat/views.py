from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import login as auth_logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . tokens import generate_token
from django.core.mail import EmailMessage,send_mail

from djangoProject import settings




# Create your views here.

# Requesting Sign In page
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    return render(request, 'index.html')

# Requesting Sign In page
def login(request):

    if request.method == "POST":
        Username = request.POST.get('Username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=Username, password=pass1)

        if user is not None:
            auth_login(request, user)
            uname = user.username
            return render(request, 'login.html', {'uname': uname})
        else:
            messages.error(request, "Mismatching Credentials")
            return redirect('/index')

    return render(request, 'login.html')


# Requesting create account page
@csrf_exempt
def create(request):

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        Username = request.POST.get('Username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=Username):
            messages.error(request, "Username Already Exist")
            return redirect('/create')

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered!")
            return redirect('/create')

        if pass1 != pass2:
            messages.error(request, "Password Mismatch")
            return redirect('/create')

        if not Username.isalnum():
            messages.error(request, "Username Should Be Alpha-Numeric!")
            return redirect('/create')

        myuser = User.objects.create_user(Username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.username = Username
        myuser.is_active = False

        myuser.save()

        messages.success(request, "Your Account is successfully Created. We have send you a confirmation Email. So,Please confirm your Email in order to Activate your Account... ")

        # Welcome Email

        subject = "Online Chat Room - Login"

        message = "Hello " + myuser.first_name +" "+myuser.last_name + "!! \n" + "ThankYou for visiting our Website.\nWe have sent you a Confimation Email, So please confirm your Email Address to activate your Account."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Online Chat Room - Login!!"
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.first_name + ' ' + myuser.last_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('/index')


    return render(request, "create.html")

@csrf_exempt

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('/index')

def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth_login(request, myuser)
        return redirect('/index')

    else:
        return render(request, "activation_failed.html")



