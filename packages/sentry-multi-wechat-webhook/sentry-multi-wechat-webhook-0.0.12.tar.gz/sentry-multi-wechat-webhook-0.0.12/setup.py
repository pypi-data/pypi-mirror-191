#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sentry-multi-wechat-webhook",
    version='0.0.12',
    author='badx',
    author_email='badx16@gmail.com',
    url='https://github.com/badx/sentry-multi-webhook',
    description=u'Sentry 企业微信 Webhook 插件',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='sentry multi wechat webhook',
    include_package_data=True,
    zip_safe=False,
    packages=['multi_wechat_webhook'],
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sentry_multi_webhook = multi_wechat_webhook.plugin:MultiWechatWebhookPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ]
)
