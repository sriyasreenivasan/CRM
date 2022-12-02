from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.serializers import UserSerializer,CourseSerializer,BatchSerializer,StudentsSerializer,PlacementsSerializer
from api.models import Students,Course,Batches,Placements
from rest_framework import authentication,permissions
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
# Create your views here.
class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    permission_classes=[permissions.AllowAny]


class CourseView(ModelViewSet):
      serializer_class=CourseSerializer
      queryset=Course.objects.all()
      permission_classes=[permissions.IsAdminUser]


class BatchView(ModelViewSet):
      serializer_class=BatchSerializer
      queryset=Batches.objects.all()
      permission_classes=[permissions.IsAdminUser]
      def create(self, request, *args, **kw):
            course_id=request.query_params.get('course')
            course=Course.objects.get(id=course_id)
            serializer=BatchSerializer(data=request.data,context={'course':course})
            if serializer.is_valid():
             serializer.save()
             return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
class StudentView(ModelViewSet):
      serializer_class=StudentsSerializer
      queryset=Students.objects.all()
      permission_classes=[permissions.IsAdminUser]
      def create(self, request, *args, **kwargs):
        course=Course.objects.get(id=3)
        user=request.user

        serializer=StudentsSerializer(data=request.data, context={'user':request.user, 'course': course})
        #serializer = StudentsSerializer(data=request.data, context={'user': user, 'course': course})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
            
      @action(methods=['get'], detail=True)
      def add_batch(self, request, *args, **kwargs):
        student = self.get_object()
        batch_code = request.query_params.get('batch_code')
        try:
            batch = Batches.objects.get(batch_code=batch_code)
        except:
            return Response('No batch with this batch code')
        student.batchstudents_set.create(batch=batch)
        return Response('created')

      @action(methods=['POST'], detail=True)
      def add_placement(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = PlacementsSerializer(
            data=request.data, context={'student': student})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
            


      

      
    