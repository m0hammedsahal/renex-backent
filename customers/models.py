from django.db import models
from users.models import User
from django.conf import settings 


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)



    
    class Meta:
        db_table = 'Customer_Customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ['-id']


    def __str__(self):
        return self.user.email