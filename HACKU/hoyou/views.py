from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Person,Record
from .forms import PersonRegistrationForm
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    context={}
    return render(request,'home.html',context)



def realtime(request):
    #この関数はまずしっかり出力されるかのテスト用なので後で直す
    records=[]
    ids=[]
    

    for num in ids:#本当はidがあるかどうかでtryする
        try:
            record=Record.objects.get(id=num)
            records.append(record)
        except ObjectDoesNotExist:
            return HttpResponse(num)


    context={"records":records}
    return render(request,'realtime.html',context)





def person_register(request):
    form=PersonRegistrationForm()
    if request.method=='POST':
        form=PersonRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            new_person=form.save(commit=False)
            new_person.save()
            '''Person.objects.create(
                family_name=request.POST.get('family_name'),
                first_name=request.POST.get('first_name'),
                email=request.POST.get('email'),
                birthday=request.POST.get('birthday'),
                image=request.FILES.get('image')
            )'''
            
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
        
    persons=Person.objects.filter(Q(first_name__icontains=q)|Q(family_name__icontains=q))
    persons_count=persons.count
    context={'persons':persons,'persons_count':persons_count}
    return render(request,'person_list.html',context)


def person_record(request,name,id):
    id=int(id)
    if request.method=='POST':
        if request.POST.get('delete_person')!=None:
            person=Person.objects.get(id=id)
            #削除の時に確認メッセージを入れる
            person.delete()
            return redirect('home')
    person=Person.objects.get(id=id)
    records=Record.objects.filter(person=person).order_by('-date')


    context={'records':records,'person':person}
    return render(request,'person_record.html',context)



def all_records(request):
    records=Record.objects.all().order_by('-date')
    context={'records':records}
    return render(request,'all_records.html',context)

