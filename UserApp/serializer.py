from rest_framework import serializers
from UserApp.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('__all__')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields =('__all__')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =('__all__')

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields =('__all__')

class CreateTeacherSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Teacher
        fields = ('__all__')
