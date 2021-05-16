from django.shortcuts import render
from .models import User
from .serializers import UserRegSerializer,LoginSeriailizer,CreateAccountSerializer,WithdrawSerializer,DepositSerializer,TransactionSerializer
from rest_framework.views import APIView
from rest_framework import generics,mixins,status,authentication,permissions
from django.contrib.auth import login,logout,authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Account,Transaction

# Create your views here.

class UserRegisterView(generics.GenericAPIView,mixins.CreateModelMixin):
    serializer_class = UserRegSerializer
    def post(self,request):
        return self.create(request)

class UserLoginview(APIView):
    def post(self,request):
        serializer=LoginSeriailizer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get("password")
            user=User.objects.get(username=username)
            if (user.username==username)&(user.password==password):
                login(request,user)
                token,created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key},status=204)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)


class LogoutApi(APIView):
    def get(self,request):
        logout(request)
        request.user.auth_token.delete()

class CreateAccountView(generics.GenericAPIView,mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    parser_classes = [IsAuthenticated]
    serializer_class =CreateAccountSerializer
    def get(self,request):
        acc_no=Account.objects.last()
        if acc_no:
            acc_no=acc_no+1
        else:
            acc_no=1000
            return Response({"acc_no":"Account Number:"+str(acc_no)})

    def post(self,request):
        return self.create(request)




class Balance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,acc_no):
        acc_no=Account.objects.get(acc_no=acc_no)
        serializer=CreateAccountSerializer(acc_no)
        return Response(serializer.data)


class Withdrawview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self,request,acc_no):
        serializer=WithdrawSerializer
        acc_no=Account.objects.get(acc_no=acc_no)
        if serializer.is_valid():
            amount=serializer.validated_data.get("amount")
            if amount<acc_no.balance:
                acc_no.balance-=amount
                acc_no.save()
                return Response({"messege": "Amount Debited, balance is " + str(acc_no.balance)})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)




class Depositview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,acc_no):
        serializer=DepositSerializer
        acc_no=Account.objects.get(acc_no=acc_no)
        if serializer.is_valid():
            amount=serializer.validated_data.get("amount")
            acc_no.balance+=amount
            acc_no.save()
            return Response({"messege": "Amount  Credited, balance is " + str(acc_no.balance)})


        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class Transactionview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,acc_no):
        accno_obj = Account.objects.get(acc_no=acc_no)
        debit_transaction = Transaction.objects.filter(acc_no=accno_obj)
        print(debit_transaction)
        credit_transaction = Transaction.objects.filter(to_acc_no=acc_no)
        serializer1 = TransactionSerializer(debit_transaction, many=True)
        serializer2 = TransactionSerializer(credit_transaction, many=True)
        return Response({"All Debit Transactions ": serializer1.data, "All  credit transaction": serializer2.data},status=status.HTTP_200_)


    def post(self,request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            accno = serializer.validated_data.get("acc_no")
            to_acc_no= serializer.validated_data.get("to_acc_no")
            amount = serializer.validated_data.get("amount")
            accno_obj = Account.objects.get(accno=accno)
            r_acno_obj = Account.objects.get(accno=to_acc_no)
            if amount <= (accno_obj.balance):
                serializer.save()
                accno_obj.balance -= amount
                r_acno_obj.balance += amount
                accno_obj.save()
                r_acno_obj.save()
                return Response({"msg ": str(amount) + " has been sent to acno: " + str(to_acc_no)})
            else:
                return Response({"No Sufficient balance"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





