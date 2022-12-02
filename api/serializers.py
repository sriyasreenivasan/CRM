from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Course,Batches,Students,BatchStudents,Placements


class UserSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        model=User
        fields=[
            "id",
            "username",
            "password"
            
        ]

    def create(self,validated_data):
       return User.objects.create_user(**validated_data)


class CourseSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    # is_active=serializers.CharField(read_only=True)
    class Meta:
        model=Course
        fields='__all__' #["id","course_name","fees","duration","is_active"]

    

class PlacementsSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    student = serializers.CharField(read_only=True)

    class Meta:
        model = Placements
        fields = '__all__'


    def create(self, validated_data):
        student = self.context.get('student')
        return student.placements_set.create(**validated_data)       



class BatchSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    course=serializers.CharField(read_only=True)
    
    class Meta:

        model=Batches
        fields=["id","course","batch_code","started_date","is_active"]
    def create(self,validated_data):
        course=self.context.get('course')
        return Batches.objects.create_user(**validated_data)

    
class StudentsSerializer(serializers.ModelSerializer):
    
    user=serializers.CharField(read_only=True)
    id=serializers.CharField(read_only=True)
    course=serializers.CharField(read_only=True)
    class Meta:
        model=Students
        fields='__all__'
    def create(self, validated_data):
        user=self.context.get('user')
        course=self.context.get('course')
        return Students.objects.create(**validated_data,user=user,course=course)
