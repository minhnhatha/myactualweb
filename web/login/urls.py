from django.urls import path
from .import views
urlpatterns = [
    path('',views.index, name='signin'),
    path('up',views.signup, name='logup'),
]