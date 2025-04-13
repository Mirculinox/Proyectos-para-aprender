from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Teacher, Class, Mission, Item
from .forms import CustomUserCreationForm, ClassForm, MissionForm, StudentForm, ItemForm, StudentProfileUpdateForm

def home(request):
    return render(request, 'main/home.html')
def register(request):
    if request.method =='POST':
        # Verifica si la solicitud es una solicitud POST (lo que significa que el formulario ha sido enviado)
        form= CustomUserCreationForm(request.POST)
        #Crea una instancia del formulario UserCreationForm con los datos enviados.
        if form.is_valid(): #Verifica si los datos del formulario son válidos
            user= form.save() #Guarda el nuevo usuario en la base de datos.
            user.refresh_from_db() #Recarga el objeto del usuario desde la base de datos para asegurarse de
            #que cualquier perfil relacionado se cargue
            # Crear perfil de estudiante o profesor según el tipo de usuario
            if user.is_student:
                Student.objects.create(
                    user=user,
                    name=form.cleaned_data.get('name'),
                    surname=form.cleaned_data.get('surname'),
                    profile_image=form.cleaned_data.get('profile_image')
                )
            elif user.is_teacher:
                Teacher.objects.create(user=user,
                                       name=form.cleaned_data.get('name'),
                                       surname=form.cleaned_data.get('surname'))
                user.is_staff = True
            user.save()#Guarda cualquier cambio adicional
            raw_password = request.POST.get('password1')  # Obtiene la contraseña del formulario POST directamente
            # Mensajes de depuración
            print(f"Usuario guardado: {user.username}")
            print(f"Contraseña en texto plano: {raw_password}")
            user= authenticate(username=user.username, password=raw_password)#Autentica al usuario.
            # Mensajes de depuración
            if user is not None:
                print("Autenticación exitosa")
                return redirect('login')  # Redirige al usuario a la página de inicio
            else:
                print("Autenticación fallida")
        else:
            # Imprimir errores del formulario para depuración
            print("Errores del formulario", form.errors)
    else:#Si la solicitud no es POST, se crea un formulario vacío
        form= CustomUserCreationForm()
    return render(request, 'main/register.html', {'form':form})
    #Renderiza la plantilla register.html con el formulario.
# main/views.py

@login_required
def profile_redirect(request):
    print("Entró en profile_redirect")
    if request.user.is_student:
        print("Redirigiendo al perfil del estudiante")
        return redirect('student_profile')
    elif request.user.is_teacher:
        print("Redirigiendo al perfil del profesor")
        return redirect('teacher_profile')
    else:
        print("Redirigiendo a la página principal")
        return redirect('home')
@login_required  # Este decorador asegura que solo los usuarios autenticados puedan acceder a estas vistas.
def student_profile(request):
    print("Entró en student_profile")
    # Obtiene el perfil del estudiante asociado al usuario autenticado
    student = Student.objects.get(user=request.user)
    items=student.items.all()
    print(f"Perfil del estudiante: {student}")
    # Renderiza la plantilla 'student_profile.html' con el perfil del estudiante
    return render(request, 'main/student_profile.html', {'student': student, 'username': request.user.username, 'items':items})

@login_required  # Este decorador asegura que solo los usuarios autenticados puedan acceder a estas vistas.
def teacher_profile(request):
    # Obtiene el perfil del profesor asociado al usuario autenticado
    teacher =Teacher.objects.get(user=request.user)
    # Renderiza la plantilla 'teacher_profile.html' con el perfil del profesor
    return render(request, 'main/teacher_profile.html', {'teacher': teacher,'username': request.user.username})

##############################################################################################
@login_required
def classes(request):
     # Verifica si el usuario es un estudiante
    if request.user.is_student:
        # Obtiene las clases en las que está inscrito el estudiante
        student = Student.objects.get(user=request.user)
        classes = student.class_set.all()
    # Verifica si el usuario es un profesor
    elif request.user.is_teacher:
        # Obtiene las clases que maneja el profesor
        teacher = Teacher.objects.get(user=request.user)
        classes = Class.objects.filter(teacher=teacher)
    else:
        # Si el usuario no es ni estudiante ni profesor, no tiene clases
        classes = []

    # Renderiza la plantilla 'classes.html' con la lista de clases y el usuario actual
    return render(request, 'main/classes.html', {'classes': classes, 'user': request.user})

##############################################################################################

