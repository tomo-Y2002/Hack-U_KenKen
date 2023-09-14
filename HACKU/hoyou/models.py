from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.

#登録した人の属性
class Person(models.Model):
    family_name=models.CharField(max_length=100,null=False,blank=False)
    first_name=models.CharField(max_length=100,null=False,blank=False)
    email=models.EmailField(max_length=100,null=False,blank=False)
    birthday=models.DateField(null=True,default=None)
    registered_date=models.DateTimeField(auto_now_add=True,null=True)
    image=models.ImageField(upload_to='person_image/',null=True,default=None)
    vector=PickledObjectField(null=True,blank=True)

    
    def __str__(self):
        return self.family_name+' '+self.first_name
class Shuttai(models.TextChoices):#出退勤、その他を記録
    shukkin='shukkin','出勤'
    taikin='taikin','退勤'
    sonota='sonota','その他'    
#通過した時の記録
class Record(models.Model):
    person=models.ForeignKey(Person,null=True,on_delete=models.SET_NULL)#Personのデータを削除したらnullとなる
    date=models.DateTimeField()#日付は山さんのデータでもらうかも
    shuttai=models.CharField(max_length=10,choices=Shuttai.choices,default=Shuttai.sonota)
    def __str__(self):
        if self.person!=None:
            return str(self.id)+str(self.person)+str(self.date)
        else:
            return str(self.id)+'DELETED_PERSON'+str(self.date)
        

'''class ChangeHistory: #削除と変更を考える
    record=models.ForeignKey(Record ,on_delete=models.SET_DEFAULT, default='DELETED_RECORD')
    date=models.DateTimeField(auto_now_add=True)'''




    




