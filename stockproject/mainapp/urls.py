
from django.urls import path
from mainapp.views import*

urlpatterns = [
    path('',stockPicker,name='stockpicker'),
    path('stocktracker/',stockTraker,name='stocktracker'),


]