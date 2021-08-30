from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import json
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Diary, Comment
from .forms import DiaryForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    diary_list = Diary.objects.all()
    if request.user.is_anonymous:
        diary_list = diary_list.filter(open='all')
    else:
        diary_list = diary_list.filter(
            Q(open='all') |
            Q(open='follow') |
            (Q(open='private') & Q(author=request.user))
        )
    paginator = Paginator(diary_list, 4) 
    page = request.GET.get('page') 
    posts = paginator.get_page(page) 
    return render(request, 'home.html', {'posts':posts})

def detail(request, post_id): 
    post = get_object_or_404(Diary, pk = post_id) 
    comments = Comment.objects.filter(post_id=post_id, comment_id__isnull=True)

    re_comments = []
    for comment in comments:
        re_comments += list(Comment.objects.filter(comment_id=comment.id))

    form = CommentForm()
    return render(request, 'detail.html', {'post':post, 'comments':comments, 're_comments':re_comments, 'form':form})

@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.post_id = Diary.objects.get(pk=post_id)
            comment.author = request.user
            comment.save()
    return redirect('/diary/' + str(post_id))

@login_required
def create_re_comment(request, post_id, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.post_id = Diary.objects.get(pk=post_id)
            comment.comment_id = Comment.objects.get(pk=comment_id)
            comment.author = request.user
            comment.save()
    return redirect('/diary/' + str(post_id))

@login_required
def new(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.pubDate = timezone.now()
            post.author = request.user
            post.save()
            return redirect('diary:home')
    else:
        form = DiaryForm()
        return render(request, 'new.html', {'form':form})

@login_required
def edit(request, id):
    post = get_object_or_404(Diary, pk=id)
    if request.method == 'GET':
        editForm = DiaryForm(instance=post)
        return render(request, 'edit.html', {'editForm':editForm})
    else:
        editForm = DiaryForm(request.POST, request.FILES, instance=post)
        if editForm.is_valid():
            editArticle = editForm.save(commit=False)
            editArticle.pubDate = timezone.now()
            editArticle.author = request.user
            editArticle.save()
        return redirect('/diary/'+str(id))

@login_required
def delete(request, id):
    post = Diary.objects.get(id=id)
    post.delete()
    return redirect('diary:home')

def search(request):
    diary_list = Diary.objects.all().order_by('-id')

    page = request.GET.get('page', '1')
    q = request.GET.get('q', '')

    if page is None:
      page = '1'

    if q:
        posts = diary_list.filter( # 글쓴이 검색
            Q(content__icontains=q)   # 내용검색
        ).distinct()
        paginator = Paginator(posts, 4)
        posts = paginator.get_page(page)
        return render(request, 'home.html', {'posts' : posts, 'q' : q, 'page':page})
    else:
        return render(request, 'home.html')

def post_likes(request):
  if request.is_ajax():
    blog_id = request.GET.get('blog_id')
    post = Diary.objects.get(id=blog_id)

    user = request.user
    if post.like.filter(id = user.id).exists():
      post.like.remove(user)
      message = "좋아요 취소"
    else:
      post.like.add(user)
      message = "좋아요"
  context = {
    'like_count' : post.like.count(),
    'message' : message,
  }
  return HttpResponse(json.dumps(context), content_type="application/json")