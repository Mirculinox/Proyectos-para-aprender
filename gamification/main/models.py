from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField()
    price = models.IntegerField(default=0)
    xp_required=models.IntegerField(default=0)
    visible= models.BooleanField(default=True)
    item_image= models.ImageField(upload_to='images/', default= False, null=True, blank=True)

class Usuario(AbstractUser):
    is_student= models.BooleanField (default=False)
    is_teacher= models.BooleanField (default=False)
    #Aquí creamos la clase user para asignarla luego a alumno y profesor. Y
    #asi de esta forma, gestionaremos los usuarios desde aqui"""
class Student(models.Model):
    user= models.OneToOneField(Usuario, on_delete=models.CASCADE)
    # Si el User es eliminado, el Student asociado también será eliminado.
    name= models.CharField (max_length= 15)
    surname = models.CharField(max_length=30)
    xp= models.IntegerField(default=0)
    coins= models.IntegerField(default=0)
    health= models.IntegerField(default=100)
    absences= models.IntegerField(default=0)
    items=models.ManyToManyField(Item, blank=True)
    profile_image= models.ImageField(upload_to='images/', default= False, null=True, blank=True)
class Teacher(models.Model):
    user= models.OneToOneField(Usuario, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=30)



class Class(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    # Una clase puede tener muchos estudiantes y un estudiante puede estar en muchas clases.
    teacher= models.ForeignKey(Teacher, on_delete=models.CASCADE)
    password=models.CharField(max_length=15, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name #hacemos esto para que al ver las clases en un menú nos salga el nombre y no class object


class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    xp_reward = models.IntegerField()
    coin_reward = models.IntegerField()
    health_penalty = models.IntegerField(default=0)
    mission_image= models.ImageField(upload_to='images/', default=False, null=True, blank=True)
    document=models.FileField(upload_to='mission_pdfs/', null=True,blank=True)

    