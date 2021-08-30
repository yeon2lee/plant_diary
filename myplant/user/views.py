from .models import CustomUser
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm 
from .forms import CustomUserChangeForm
from django.contrib import messages
from diary.models import Diary
from django.db.models import Q

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

def profile_view(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    context = {
        'user': user
    }
    posts = Diary.objects.all().filter(author=user)
    if request.user.is_anonymous:
        posts = posts.filter(open='all')
    else:
        posts = posts.filter(
            Q(open='all') |
            Q(open='follow') |
            (Q(open='private') & Q(author=request.user))
        )
    return render(request, 'profile.html', {'posts':posts, 'context':context, 'writer':user})

def profile_update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance = request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return redirect('/user/profile/'+str(request.user.pk))
    else:
        user_change_form = CustomUserChangeForm(instance = request.user)
        return render(request, 'update.html', {'user_change_form':user_change_form})

def profile_delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('diary:home')
    return render(request, 'delete.html')

def follow(request, pk):
    User = get_user_model()
    # 팔로우 당하는 사람
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        # 팔로우를 요청한 사람 => request.user
        # 팔로우가 되어 있다면,
        if user.followers.filter(pk=request.user.pk).exists():
            # 삭제
            user.followers.remove(request.user)
        else:
            # 추가
            user.followers.add(request.user)
    return redirect('/user/profile/'+str(user.pk))