from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Person,Record
from .forms import PersonRegistrationForm,YesNoForm
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/manager_login')
# Create your views here.
def home(request):
    context={}
    return render(request,'home.html',context)



def manager_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')  
        try:
            manager=User.objects.get(username=username)
        except:
            HttpResponse('user does not exist')
        manager=authenticate(request,username=username,password=password)
        if manager is not None:
            login(request,manager)
            return redirect('home')
        else:
            return HttpResponse('username or password is wrong')          
    context={}
    return render(request,'manager_login.html',context)


@login_required(login_url='/manager_login')
def manager_logout(request):
    logout(request)
    return redirect('manager_login')




@login_required(login_url='/manager_login')
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




@login_required(login_url='/manager_login')
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


@login_required(login_url='/manager_login')
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



@login_required(login_url='/manager_login')
def person_record(request,name,id):
    id=int(id)
    person=Person.objects.get(id=id)
    if request.method=='POST':
        
        if request.POST.get('delete_person')!=None:
            #削除の時に確認メッセージを入れる
            person.delete()
            return redirect('home')
        

    records=Record.objects.filter(person=person).order_by('-date')

    context={'records':records,'person':person}
    return render(request,'person_record.html',context)



@login_required(login_url='/manager_login')
def person_modify(request,name,id):
    id=int(id)
    person=Person.objects.get(id=id)
    form=YesNoForm()
    if request.method=='POST':
        form=YesNoForm(request.POST)
        if form.is_valid():
            person.family_name=request.POST.get('family_name')
            person.first_name=request.POST.get('first_name') 
            person.email=request.POST.get('email')     
            person.birthday=request.POST.get('birthday')

            if form.cleaned_data['choice'] == 'no':
                pass
            else:
                #いらない写真を消す機能が必要かも
                person.image=request.FILES.get('image')
            person.save()

            records=Record.objects.filter(person=person).order_by('-date')
            context={'person':person,'records':records}

            return render(request,'person_record.html',context)
        else:
            return HttpResponse('form is not valid')

    context={'person':person,'form':form}
    return render(request,'person_modify.html',context)


@login_required(login_url='/manager_login')
def all_records(request):
    records=Record.objects.all().order_by('-date')
    context={'records':records}
    return render(request,'all_records.html',context)



@login_required(login_url='/manager_login')
def delete_modify_records(request):


    context={}
    return render(request,'delete_modify_records.html',context)

