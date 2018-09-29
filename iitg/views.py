from django.shortcuts import render

# Create your views here.
from .forms import SignUpForm,CreatePageForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Student, Event, Page
from django.db.models import Max
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from iitg import models

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('student_create')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def home(request):
    student=Student.objects.get(pk=request.user.student.id)
    return render(request, 'home.html',{'student':student})

@login_required
def my_pages(request):
    student=Student.objects.get(pk=request.user.student.id)
    return render(request, 'my_pages.html',{'student':student})

class StudentCreate(CreateView):
    model = Student
    fields=['user','rollNo']
    success_url = reverse_lazy('home')


def page_detail(request,pk):
    page=Page.objects.get(pk=pk)
    # print(request.user)
    # print(list(page.admins.all()))
    if page.admins.filter(pk=request.user.id).exists():
        return render(request, 'iitg/page_detail.html', {'page': page,'x':'Add an event','y':'create_event'})
    return render(request, 'iitg/page_detail.html', {'page': page,'x':'Subscribe','y':'subscribe'})

def CreatePage(request):
    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            obj = models.Page(name= name , description=description)
            obj.save()
            user = Student.objects.get(user=request.user)
            obj.admins.add(user)
            obj.students.add(user)

            return redirect('home')
    else:
        form = CreatePageForm()
    return render(request, 'page_form.html', {'form': form})

class EventCreate(CreateView):
    model = Event
    fields=['name','description','time']
    def get_success_url(self):
        event = self.object
        print(self.kwargs)
        page=Page.objects.get(pk=self.kwargs['xy'])
        page.event.add(event)
        page.save()
        return reverse_lazy( 'home')

class PageListView(generic.ListView):
    model=Page