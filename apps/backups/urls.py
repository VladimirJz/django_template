# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.backups import views
from apps.backups.views import listbackups

urlpatterns = [

    # The home page
    path('backups/', views.index, name='backups'),

    path('backups2/', listbackups.as_view()),

]
