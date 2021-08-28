from django.contrib import admin
from django.urls import path, include
from diary.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('diary/', include('diary.urls', namespace='diary')),
    path('shop/', include('shop.urls', namespace='shop')), 
    path('user/', include('user.urls', namespace='user')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
