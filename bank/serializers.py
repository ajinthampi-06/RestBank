from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User,Account,Transaction


class UserRegSerializer(ModelSerializer):
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'username']

class LoginSeriailizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateAccountSerializer(ModelSerializer):
    class Meta:
        model=Account
        fields = ['acc_no','username','balance','account_type']


class WithdrawSerializer(serializers.Serializer):
    amount=serializers.IntegerField()



class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


class TransactionSerializer(serializers.Serializer):
    acc_no=serializers.IntegerField()
    to_acc_no=serializers.IntegerField()
    amount=serializers.IntegerField()
    date=serializers.DateField()
    def create(self, validated_data):
        acc_no=validated_data["acc_no"]
        account_obj=Account.objects.get(acc_no=acc_no)
        validated_data["acc_no"]=account_obj
        return Transaction.objects.create(**validated_data)