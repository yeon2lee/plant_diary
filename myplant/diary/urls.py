from django.urls import path
from .views import *

app_name = 'diary'

urlpatterns = [
    path('', home, name="home"),
    path('<int:post_id>', detail, name="detail"),
    path('new/', new, name="new"),
    path('edit/<int:id>', edit, name="edit"),
    path('delete/<int:id>', delete, name="delete"),
    path('search', search, name="search"),
    path('<int:post_id>/comment', create_comment, name="comment"),
    path('<int:post_id>/comment/<int:comment_id>', create_re_comment, name="re_comment"),
    path('like/', post_likes, name="post_likes"),
] 