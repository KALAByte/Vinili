from django import forms
from .models import Vinile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VinileForm(forms.ModelForm):
    class Meta:
        model = Vinile
        fields = ['titolo', 'autore', 'anno_pubblicazione', 'generi', 'formati', 'dimensione', 'velocita', 'prezzo', 'stock', 'disponibile', 'condizione', 'discogs_id', 'copertina']

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, label="Nome")
    last_name = forms.CharField(max_length=30, label="Cognome")
    telefono = forms.CharField(max_length=15, label="Numero di Telefono", required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']