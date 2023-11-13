from django.shortcuts import render, redirect
from .models import Users
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.shortcuts import render, redirect
from users.forms import RegisterForm
#import qrcode
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from io import BytesIO
import base64


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate( email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'users/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'users/login.html')

    


# -------DESACTIVAR USUARIO-------

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


# -------REGISTRAR USUARIO-------



def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split('@')[0]

            exist = Users.objects.filter(email=email).exists()

            if not exist:
                user = Users.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.is_activate = True
                user.save()
                return render(request, 'users/login.html')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

#--------------------- cambio de contraseña ---------------------


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Su contraseña ha sido modificada con exito')
            return redirect('change_password')
        else:
            messages.error(request, 'Por favor, intente nuevamente.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

#--------- creación por QR ---------

