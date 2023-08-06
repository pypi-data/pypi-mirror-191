# coding: utf-8
import json
import requests

from django import forms
from sentry.plugins.bases import notify


WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"


class WechatWebhookOptionsForm(forms.Form):
    key = forms.CharField(
        max_length=255,
        help_text='默认企业微信webHookKey',
        required=True
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


class MultiWechatWebhookPlugin(notify.NotificationPlugin):
    author = 'badx'
    author_url = 'https://github.com/badx/sentry-multi-webhook'
    version = '0.0.23'
    description = u'Sentry 企业微信 Webhook 插件'
    resource_links = [
        ('Source', 'https://github.com/badx/sentry-multi-webhook'),
        ('Bug Tracker', 'https://github.com/badx/sentry-multi-webhook/issues'),
        ('README', 'https://github.com/badx/sentry-multi-webhook/blob/master/README.md'),
    ]

    slug = 'multi_wechat_webhook'
    title = 'Multi Wechat Webhook'
    conf_key = slug
    conf_title = title
    project_conf_form = WechatWebhookOptionsForm

    def is_configured(self, project):
        isConfigured = bool(self.get_option('key', project))
        print("check notify_users:" + str(isConfigured))
        return isConfigured

    def notify_users(self, group, event, *args, **kwargs):
        print("notify_users")
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

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
