from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Person,Record
from .forms import PersonRegistrationForm,YesNoForm
from .functions import get_datetime
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required(login_url='/manager_login')
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

def manager_register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if username==None or email==None or password1==None or password2==None:
            return HttpResponse('fill all fields')
        elif password1!=password2:
            return HttpResponse('password does not match')
        
        password=password1
        manager=User.objects.create(username=username,email=email,password=password)

        login(request,manager)
        return redirect('home')

    context={}
    return render(request,'manager_register.html',context)


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
    if request.GET.get('search')!=None:
        if request.GET.get('q')!=None:
            q=request.GET.get('q')
        else:
            q=''
        q_condition=Q(first_name__icontains=q)|Q(family_name__icontains=q)
        persons=Person.objects.filter(q_condition)
        person_condition= Q(person__in=persons)
        shuttai=request.GET.get('shuttai')
        if shuttai!='no_choice':
            shuttai_condition= Q(shuttai=shuttai)
        else:
            shuttai_condition=Q(shuttai__icontains='')

        start_date = request.GET.get('start_date') if request.POST.get('start_date')!=None else "2000-01-01"
        start_time = request.GET.get('start_time') if request.POST.get('start_time')!=None else "00:00"
        start_datetime=get_datetime(start_date,start_time)
        if request.POST.get('end_date')!=None:
            end_date = request.GET.get('end_date') 
        else:
            end_datetime=datetime.now()
            end_date=end_datetime.date()
            end_date=end_date.strftime('%Y-%m-%d')
        end_time = request.GET.get('start_time') if request.POST.get('start_time')!=None else "23:59"
        end_datetime=get_datetime(end_date,end_time)
        print(start_datetime,end_datetime)
        datetime_condition=Q(date__gte=start_datetime)&Q(date__lte=end_datetime)
        records=Record.objects.filter(person_condition & shuttai_condition & datetime_condition)
    else:
        records=Record.objects.all().order_by('-date')
    context={'records':records}
    return render(request,'all_records.html',context)


@login_required(login_url='/manager_login')
def change_records(request,id):
    id=str(id)
    record=Record.objects.get(id=id)
    persons=Person.objects.all()
    if request.method=="POST":
        if request.POST.get('change')!=None:
            new_person_id=int(request.POST.get('person'))
            try:
                new_person=Person.objects.get(id=new_person_id)
            except:
                HttpResponse('person does not exist')
            new_shuttai=request.POST.get('shuttai')
            record.person=new_person
            record.shuttai=new_shuttai
            record.save()
            return redirect('all_records')
        elif request.POST.get('delete')!=None:
            record.delete()
            return redirect('all_records')
    
    context={'record':record,'persons':persons}
    return render(request,'change_records.html',context)

@login_required(login_url='/manager_login')
def add_records(request):
    persons=Person.objects.all()
    if request.method=='POST':
        id=int(request.POST.get('person'))
        person=Person.objects.get(id=id)
        shuttai=request.POST.get('shuttai')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # 日付のフォーマットに合わせる
        time_obj = datetime.strptime(time_str, '%H:%M')  # 時間のフォーマットに合わせる
        combined_datetime = datetime.combine(date_obj.date(), time_obj.time())
        Record.objects.create(person=person,shuttai=shuttai,date=combined_datetime)
        return redirect('all_records')
    context={'persons':persons}
    return render(request,'add_records.html',context)




@login_required(login_url='/manager_login')
def delete_modify_history(request):
    context={}
    return render(request,'delete_modify_history.html',context)