@login_required
def shop(request):
    if request.user.is_student:
        student=get_object_or_404(Student, user=request.user)
        items=Item.objects.filter(visible=True, xp_required__lte=student.xp)
    
    elif request.user.is_teacher:
        items= Item.objects.all()
    return render(request, 'main/shop.html', {'items':items})

@login_required
def create_item (request):
    if request.user.is_teacher:
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('shop')
        else:
            form = ItemForm()
        return render (request, 'main/create_item.html', {'form':form})
    else:
        return redirect('shop') 
     

@login_required
def update_item (request, item_id):
    item_instance=get_object_or_404(Item, id=item_id)
    if request.user.is_teacher:
        if request.method == 'POST':
            form= ItemForm(request.POST,request.FILES, instance=item_instance)
            if form.is_valid():
                item_instance.save()
                return redirect ('shop')
        else:
            form=ItemForm(instance=item_instance)
        return render(request, 'main/update_item.html', {'form':form})
    else:
        return redirect('shop')
    


@login_required
def delete_item (request, item_id, student_id=None):
    item_instance=get_object_or_404(Item, id=item_id)
    if request.user.is_teacher:
        if student_id:
            student= get_object_or_404(Student, id=student_id)
            student.items.remove(item_instance)
            student.save()
            return redirect('student_details', student_id=student.id)
        elif student_id==None and request.method=='POST':
            item_instance.delete()
            return redirect('shop')
        else:
            return render(request, 'main/delete_item.html', {'item': item_instance})
    else:
        return redirect('shop')

@login_required
def buy_item (request, item_id):
    item_instance=get_object_or_404(Item, id=item_id)
    if request.user.is_student:
        student=get_object_or_404(Student, user=request.user)
        print(f"Estudiante: {student.name} - Monedas actuales: {student.coins}")
        print(f"Intentando comprar: {item_instance.name} - Precio: {item_instance.price}")
        if student.coins >= item_instance.price:
            student.coins-=item_instance.price
            student.items.add(item_instance)
            student.save()
            print(f"Compra exitosa. Monedas restantes: {student.coins}")
            
        else:
            not_money=f"No tienes suficientes monedas para comprar {item_instance.name}"
            return render(request, 'main/shop.html', {'not_money': not_money, 'items': Item.objects.filter(visible=True, xp_required__lte=student.xp)})
    return redirect('shop')

##############################################################################################

@login_required
def create_mission (request, class_id):
    class_instance=get_object_or_404(Class, id=class_id )
    if request.method=='POST':
        form=MissionForm(request.POST, request.FILES)
        if form.is_valid():
            new_mission= form.save(commit=False)
            new_mission.class_assigned= class_instance
            new_mission.save()
        return redirect ('enter_class', class_id=class_id)
    else:
        form=MissionForm()
    return render(request, 'main/create_mission.html', {'form':form})

@login_required    
def update_mission(request, mission_id):
    mission_instance=get_object_or_404(Mission, id=mission_id)
    class_instance=mission_instance.class_assigned
    if request.user.is_teacher and class_instance.teacher.user == request.user:
        if request.method=='POST':
            form=MissionForm(request.POST, request.FILES, instance= mission_instance)
            if form.is_valid():
                mission_instance.save()
            return redirect ('enter_class', class_id=class_instance.id)
        else:
            form=MissionForm(instance=mission_instance)
    return render(request, 'main/update_mission.html', {'form':form})

@login_required     
def delete_mission(request, mission_id):
    mission_to_delete= get_object_or_404(Mission, id=mission_id)
    class_instance= mission_to_delete.class_assigned
    if request.user.is_teacher and class_instance.teacher.user == request.user:
        mission_to_delete.delete()
        return redirect('enter_class', class_id=class_instance.id)

##############################################################################################

@login_required
def create_class(request):
    if request.method == 'POST':
        form=ClassForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = Teacher.objects.get(user=request.user)
            new_class=Class(name= form.cleaned_data['name'], teacher=teacher)
            new_class.save()
            return redirect('classes')
    else:
        form=ClassForm()
    return render(request, 'main/create_class.html', {'form':form})
        
