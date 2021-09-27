from django.shortcuts import render
from .forms import *
from .models import Customer
from django.http import HttpResponse
from django.shortcuts import  redirect
from .ML.script import get_joints, get_measurements

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

            points = get_joints(str(c.image))            
            shoulderDistance, waistDistance, torso, lower = get_measurements(points, c.height)

            values = {'shoulder': shoulderDistance, 'torso': torso, 'waist': waistDistance, 'lower': lower}
            return render(request, 'main/results.html', values)

            # return redirect('success')
    else:
        form = CustomerForm()
    return render(request, 'main/post.html', {'form' : form})