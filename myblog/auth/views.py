from django.shortcuts import render, HttpResponse, get_object_or_404
from .MyForms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {'user': user})