@login_required
def update_class(request, class_id):
    # Obtiene la clase que se desea actualizar o devuelve un error 404 si no se encuentra
    class_instance = get_object_or_404(Class, id=class_id)
    
    # Verifica que el usuario es un profesor y que la clase pertenece a ese profesor
    if request.user.is_teacher and class_instance.teacher.user == request.user:
        if request.method == 'POST':
            # Si el formulario ha sido enviado, lo instancia con los datos del POST y la instancia actual de la clase
            form = ClassForm(request.POST, request.FILES, instance=class_instance)
            if form.is_valid():
                # Si el formulario es válido, actualiza la clase con los datos del formulario
                class_instance.save()
                # Redirige a la lista de clases después de la actualización
                return redirect('classes')
        else:
            # Si la solicitud es GET, instancia el formulario con los datos de la clase actual
            form = ClassForm(instance=class_instance)
    else:
        # Si el usuario no es el profesor de la clase, redirige a la lista de clases
        return redirect('classes')
    
    # Renderiza la plantilla 'update_class.html' con el formulario
    return render(request, 'main/update_class.html', {'form': form})


@login_required  # Asegura que solo los usuarios autenticados puedan acceder a esta vista
def delete_class(request, class_id):
    # Obtiene la clase que se desea eliminar o devuelve un error 404 si no se encuentra
    class_to_delete = get_object_or_404(Class, id=class_id)
    # Verifica que el usuario es un profesor y que la clase pertenece a ese profesor
    if request.user.is_teacher and class_to_delete.teacher.user == request.user:
        # Usa el método delete_class del modelo Class para eliminar la clase
        class_to_delete.delete()
    # Redirige a la vista de lista de clases
    return redirect('classes')

@login_required
def enter_class(request, class_id):
    # Obtener la clase utilizando el ID de la clase
    class_instance = get_object_or_404(Class, id=class_id)
    
    # Inicializar la variable `missions`
    missions = []
    students=[]
    # Verificar si el usuario es estudiante
    if request.user.is_student:
        # Obtener el perfil del estudiante
        student = Student.objects.get(user=request.user)
        
        # Verificar si el estudiante está inscrito en la clase
        if student not in class_instance.students.all():
            # Obtener todas las misiones de la clase
            return redirect('classes')
            
    # Verificar si el usuario es profesor
    elif request.user.is_teacher:
        # Obtener el perfil del profesor
        teacher = Teacher.objects.get(user=request.user)
        
        # Verificar si el profesor es el profesor de la clase
        if teacher != class_instance.teacher:
            # Obtener todas las misiones de la clase
            return redirect('classes')
    
    # Determinar qué vista mostrar (misiones o estudiantes)
    view = request.GET.get('view', 'missions')
    print(f"View: {view}")  # Mensaje de depuración
    if view == 'missions':
        missions = class_instance.mission_set.all()
        print(f"Missions: {missions}")  # Mensaje de depuración
    elif view == 'students':
        students = class_instance.students.all()
        print(f"Students: {students}")  # Mensaje de depuración

    # Renderizar la plantilla con las misiones y el usuario actual
    return render(request, 'main/enter_class.html', {
        'missions': missions,
        'students': students,
        'class_instance': class_instance,
        'user': request.user,
        'class_id':class_instance.id,
        'view': view,
    })
    

@login_required
def join_class(request):
    if request.method=='POST':
        password=request.POST.get('password')
        try:
            class_instance=Class.objects.get(password=password)
            student=Student.objects.get(user=request.user)
            if student not in class_instance.students.all():
                class_instance.students.add(student)
                class_instance.save()
            else:
                messages.info(request, "Ya eres miembro de esta clase")
            return redirect('classes')
        except Class.DoesNotExist:
            return redirect ('classes')
    return render(request, 'main/join_class.html')

##############################################################################################

@login_required
def student_details(request,student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'main/student_details.html', {'student':student, 'student_id':student.id, 'class_id':student.class_set.first().id})

@login_required
def update_student (request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.user.is_teacher:
        if request.method=='POST':
            form = StudentForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_details', student_id=student.id)
        else:
            form=StudentForm(instance=student)
    else:
        return redirect('student_details', student_id=student.id)
    
    return render(request, 'main/update_student.html', {'form':form, 'student':student, 'student_id':student_id})

@login_required
def delete_student (request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.user.is_teacher:
        if request.method=='POST':
            student.delete()
            return redirect ('classes')
    return render(request, 'main/delete_student.html', {'student': student, 'student_id':student.id})

@login_required
def update_student_profile(request):
    student=get_object_or_404(Student, user=request.user)
    if request.method=='POST':
        form= StudentProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            print("Perfil actualizado correctamente.")
            return redirect('student_profile')
        else:
            print("Errores en el formulario:", form.errors)
    else:
        form=StudentProfileUpdateForm(instance=student)
    
    return render(request, 'main/update_student_profile.html', {'form':form})
