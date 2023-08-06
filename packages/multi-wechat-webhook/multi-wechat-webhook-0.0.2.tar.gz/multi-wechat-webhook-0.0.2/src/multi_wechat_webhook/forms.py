# coding: utf-8

from django import forms


class WechatOptions(forms.Form):
    key = forms.CharField(
        max_length=255,
        help_text='Wechat Wrok robot webhook key'
    )
    prod_key = forms.CharField(
        max_length=255,
        help_text="生产企业微信webHookKey,为空则通过默认Key发送消息",
        required=False
    )
    noticeUser = forms.CharField(
        max_length=255,
        help_text="群里面@指定人,仅支持企业微信用户ID,提醒多人,号隔开",
        required=False
    )