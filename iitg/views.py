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

class PageDetailView(generic.DetailView):
    model=Page
    fields=['deadline', 'event', 'name', 'description']
    def get_success_url(self):
        page = self.object
        if self.request.user in page.admins.all:
            return render(request, 'home.html', {'page': page,'x':0})
        return reverse_lazy( 'professor_update', kwargs={'pk': professor.id})
    success_url=reverse_lazy('home')

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
