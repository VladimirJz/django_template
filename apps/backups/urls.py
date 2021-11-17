# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.backups import views
from apps.backups.views import index ,rule_new,StepAddView,steps_listview

urlpatterns = [

    # The home page
    #path('backups/', views.index, name='backups'),
    path('backups/',index.as_view()),
    path('backups/jobs/rule', views.rule_new, name='rule'),
    path('backups/jobs/rotation', views.rotation_rules, name='rule'),
    #path('backups2/', listbackups.as_view()),

    path('backups/steps/add', StepAddView.as_view(), name="add_step"),
    path('backups/steps', steps_listview.as_view(), name="step_list"),

]
