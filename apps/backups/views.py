from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, request
from django.template import loader
from django.urls import reverse

from apps.backups.forms import RotationForm, BaseRotationFormSet, StepForm,step_form, StepsFormSet
from django.forms.formsets import BaseFormSet

from .models import Backups, Status,Locations,Rotation,Jobs
from django.db.models import Sum
from django.views.generic import ListView,TemplateView,DetailView

from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.urls import reverse_lazy




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
    queryset =  Backups.objects.filter(Size__isnull=False).values('id','Comments','Location__LocationName','FileName','Size','Comments','CreationDate','Status__Description','Status_id').order_by('-id')
    template_name='backups/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
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


class jobs(ListView):
    model=Jobs
    context_object_name ='jobs_list'
    queryset =  Jobs.objects.all()
    template_name='backups/jobs.html'
#paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
        app='backups'
        view='jobs'
        context ['app']=app
        context['view']=view
        return context




def rule_new(request):
    app='jobs'
    view='rule'
    context = {'app':app,'view':view}
    if request.method == "POST":
        form = RotationForm(request.POST)
      
        if form.is_valid():
            #conductor = form.save(commit=False)
            form.save()
            return render(request, 'backups/success.html', {'form': form})
        else:
            return render(request, 'backups/rule.html', {'form': form})
    else:
        form = RotationForm()
    return render(request, 'backups/rule.html', {'form': form,'app':app,'view':view})



def rotation_rules(request):
    rotation_formset=formset_factory(StepForm,formset=BaseRotationFormSet)
    current_steps=Rotation.objects.filter(Job=1).order_by('Order')
    if current_steps:
        steps_detail=[{'job': l.Job_id, 'order': l.Order,'rule':l.Rule,'status_step':l.Status,'location':l.Location_id,'retentention_days':l.RetentionDays,'file_format':l.FileFormat} 
                    for l in current_steps]
    else:
        steps_detail=[{'job': 0, 'order':1,'rule':'','status_step':1,'location':1,'retentention_days':0,'file_format':'.bak'} ]

    if request.method=='POST':
        steps_forms= rotation_formset(request.POST)
        if steps_forms.is_valid():
            new_steps=[]
            for step_form in steps_forms:
                job=step_form.cleaned_data.get('job')
                order=step_form.cleaned_data.get('order')
                rule=step_form.cleaned_data.get('rule')
                status=step_form.cleaned_data.get('status_step')
                location=step_form.cleaned_data.get('location')
                retention=step_form.cleaned_data.get('retention_days')
                file_format=step_form.cleaned_data.get('file_format')
                new_steps.append(Rotation(Job=job,Order=order,Rule=rule,Status=status,Location=location,RetentionDays=retention,FileForma=file_format))

            try:
                with transaction.atomic():
                    #Rotation.objects.filter(Job=1).delete()
                    #Rotation.objects.bulk_create(new_steps)
                    messages.success(request, 'Job Actualizado')
            except IntegrityError: #If the transaction failed
                messages.error(request, 'Ocurrio un error.')
                return redirect(reverse('profile-settings'))


    else: # get
        steps_forms=rotation_formset(initial=steps_detail)
    
    context={'steps_forms':steps_forms}
    
    return render(request, 'backups/job_steps.html', context)



class steps_listview(ListView):
    model=Rotation
    template_name='backups/step_list.html'


class StepAddView(TemplateView):
    template_name = "backups/add_step.html"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = StepsFormSet(queryset=Rotation.objects.filter(Job=self.kwargs['pk']).order_by('Order'))
        return self.render_to_response({'step_formset': formset})
    
    def post(self, *args, **kwargs):

        formset = StepsFormSet(data=self.request.POST)
        #
        # Check if submitted forms are valid
        if formset.is_valid():
            
            formset.save()
            return redirect(reverse_lazy("step_list"))
        else:
            formset.clean()
        return self.render_to_response({'step_formset': formset})