# forms.py
from django import forms
from .models import *

class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = ['height', 'image']
		widgets = {
            'height': forms.NumberInput(attrs={"type": "text", "name": "title",  "id": "title", "class":"form-controll"}),
			'image' : forms.FileInput(attrs={"type":"file", "name":"images", "id":"images", "required":"required",
			"multiple":"multiple"}),
        }
