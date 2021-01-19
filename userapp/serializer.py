from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from userapp.models import User, Employee


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "username": {
                "required": True,
                "min_length": 2,
            },
        }

    def validate(self, attrs):
        """对重复密码进行校验"""
        # TODO 对重复密码进行校验
        return attrs

    def validate_username(self, value):
        user = User.objects.filter(username=value).first()
        if user:
            raise serializers.ValidationError("用户名已存在")
        return value


class EmployeeModelSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "name", "salary", "full_img", "age", "img")

        extra_kwargs = {
            "full_img": {
                "read_only": True,
            },
            "img": {
                "write_only": True
            }
        }
