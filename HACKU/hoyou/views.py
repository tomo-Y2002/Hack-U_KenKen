from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Person,Record
from .forms import PersonRegistrationForm
from django.db.models import Q

# Create your views here.
def home(request):
    context={}
    return render(request,'home.html',context)



def realtime(request):
    #この関数はまずしっかり出力されるかのテスト用なので後で直す
    nums=[1,1,2,3]
    ids=[]
    records=[]
    for num in nums:
        passedperson=Person.objects.get(id=num)
        new_record=Record.objects.create(person=passedperson)#Recordオブジェクトの作成
        ids.append(new_record.id)

    for num in ids:#本当はidがあるかどうかでtryする
        record=Record.objects.get(id=num)
        records.append(record)

    context={"records":records}
    return render(request,'realtime.html',context)




def person_register(request):
    form=PersonRegistrationForm()
    if request.method=='POST':
        form=PersonRegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            Person.objects.create(
                name=request.POST.get('name'),
                #image=request.POST.get('image')
            )
            return redirect('home')
        else:
            messages.error(request, 'An error occurred')
    context={'form':form}
    return render(request,'person_register.html',context)



def person_list(request):
    #id取得用の仮インスタンス
    if request.GET.get('q')!=None:
        q=request.GET.get('q')
    else:
        q=''
        
    persons=Person.objects.filter(Q(name__icontains=q))
    context={'persons':persons}
    return render(request,'person_list.html',context)


def person_record(request,name):
    person=Person.objects.get(name=name)
    records=Record.objects.filter(person=person)

    
    context={'records':records,'person':person}
    return render(request,'person_record.html',context)

