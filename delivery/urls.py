from django.urls import path
from delivery.views import home

urlpatterns = [
    path("",home,name='home')

]