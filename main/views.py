from django.shortcuts import render
from .forms import *
from .models import Customer
import cv2
from django.http import HttpResponse
from django.shortcuts import  redirect
from .ML.script import get_joints  

def success(request):
    # deletes all the previous images
    Customer.objects.all().delete()

    return HttpResponse('successfully uploaded')

# Create your views here.
def post_image(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)

        
        if form.is_valid():
            form.save()
            c = Customer.objects.all()[0]

            joints = get_joints(str(c.image))
       

        
            return redirect('success')
    else:
        form = CustomerForm()
    return render(request, 'main/post_image.html', {'form' : form})