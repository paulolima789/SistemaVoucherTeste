from django.contrib import admin
from django.urls import path, include
# importa as configurações da aplicação
from django.conf import settings
# importa as comfiguraçoes do static
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name='admin1'),
    path('', include('login.urls')),
    path('voucher/',include('app_voucher.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)