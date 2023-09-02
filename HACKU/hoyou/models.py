from django.db import models

# Create your models here.


#登録した人の属性
class Person(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    #image=models.ImageField()


    def __str__(self):
        return self.name



