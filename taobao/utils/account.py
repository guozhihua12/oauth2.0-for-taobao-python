__author__ = 'apple'

# coding=utf-8

from django.contrib.auth import get_backends
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def login_without_password(request, user):
    _user = user
    backend = get_backends()[0]
    _user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    auth_login(request, user)

def taobao_login(request, email, passwd):
    _user = authenticate(username=email, password=passwd)
    auth_login(request, _user)
    return _user


def _check_mail(email):
    try:
        User.objects.get(email=email)
        return False
    except User.DoesNotExist, e:
        return True
    return False
