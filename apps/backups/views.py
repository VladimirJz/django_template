from django.shortcuts import render

# Create your views here.
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Backups, Status,Locations
from django.db.models import Sum
from django.views.generic import ListView

@login_required(login_url="/login/")
def index2(request):
    '''
    Pagina de Incio
    '''
    num_backups=Backups.objects.all().count()
    ok_backups=Backups.objects.filter(Status__exact=1).count()


    data_size = Backups.objects.filter(Status__exact=1).aggregate(Sum('SizeMB'))['SizeMB__sum']
    data_size=round(data_size/1024,2)

    app='backups'
    view='index'
    context = {'app':app,'view':view,
        'num_backups': num_backups,'ok_backups': ok_backups,'data_size':data_size}

    html_template = loader.get_template('backups/index.html')
    return HttpResponse(html_template.render(context, request))



class index(ListView):
    model=Backups
    context_object_name ='backups_list'
    queryset =  Backups.objects.filter(Size__isnull=False).values('id','Comments','Location__LocationName','FileName','Size','Comments','CreationDate','Status__Description','Status_id')
    template_name='backups/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        num_backups=Backups.objects.all().count()
        ok_backups=Backups.objects.filter(Status__exact=1).count()
        data_size = Backups.objects.filter(Status__exact=1).aggregate(Sum('SizeMB'))['SizeMB__sum']
        data_size=round(data_size/1024,2)
        app='backups'
        view='index'
        context ['app']=app
        context['view']=view
        context['num_backups']= num_backups
        context['ok_backups']= ok_backups
        context['data_size']=data_size
        return context


        