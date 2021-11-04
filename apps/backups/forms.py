from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from .models  import Backups, Rotation

class BackupsForm(ModelForm):
    class Meta:
        model=Backups
        fields='__all__'

class RotationForm(ModelForm):
    class Meta:
        model=Rotation
        fields='__all__'