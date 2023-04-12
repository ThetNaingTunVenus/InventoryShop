from django import forms
from .models import *


class ULoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'mobile', 'shipping_address']
        widgets = {
            'ordered_by': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            # 'ordered_staus': forms.Select(attrs={'class': 'form-control col-md-4'}),

        }


class AdminProductEditForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['item_name','category','pruchase_price','sell_price','balance_qty']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'category': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'pruchase_price': forms.NumberInput(attrs={'class': 'form-control col-md-6'}),
            'sell_price': forms.NumberInput(attrs={'class': 'form-control col-md-6'}),
            'balance_qty': forms.NumberInput(attrs={'class': 'form-control col-md-6', 'readonly':'True'}),

        }

class SupplierEditForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name','phone_number','address']
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
            'address': forms.TextInput(attrs={'class': 'form-control col-md-6'}),
        }

class DamageProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ['product','rate','quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control','readonly':'True'}),
            'rate': forms.TextInput(attrs={'class': 'form-control','readonly':'True'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control','readonly':'True'}),
        }

class StatusChangeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_staus']
        widgets = {'ordered_staus':forms.Select(attrs={'class':'form-control col-md-4'})}
