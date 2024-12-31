from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('panel_admin/', include('costumadmin.urls')),
                  path('', include('user.urls')),
                  # path('', include('zakaz22.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
