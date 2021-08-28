from .models import CustomUser
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm 
from diary.models import Diary

def login_view(request):
    if request.method == 'POST': 
        form = AuthenticationForm(request=request, data=request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password') 
            user = authenticate(request=request, username=username, password=password) 
            if user is not None:
                login(request, user) 
        return redirect("diary:home")
    else: 
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('diary:home')

def register_view(request):
    if request.method == "POST": 
        form = RegisterForm(request.POST) 
        if form.is_valid(): 
            user = form.save()
            login(request, user) 
        return redirect("diary:home")
    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form':form})

def profile_view(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    posts = Diary.objects.all()
    posts = posts.filter(author=user)
    return render(request, 'profile.html', {'posts':posts, 'context':context, 'writer':user})

