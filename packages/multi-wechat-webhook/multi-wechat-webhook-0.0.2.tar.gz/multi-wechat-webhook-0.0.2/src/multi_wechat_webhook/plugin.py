'''
@Author: Whzcorcd
@Date: 2020-06-08 09:15:49
@LastEditors: Wzhcorcd
@LastEditTime: 2020-06-08 14:15:18
@Description: file content
'''
# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

from .forms import WechatOptions

WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"

class WechatPlugin(NotificationPlugin):
    """
    Sentry extension to Share information to Wechat Work.
    """
    author = 'badx'
    author_url = 'https://github.com/badx/multi-wechat-webhook'
    version = "0.0.2"
    description = 'Share information to Wechat Work.'
    resource_links = [
        ('Source', 'https://github.com/badx/multi-wechat-webhook'),
        ('Bug Tracker', 'https://github.com/badx/multi-wechat-webhook/issues'),
        ('README', 'https://github.com/badx/multi-wechat-webhook/blob/master/README.md'),
    ]

    slug = 'Wechat HooK'
    title = 'Wechat HooK'
    conf_key = slug
    conf_title = title
    project_conf_form = WechatOptions

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('key', project))

    def notify_users(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        key = self.get_option('key', group.project)
        prod_key = self.get_option("prod_key", group.project) or key
        noticeUser = self.get_option("noticeUser", group.project)
        url = WECHAT_WEBHOOK_URL.format(key=key)
        environment = event.get_tag("environment") or ""
        slug = event.project.slug
        print("environment:%s, slug:%s" % (environment, slug))

        if slug.endswith("prod") or environment.startswith("prod"):
            url = WECHAT_WEBHOOK_URL.format(key=prod_key)

        title = u"有新的通知来自 {} 项目".format(slug +
                                        (("(%s)" % environment) if (not slug.endswith("prod") and
                                                         not slug.endswith("int")
                                                         and environment) else ""))
        level = event.get_tag("level") or ""
        description = event.title or event.message

        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": u"#### {title} \n 环境: <font color=\"info\">{environment}</font> \n > 等级: <font color=\"warning\">{level}</font> \n > {message} \n [查看]({url})".format(
                    title=title,
                    environment=environment,
                    level=level,
                    message=description,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                ) + ("\n<@{noticeUser}>".format(noticeUser=noticeUser.replace(",", ",@")) if noticeUser else "")
            }
        }
        print("title:%s, data:%s" % (title, json.dumps(data).encode("utf-8")))
        print("result:%s", json.dumps(requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        ).json()))