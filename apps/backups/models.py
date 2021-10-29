from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class ServerTypes(models.Model):
    Name=CharField(max_length=50,help_text='Tipo de Servidor');
    Version=CharField(max_length=10,help_text='Version',null=True)



class Servers(models.Model):
    Name=models.CharField( max_length=50,help_text='Nombre del Servidor');
    IP=models.CharField(max_length=20,help_text='IP del servidor');
    ServerType=models.ForeignKey(ServerTypes,on_delete=models.SET_NULL,null=True);


class Databases(models.Model):
    DatabaseName=models.CharField(max_length=20,help_text='Nombre de la BD');
    FriendlyName=models.CharField(max_length=50,help_text='Alias de la BD')
    Server=ForeignKey(Servers,on_delete=models.SET_NULL,null=True);

class Jobs(models.Model):
    JobName=models.CharField(max_length=50,help_text='Nombre del la Rutina');

class Locations(models.Model):
    LocationName=models.CharField(max_length=50,help_text='Nombre de la Ubicación');
    FilesPath=models.CharField(max_length=200,help_text='Ubicación fisica')    

class Status(models.Model):
    Status=models.CharField(max_length=20,help_text='Estatus');
    Description=models.CharField(max_length=200,help_text='Descripcion del Status')

class Backups(models.Model):
    Database=models.ForeignKey(Databases,on_delete=models.SET_NULL,null=True);
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True);
    Status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True);
    Location=models.ForeignKey(Locations,on_delete=models.SET_NULL,null=True);
    CreationDate=models.DateField(null=True,blank=True,help_text='Fecha de Creación');
    StartBackup=models.DateTimeField(null=True,blank=True,help_text='Inicio de generación del backup');
    EndBackup=models.DateTimeField(null=True,blank=True,help_text='Terminación del Backup');
    FileName=models.CharField(max_length=100,help_text='Nombre del archivo');
    SizeMB=models.DecimalField(max_digits=20,decimal_places=2,help_text='Tamaño en MB');
    Size=models.BigIntegerField(help_text='Tamaño');
    Comments=models.TextField(help_text='Comentarios')

    def __str__(self):
            return self.FileName

