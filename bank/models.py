from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    acc_no=models.IntegerField(unique=True)
    username=models.CharField(max_length=100)
    balance=models.IntegerField(default=0)
    account_type=models.CharField(max_length=50)

    def __str__(self):
        return str(self.acc_no)

class Transaction(models.Model):
    acc_no=models.ForeignKey(Account,on_delete=models.CASCADE)
    to_acc_no=models.IntegerField()
    amount=models.IntegerField()
    date=models.DateField(auto_now=True)



