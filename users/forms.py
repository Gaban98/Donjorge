from django import forms
from .models import Users

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 
                'last_name', 
                'email', 
                'username',
                'password']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'username': 'Usuario',
            'password': 'Contraseña'
        }