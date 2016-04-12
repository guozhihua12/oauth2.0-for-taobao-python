# -*- coding: utf-8 -*-
__author__ = 'apple'

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils.log import logger
from random import choice
from taobao import api
from taobao.models import Token
from taobao.utils.account import taobao_login, login_without_password


def gen_random_str(min_length=20, max_length=30, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        if min_length == max_length:
            length = min_length
        else:
            length = choice(range(min_length, max_length))

        return ''.join([choice(allowed_chars) for i in range(length)])

def auth(request):

    if request.method == "GET":

        _code = request.GET.get('code', None)
        try:
            (oauth_id, screen_name, access_token, expires_in) = api.show_me(_code)
        except :
            return render_to_response('weibo/invalid_grant.html',
                                      context_instance=RequestContext(request))
        logger.info("taobao token %s" %access_token)

        token = Token.objects.create_or_update(oauth_type=Token.Taobao, oauth_id=oauth_id, screen_name=screen_name,
                                               access_token=access_token, expires_in=expires_in)
        if token.user_id:
            login_without_password(request, token.user)
        else:
            user_name = 'tb_%s@epub360.com' % screen_name
            password = gen_random_str()
            user = User.objects.create_user(username=user_name, password=password)
            token.user=user
            token.save()
            taobao_login(request, user_name, password)

        # 跳转到网站的根目录，这里你可以设置授权成功后跳转uri
        return HttpResponseRedirect('/')


def login(request):
    url = api.get_authorize_url()
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url:
        logger.info(next_url)
    return HttpResponseRedirect(url)



