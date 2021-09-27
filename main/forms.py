# forms.py
from django import forms
from .models import *

class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = ['height', 'image']
