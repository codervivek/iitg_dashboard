from django.shortcuts import render

# Create your views here.
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Student, Event, Page
from django.db.models import Max
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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


class StudentCreate(CreateView):
    model = Student
    fields=['user','rollNo','pages']
    success_url = reverse_lazy('home')

class PageDetailView(generic.DetailView):
    model=Page