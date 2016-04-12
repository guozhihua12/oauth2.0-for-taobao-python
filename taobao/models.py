# coding=utf-8
__author__ = 'apple'

from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import ugettext_lazy as _

class TokenManger(models.Manager):
    def create_or_update(self, oauth_type, oauth_id,screen_name, access_token, expires_in):
        try:
            token = self.get(oauth_type=oauth_type, oauth_id=oauth_id)
            token.screen_name = screen_name
            token.access_token = access_token
            token.expires_in = expires_in
            token.save()
        except Exception, e:
            token = self.create(oauth_type=oauth_type,
                                oauth_id=oauth_id,
                                screen_name=screen_name,
                                access_token=access_token,
                                expires_in=expires_in)
        finally:
            return token

    def update_user_id(self, oauth_id, user_id):
        token = self.get(oauth_id=oauth_id)
        token.user_id = user_id
        token.save()

class Token(models.Model):
    Weibo = u'M'
    QQ = u'Q'
    Taobao = u'T'
    OAUTH_CHOICES = ((Weibo, u'微博'),
                     (QQ,  u'qq'),
                     (Taobao, u'淘宝'))
    user = models.OneToOneField(User, related_name="taobao", null=True)
    oauth_type = models.CharField(max_length=2, choices=OAUTH_CHOICES)
    oauth_id = models.CharField(max_length=64, unique=True)
    screen_name = models.CharField(max_length=30)
    access_token = models.CharField(max_length=128)
    expires_in = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, editable=False, db_index=True)
    objects = TokenManger()

    def __unicode__(self):
        return self.oauth_id