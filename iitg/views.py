from django.shortcuts import render

# Create your views here.
from .forms import SignUpForm,CreatePageForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Student, Event, Page, Deadline
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

@login_required
def page_detail(request,pk):
    page=Page.objects.get(pk=pk)
    # print(request.user)
    # print(list(page.admins.all()))
    if page.admins.filter(pk=request.user.id).exists():
        return render(request, 'iitg/page_detail.html', {'page': page,'x':'Add an event','y':'create_event'})
    return render(request, 'iitg/page_detail.html', {'page': page,'x':'Subscribe','y':'subscribe'})

@login_required
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
            obj.save()

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
        return reverse_lazy('home')

class DeadlineCreate(CreateView):
    model = Deadline
    fields=['name','totalTime','description','deadline']
    def get_success_url(self):
        deadline = self.object
        print(self.kwargs)
        page=Page.objects.get(pk=self.kwargs['xy'])
        page.deadline.add(deadline)
        page.save()
        return reverse_lazy('home')

class PageListView(generic.ListView):
    model=Page

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt 
def appkey(request):
    json_data = json.loads(request.body.decode("utf-8"))
    user=User.objects.filter(email=json_data['email'])
    return JsonResponse({'key':user.first().id})

def subscribe(request,pk):
    page=Page.objects.get(pk=pk)
    page.students.add(request.user.student)
    return render(request,'subscribe.html')

def listing(request):
    events = Event.objects.annotate(
        t=Max("time")
    ).order_by("-t")
    deadlines = Deadline.objects.annotate(
        t=Max("deadline")
    ).order_by("-t")
    
    # list=[]
    # z=0
    print(list(events))
    print(deadlines)
    # cur_deadline=deadline.first()
    # answer_ids = set(answer.id for answer in events)
    # existing_question_answers = filter(lambda x: x.answer.id not in answers_id, existing_question_answers)
    # print(existing_question_answers)
    # for event in events:
    #     while(dea)
    return JsonResponse({'success':'true'})