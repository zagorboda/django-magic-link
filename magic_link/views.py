from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.urls import reverse

from .forms import RegistrationForm, EmailForm
from .models import MagicLinkHash

import datetime
import hashlib


def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('magic_link:home')
    else:
        form = RegistrationForm()
    return render(request, 'magic_link/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('magic_link:home')
        else:
            messages.error(request, 'Username or password not correct')
            return redirect('magic_link:login')
    else:
        form = AuthenticationForm()
    return render(request, 'magic_link/login.html', {'form': form})


def home_view(request):
    return render(request, 'magic_link/home.html')


def create_magic_link_view(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            token = get_random_string(50)
            hash_object = hashlib.sha256(token.encode())
            token_hash = hash_object.hexdigest()

            link = request.build_absolute_uri(reverse('magic_link:handle_magic_link'))
            link += '?token=' + token

            new_magic_link_obj = MagicLinkHash()
            new_magic_link_obj.user_id = user.id
            new_magic_link_obj.user_email = email
            new_magic_link_obj.token_hash = token_hash
            new_magic_link_obj.created_at = datetime.datetime.now()
            new_magic_link_obj.save()

            # Send email with token link

        messages.success(request, 'Message was sent to your email')
        return redirect('magic_link:create_magic_link')
    else:
        form = EmailForm()
    return render(request, 'magic_link/receive_magic_link.html', {'form': form})


def handle_magic_link_view(request):
    token = request.GET.get('token')

    if token:
        hash_object = hashlib.sha256(token.encode())
        token_hash = hash_object.hexdigest()

        if MagicLinkHash.objects.filter(token_hash=token_hash).exists():
            magic_link_object = MagicLinkHash.objects.get(token_hash=token_hash)
            user_id = magic_link_object.user_id

            magic_link_object.hits += 1
            magic_link_object.save()

            try:
                user = User.objects.get(id=user_id)
            except ObjectDoesNotExist:
                user = None

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('magic_link:home')
    raise Http404


def logout_view(request):
    logout(request)
    return redirect('magic_link:home')


def protected_url_view(request):
    if request.user.is_authenticated:
        return render(request, 'magic_link/protected.html')
    return redirect('magic_link:home')
