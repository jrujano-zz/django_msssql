from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from chat.views import ChatterBotAppView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('api/chat/', ChatterBotAppView.as_view()),

]
