from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página principal
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', next_page='profile_redirect'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Cerrar sesión
    path ('profile_redirect/', views.profile_redirect, name='profile_redirect'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('classe/', views.classes, name='classes'),
    path('shop/', views.shop, name='shop'),
    path('class/create/', views.create_class, name='create_class'),  # Página para crear una nueva clase
    path('class/update/<int:class_id>/', views.update_class, name='update_class'),  # Página para actualizar una clase
    path('class/delete/<int:class_id>/', views.delete_class, name='delete_class'),  # Página para eliminar una clase
    path('enter_class/<int:class_id>/', views.enter_class, name='enter_class'),  # Página para entrar en una clase
    path('mission/create/<int:class_id>/', views.create_mission, name='create_mission'),  # Página para crear una nueva misión
    path('mission/update/<int:mission_id>/', views.update_mission, name='update_mission'),  # Página para actualizar una misión
    path('mission/delete/<int:mission_id>/', views.delete_mission, name='delete_mission'),  # Página para eliminar una misión
    path('class/join_class/', views.join_class, name='join_class'), #Página para unirte a una clase
    path('class/student_details/<int:student_id>/', views.student_details, name='student_details'), #Página para ver datos del alumno seleccionado
    path('student/update/<int:student_id>/', views.update_student, name='update_student'),
    path('student/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('shop/create/', views.create_item, name='create_item'),  # Página para crear un nuevo item
    path('shop/update/<int:item_id>/', views.update_item, name='update_item'),  # Página para actualizar un item
    path('shop/delete/<int:item_id>/', views.delete_item, name='delete_item'),  # Página para eliminar un item
    path('student/delete/<int:item_id>/<int:student_id>/', views.delete_item, name='delete_item_student'),  # Página para eliminar un item de un estudiante
    path('shop/buy/<int:item_id>/', views.buy_item, name='buy_item'), #Página para comprar un item
    path('student/update_profile/', views.update_student_profile, name='update_student_profile'),
]

