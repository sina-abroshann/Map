from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns=[
    path('', views.home, name='home'),
    path('SubmitInformation', views.Submit_Information_View, name='Submit_Information_Path'),
    path('Cartable', views.Cartable, name='Cartable_Path'),
    path('Cartable/<int:id>/', views.Cartable_Details, name='Cartable_Details_Path'),
]