#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'defaultstr'

from django.db import models
from .forms import *
from hashlib import sha512
from uuid import uuid4
import time
from django.utils.deconstruct import deconstructible


user_group_list = (
    ('admin', u'administrator'),
    ('normal_user', u'normal user'),
)

@deconstructible
class TimestampGenerator(object):

    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds
    
    def __eq__(self,other):
        return self.seconds==other.seconds

@deconstructible
class KeyGenerator(object):

    def __init__(self, length):
        self.length = length

    def __call__(self):
        key = sha512(uuid4().hex).hexdigest()[0:self.length]
        return key
    
    def __eq__(self,other):
        return self.length==other.length


class User(models.Model):
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
    age = models.IntegerField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    field = models.CharField(max_length=50)
    search_frequency = models.CharField(max_length=50, choices=search_frequency_choices)
    search_history = models.CharField(max_length=50, choices=search_history_choices)
    signup_time = models.DateTimeField()
    last_login = models.DateTimeField()
    login_num = models.IntegerField()


class ResetPasswordRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=50, default=KeyGenerator(12))
    expire = models.IntegerField(default=TimestampGenerator(60*60*30))


