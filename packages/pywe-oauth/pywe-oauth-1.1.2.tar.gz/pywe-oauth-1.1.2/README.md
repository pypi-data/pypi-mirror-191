# pywe-oauth

Wechat Oauth Module for Python.

# Installation

```shell
pip install pywe-oauth
```

# Usage

```python
from pywe_oauth import get_access_info, get_oauth_code_url, get_userinfo, get_component_access_info, get_component_oauth_code_url, get_component_userinfo, get_oauth_redirect_url
```

# Method

```python
def get_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, component=False, component_appid=None):

def get_access_info(self, appid=None, secret=None, code=None, component=False, component_appid=None, component_access_token=None):

def get_userinfo(self, access_token=None, openid=None, component=False):

def get_component_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, component_appid=None):

def get_component_access_info(self, appid=None, code=None, component_appid=None, component_access_token=None):

def get_component_userinfo(self, access_token=None, openid=None):

def get_oauth_redirect_url(self, oauth_uri, scope='snsapi_base', redirect_url=None, default_url=None, direct_redirect=None, random_str=True):
```

# Relative Libs
* [Django WeChat OAuth2/Share API](https://github.com/django-xxx/django-we)

# OAuth2 URL Examples
```
https://wx.com/oauth2?redirect_url=redirect_url
https://wx.com/oauth2?redirect_url=redirect_url&default_url=default_url
https://wx.com/oauth2?scope=snsapi_base&redirect_url=redirect_url
https://wx.com/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url
https://wx.com/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url&direct_redirect=true
```

# Backend Examples

* Django

  * settings.py
    ```python
    # Wechat Settings
    WECHAT = {
        'JSAPI': {
            'token': '5201314',
            'appID': '',
            'appsecret': '',
            'mchID': '',
            'apiKey': '',
            'mch_cert': '',
            'mch_key': '',
            'redpack': {
                'SEND_NAME': '',
                'NICK_NAME': '',
                'ACT_NAME': '',
                'WISHING': '',
                'REMARK': '',
            }
        },
    }

    WECHAT_OAUTH2_REDIRECT_URI = 'https://wx.com/wx_oauth2?scope={}&redirect_url={}'
    WECHAT_BASE_REDIRECT_URI = 'https://wx.com/base_redirect'
    WECHAT_USERINFO_REDIRECT_URI = 'https://wx.com/userinfo_redirect'
    ```

  * urls.py
    ```python
    # -*- coding: utf-8 -*-

    from django.conf.urls import include, url
    from wechat import views as wx_views

    urlpatterns = [
        url(r'^oauth2$', wx_views.wx_oauth2, name='wx_oauth2'),
        url(r'^base_redirect$', wx_views.base_redirect, name='base_redirect'),
        url(r'^userinfo_redirect$', wx_views.userinfo_redirect, name='userinfo_redirect'),
    ]
    ```

  * views.py
    ```python
    # -*- coding: utf-8 -*-

    from django.conf import settings
    from django.shortcuts import redirect
    from furl import furl
    from pywe_oauth import get_access_info, get_oauth_code_url, get_oauth_redirect_url, get_userinfo


    JSAPI = settings.WECHAT.get('JSAPI', {})


    def wx_oauth2(request):
        scope = request.GET.get('scope', 'snsapi_userinfo')
        redirect_url = request.GET.get('redirect_url', '')
        default_url = request.GET.get('default_url', '')

        if request.weixin:
            redirect_uri = settings.WECHAT_USERINFO_REDIRECT_URI if scope == 'snsapi_userinfo' else settings.WECHAT_BASE_REDIRECT_URI
            return redirect(get_oauth_code_url(JSAPI['appID'], redirect_uri, scope, redirect_url))

        return redirect(default_url or redirect_url)


    def base_redirect(request):
        """ snsapi_base cannot get unionid and userinfo """
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')

        access_info = get_access_info(JSAPI['appID'], JSAPI['appsecret'], code)
        if 'errcode' in access_info:
            return redirect(get_oauth_redirect_url(settings.WECHAT_OAUTH2_REDIRECT_URI, 'snsapi_base', state))

        return redirect(furl(state).add(access_info).url)


    def userinfo_redirect(request):
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')

        access_info = get_access_info(JSAPI['appID'], JSAPI['appsecret'], code)
        if 'errcode' in access_info:
            return redirect(get_oauth_redirect_url(settings.WECHAT_OAUTH2_REDIRECT_URI, 'snsapi_userinfo', state))

        userinfo = get_userinfo(access_info.get('access_token', ''), access_info.get('openid', ''))
        if 'openid' not in userinfo:
            return redirect(get_oauth_redirect_url(settings.WECHAT_OAUTH2_REDIRECT_URI, 'snsapi_userinfo', state))

        # Save Userinfo Or Other Handle
        # Some codes

        return redirect(furl(state).add(userinfo).url)
    ```
