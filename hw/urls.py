from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 
from . import views

urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.home_page, name="home_page"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
