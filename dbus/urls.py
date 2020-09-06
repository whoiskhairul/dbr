from django.contrib import admin
from django.urls import path,include
from bus import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('khairul/', admin.site.urls),
    path('', include('bus.urls')),
    path('map/', include('map.urls')),
    path('accounts/',include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)