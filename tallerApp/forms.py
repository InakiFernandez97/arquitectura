from django import forms
from .models import Categoria, Producto
from django.forms import ModelForm

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"