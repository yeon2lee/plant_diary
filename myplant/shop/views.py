from django.shortcuts import render

def home(request):
    return render(request, 'shop_home.html')