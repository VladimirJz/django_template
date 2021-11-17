from typing import Tuple
from django.core.exceptions import RequestDataTooBig
from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.forms import modelformset_factory
from .models  import Backups, Jobs, Rotation
from django import forms
class BackupsForm(ModelForm):
    class Meta:
        model=Backups
        fields='__all__'

class RotationForm(ModelForm):
    class Meta:
        model=Rotation
        fields='__all__'

class StepForm(forms.Form):
    
    job=forms.IntegerField(required=True)
    order=forms.IntegerField(required=True);
    rule=forms.CharField(max_length=50,required=True);
    status_step=forms.IntegerField();
    location=forms.IntegerField(required=True);
    retention_days=forms.IntegerField (required=True);
    file_format=forms.CharField(max_length=5, required=True);


class BaseRotationFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        jobs=[]
        orders=[]
        rules=[]
        status=[]
        locations=[]
        retentions=[]
        formats=[]
        order_error = False
        for form in self.forms:
            if form.cleaned_data:
                job=form.cleaned_data['job']
                order = form.cleaned_data['order']
                rule = form.cleaned_data['rule']
                status_step=form.cleaned_data['status_step']
                location=form.claened_data['location']
                retention=form.cleaned_data['retention_days']
                file_format=form.cleaned_data['file_format']
                
                if order in orders:
                    order_error=True                
                orders.append(order)
                rules.append(rule)
                status.append(status_step)
                locations.append(location)
                retentions.append(retention)
                formats.append(file_format)
                jobs.append(job)


                if order_error:
                    raise forms.ValidationError(
                        'Verifique el orden de los pasos',
                        code='duplicate_order')

class step_form(ModelForm):
    class Meta:
      model  = Rotation
      fields = ["Job", "Order","Rule","Status","Location","RetentionDays","FileFormat"]

StepsFormSet = modelformset_factory(Rotation, 
            fields=("Job", "Order","Rule","Status","Location","RetentionDays","FileFormat")
            , extra=1)