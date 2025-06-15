from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .authUser import authenticate_user
from django.contrib.auth import login,logout
from .forms import AccountForm
from .models import Account
# Create your views here.

# EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def index(request):
    return render(request, "index.html")

def registration(request):
    form = AccountForm()
    if request.method == 'POST':
        reg_form_submit = AccountForm(request.POST)
        first_name = reg_form_submit['first_name'].value()
        last_name = reg_form_submit['last_name'].value()
        email = reg_form_submit['email'].value()
        phone_number = reg_form_submit['phone_number'].value()
        password = reg_form_submit['password'].value()
        username = email.split('@')[0]
        try:
            user_check=Account.objects.get(email=email)
        except Account.DoesNotExist:
            user_check=None
        if user_check is not None:
            messages.error(request, "This email address is already taken")
            context = {'form': form}
            return render(request, "login_registration.html", context)
        else:
            if password == request.POST.get('Confirm password'):
                user = Account.objects.create_user(
                    first_name=first_name,last_name=last_name,email=email,
                    username=username,password=password
                )
                user.phone_number = phone_number
                user.save()
                return redirect('email')
            else:
                messages.error(request, "password does not match>> re-enter your password")
    context={'form':form}
    return render(request, "login_registration.html", context)


def user_email_activation_link(request):
    if request.method =="POST":
        email=request.POST.get('email')
        user_email = email
        try:
            user=Account.objects.get(email=email)
        except Account.DoesNotExist:
            user =None
        if user is not None:
            mail_subject = "Account activation mail"
            current_site = get_current_site(request)
            email_context = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            }
            message = render_to_string("email_activation.html", email_context)
            emil_message = EmailMessage(mail_subject, message, to=[user_email])
            emil_message.send()
            messages.success(request,
                             f"you account has been created successfully and a confirmation has been sent to {user_email}")
            return render(request, "email.html")
        else:
            messages.error(request, "THIS EMAIL ADDRESS DOES NOT EXIST")
            return render(request, "email.html")
    return render(request, "email.html")


def user_login(request):
    page = "login"
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate_user(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")
    context={'page':page}
    return render(request, "login_registration.html", context)

def user_logout(request):
    logout(request)
    return redirect('home')

def activation(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()

        return render(request, "activation_success.html")
    else:
        return render(request, "activation_fail.html")


def reset_password(request):
    if request.method == "POST":
        email=request.POST.get('email')
        try:
            user=Account.objects.get(email=email)
        except Account.DoesNotExist:
            user =None
        if user is not None:
            user_email = email
            mail_subject = " Reset password  mail"
            current_site = get_current_site(request)
            email_context = {
                'user_email':user_email,
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            }
            message = render_to_string("reset_password_email.html", email_context)
            emil_message = EmailMessage(mail_subject, message, to=[user_email])
            emil_message.send()
            messages.success(request,f"Reset password confirmation has been sent to {user_email}")
            return render(request, "reset_password.html")
        else:
            messages.error(request, "THIS EMAIL ADDRESS DOES NOT EXIST")
    return render(request, "reset_password.html")


def reset_password_confirm(request, uidb64, token):
    if request.method=="POST":
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm-password')
        if password==confirm_password:
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user=Account._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return redirect('login')
            else:
                return HttpResponse("BAD REQUEST")
        else:
            messages.error(request, "password does not match>> re-enter your password")
    return  render(request, "reset_password_done.html")
