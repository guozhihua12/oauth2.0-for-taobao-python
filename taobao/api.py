__author__ = 'apple'

from django.conf import settings
from taobao.utils.sdk import APIClient

APP_KEY = getattr(settings, 'TAOBAO_APP_KEY', 'xxx')
APP_SECRET = getattr(settings, 'TAOBAO_APP_SECRET', 'xxx')
CALLBACK_URL = getattr(settings, 'TAOBAOCALLBACK_URL', 'http://www.xxx.com/taobao/auth')

def get_authorize_url():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    return client.get_authorize_url()

def show_me(code):
    if code is None:
        raise Exception('code is None')
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    taobao_user_nick = r.taobao_user_nick
    user_id = r.get('open_uid', '')
    client.set_access_token(access_token, expires_in)
    # return client.users.show.get(open_uid=user_id), access_token, expires_in
    return user_id, taobao_user_nick, access_token, expires_in

def unbind(access_token):
    if access_token is None:
        raise Exception('access token None')
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    # client.set_access_token(access_token, expires_in)
    return client.request_revoke(access_token)
    # return client.revokeoauth2.get()