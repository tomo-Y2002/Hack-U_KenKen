from django.db import models

# Create your models here.


#登録した人の属性
class Person(models.Model):
    name = models.CharField(max_length=100,blank=False,null=False)
    #image=models.ImageField()


    def __str__(self):
        return self.name
    
#通過した時の記録
class Record(models.Model):
    person=models.ForeignKey(Person,null=True,on_delete=models.SET_NULL)#Personのデータを削除したらnullとなる
    date=models.DateTimeField(auto_now_add=True)#日付は山さんのデータでもらうかも





