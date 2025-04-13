from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Student, Teacher, Class, Mission, Item

admin.site.register(Usuario, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Mission)
admin.site.register(Item)
