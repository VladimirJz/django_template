# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # This redirec all routes /** to view function
    # 
    #re_path(r'^.*\.*', views.pages, name='pages'),

]
