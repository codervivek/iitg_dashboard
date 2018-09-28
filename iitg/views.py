from django.shortcuts import render

# Create your views here.
from deep_player.forms import SignUpForm, UploadForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Student
from django.db.models import Max
from django.views import generic
from django.contrib.auth.models import User
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


class StudentCreate(CreateView):
    model = Student
    fields=['roll_No','pages']

