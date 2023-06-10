from django.contrib import admin
from UserApp.models import *
from django.contrib.auth.hashers import make_password
from django.utils import timezone


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname','phoneNumber','adress','username','birthdate','gender','payement_method','payed','type')
    fields = ['firstname', 'lastname','phoneNumber','adress','username','password','birthdate','gender','payement_method'] 

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password:
            obj.password = make_password(password)
            
        today = timezone.now().date()
        if(obj.payement_method == 'Freemuim'):
            obj.attemps = 3
            obj.payed = False
            obj.payment_date = None
        elif (obj.payement_method == 'Yearly'):
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        else:
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        obj.type = 'SIMPLE_USER'
        obj.save()

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname','phoneNumber','adress','username','birthdate','gender','payement_method','payed','matricule','email','type')
    fields = ['firstname', 'lastname','phoneNumber','adress','username','password','birthdate','gender','payement_method','matricule','email'] 
    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password:
            obj.password = make_password(password)
        
        today = timezone.now().date()
        if(obj.payement_method == 'Freemuim'):
            obj.attemps = 3
            obj.payed = False
            obj.payment_date = None
        elif (obj.payement_method == 'Yearly'):
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        else:
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        obj.type = 'TEACHER'
        obj.save()

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('id','firstname','lastname','phoneNumber','adress','username','birthdate','gender','payement_method','payed','matricule','email','type')
    fields = ['firstname', 'lastname','phoneNumber','adress','username','password','birthdate','gender','payement_method','matricule','email'] 

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password:
            obj.password = make_password(password)

        today = timezone.now().date()
        if(obj.payement_method == 'Freemuim'):
            obj.attemps = 3
            obj.payed = False
            obj.payment_date = None
        elif (obj.payement_method == 'Yearly'):
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        else:
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        obj.type = 'PARENT'
        obj.save()

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname','phoneNumber','adress','username','birthdate','gender','payement_method','payed','matricule','type')
    fields = ['firstname', 'lastname','phoneNumber','adress','username','password','birthdate','gender','payement_method','matricule','grade','father']
    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password:
            obj.password = make_password(password)
        
        today = timezone.now().date()
        if(obj.payement_method == 'Freemuim'):
            obj.attemps = 3
            obj.payed = False
            obj.payment_date = None
        elif (obj.payement_method == 'Yearly'):
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        else:
            obj.attemps = -1
            obj.payed = True
            obj.payment_date = today
        obj.type = 'STUDENT'
        obj.save()

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('level','designiation')

class MyModelReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ('id','questions','types', 'answer','correctAnswers','note','student')
    list_display = ('id', 'questions','types','answer','correctAnswers','note','student')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Quiz, MyModelReadOnlyAdmin)
# Register your models here.


