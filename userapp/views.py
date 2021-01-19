from django.shortcuts import render

# Create your views here.
from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from userapp.models import User, Employee
from userapp.serializer import UserModelSerializer, EmployeeModelSerializer
from utils.response import APIResponse


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        username = request.query_params.get("username")
        password = request.query_params.get("password")

        user_obj = User.objects.filter(username=username, password=password).first()

        if user_obj:
            data = UserModelSerializer(user_obj).data
            return Response({"results": data, "message": True}, status=status.HTTP_200_OK)

        return Response({"results": "登录参数有误", "message": False}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()

        return Response({"results": UserModelSerializer(user_obj).data})

class EmployeeAPIView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      RetrieveModelMixin,
                      GenericAPIView,
                      UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      PageNumberPagination):
    queryset = Employee.objects.all()
    serializer_class = EmployeeModelSerializer
    lookup_field = "id"
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 5

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        return APIResponse(results=response.data)

