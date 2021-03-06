from django.conf import settings
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
import requests


def send_email(email, link):
    """ Send email to user """
    html = """<html>
      <body>
        <p><a href="{}">Link</a> to login into website. Mark this message as not spam (otherwise link will not show)</p>
      </body>
    </html>
    """.format(link)
    return requests.post(
        settings.MAIL_GUN_API_LINK,
        auth=("api", settings.MAIL_GUN_API_TOKEN),
        data={"from": 'young-headland-52474@herokuapp.com',
              "to": [email],
              "subject": "Hello",
              "text": "_Link_ {} to login into website. Mark this message as not spam (otherwise link will not show)".format(link),
              "html": html}).json()


def signup_view(request):
    """ User signup """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('magic_link:home')
    else:
        form = RegistrationForm()
    return render(request, 'magic_link/signup.html', {'form': form})


def login_view(request):
    """ User login """
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
    """ Render main page """
    return render(request, 'magic_link/home.html')


def create_magic_link_view(request):
    """ Generate magic link for specific user """
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():  # Check if user with that email exists
            user = User.objects.get(email=email)

            token = get_random_string(50)  # create random string
            hash_object = hashlib.sha256(token.encode())
            token_hash = hash_object.hexdigest()  # create hash from random string

            link = request.build_absolute_uri(reverse('magic_link:handle_magic_link'))
            link += '?token=' + token  # create absolute url with token

            new_magic_link_obj = MagicLinkHash()
            new_magic_link_obj.user_id = user.id
            new_magic_link_obj.user_email = email
            new_magic_link_obj.token_hash = token_hash
            new_magic_link_obj.created_at = datetime.datetime.now()
            new_magic_link_obj.save()  # save information about magic link

            send_email(email, link)

        messages.success(request, 'Message was sent to your email')
        return redirect('magic_link:create_magic_link')
    else:
        form = EmailForm()
    return render(request, 'magic_link/receive_magic_link.html', {'form': form})


def handle_magic_link_view(request):
    """ Authenticate user with magic link """
    token = request.GET.get('token')

    if token:  # check if token parameter is exists
        hash_object = hashlib.sha256(token.encode())
        token_hash = hash_object.hexdigest()  # create hash from token

        if MagicLinkHash.objects.filter(token_hash=token_hash).exists():  # check hash existence
            magic_link_object = MagicLinkHash.objects.get(token_hash=token_hash)
            user_id = magic_link_object.user_id

            try:
                user = User.objects.get(id=user_id)  # get user that requested token
            except ObjectDoesNotExist:
                user = None

            if user is not None:
                if user.is_active:
                    magic_link_object.hits += 1
                    magic_link_object.save()

                    login(request, user)
                    return redirect('magic_link:home')
    raise Http404


def logout_view(request):
    """ Logout view """
    logout(request)
    return redirect('magic_link:home')


def protected_url_view(request):
    """ Simple view for logged users """
    if request.user.is_authenticated:
        return render(request, 'magic_link/protected.html')
    return redirect('magic_link:home')
