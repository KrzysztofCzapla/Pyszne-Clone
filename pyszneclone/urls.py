from django.contrib import admin
from django.urls import include, path
from register import views as v
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('menu/', include('main.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', v.register, name="register"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
