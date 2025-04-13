from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Class, Mission, Student, Item
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=15, required=False)
    surname = forms.CharField(max_length=30, required=False)
    class Meta:
        model = Usuario
        fields = ('username', 'is_student', 'is_teacher', 'name', 'surname')
        labels={
            'username':'Nombre de usuario', 
            'is_student':'Soy estudiante', 
            'is_teacher': 'Soy profesor/a',
            'name': 'Nombre' ,
            'surname':'Apellidos'
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model=Class # Asociamos el formulario con el modelo 'Class'
        fields=['name', 'password'] # Incluimos el campo 'name' del modelo 'Class' en el formulario
        labels={
            'name': 'Nombre de la clase',
            'password': 'Código de inscripción'
        }

class MissionForm (forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model= Mission
        fields=['mission_image', 'title', 'description', 'class_assigned', 'xp_reward', 'coin_reward', 'health_penalty', 'document']
        labels = {
            'mission_image': 'Imagen',
            'title': 'Título de la misión',
            'description': 'Descripción',
            'class_assigned': 'Clase asignada',
            'xp_reward': 'Recompensa de XP',
            'coin_reward': 'Recompensa de monedas',
            'health_penalty':'Penalización de vida',
            'document':'Sube tu documento'
            
        }

class StudentForm (forms.ModelForm):
    class Meta:
        model=Student
        fields= ['name', 'surname', 'profile_image', 'xp', 'coins', 'health', 'absences']
        labels = {
            'name': 'Nombre',
            'surname': 'Apellidos',
            'profile_image': 'Imagen de Perfil',
            'xp': 'Puntos de Experiencia',
            'coins': 'Monedas',
            'health': 'Salud',
            'absences': 'Ausencias'
        }

class StudentProfileUpdateForm (forms.ModelForm):
    class Meta:
        model=Student
        fields= ['name', 'surname', 'profile_image']
        labels = {
            'name': 'Nombre',
            'surname': 'Apellidos',
            'profile_image': 'Imagen de Perfil'
        }

class ItemForm (forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model=Item
        fields=['item_image', 'name', 'description', 'price', 'visible', 'xp_required']
        labels={
            'item_image':'Imagen', 
            'name':'Nombre del objeto', 
            'description':'Descripción del objeto', 
            'price': 'Precio', 
            'visible':'Visible', 
            'xp_required': 'XP necesaria'
        }
    