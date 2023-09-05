from django.db import models

# Create your models here.


#登録した人の属性
class Person(models.Model):
    family_name=models.CharField(max_length=100,null=False,blank=False,default='NO_NAME')
    first_name=models.CharField(max_length=100,null=False,blank=False,default='NO_NAME')
    email=models.EmailField(max_length=100,null=False,blank=False,default='no-adress@email.com')
    birthday=models.DateField(null=True,default=None)
    registered_date=models.DateTimeField(auto_now_add=True,null=True)
    image=models.ImageField(upload_to='person_image/',null=True,default=None)


    def __str__(self):
        return self.family_name+' '+self.first_name
    
#通過した時の記録
class Record(models.Model):
    person=models.ForeignKey(Person,null=True,on_delete=models.SET_NULL)#Personのデータを削除したらnullとなる
    date=models.DateTimeField(auto_now_add=True)#日付は山さんのデータでもらうかも

    def __str__(self):
        if self.person!=None:
            return str(self.id)+str(self.person)+str(self.date)
        else:
            return str(self.id)+'DELETED_PERSON'+str(self.date)





