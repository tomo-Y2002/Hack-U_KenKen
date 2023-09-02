from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Person
from .forms import PersonRegistrationForm

# Create your views here.
def home(request):
    context={}
    return render(request,'home.html',context)

def realtime(request):
    #この関数はまずしっかり出力されるかのテスト用なので後で直す
    num=1 
    person=Person.objects.get(id=num)
    name=person.name
    #image=person.image
    context={"name":name}#,"image":image}
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

