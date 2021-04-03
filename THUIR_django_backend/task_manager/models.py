#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'franky'

from django.db import models
from user_system.models import User

try:
    import simplejson as json
except ImportError:
    import json


class TaskAnnotation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timelocation = models.CharField(max_length=1000)
    background = models.CharField(max_length=1000000)
    intent = models.CharField(max_length=1000000)
    satisfaction = models.IntegerField()
    ending_type = models.IntegerField()
    other_reason = models.CharField(max_length=1000)
    information_difficulty = models.IntegerField()
    query_difficulty = models.IntegerField()
    experience = models.IntegerField()
    annotation_status = models.BooleanField(default=False)


class Query(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task_annotation = models.ForeignKey(TaskAnnotation,on_delete=models.CASCADE)
    partition_status = models.BooleanField(default=False)
    annotation_status = models.BooleanField(default=False)
    query_string = models.CharField(max_length=1000)
    start_timestamp = models.IntegerField()
    life_start = models.IntegerField()


class PageLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    belong_query = models.ForeignKey(Query,on_delete=models.CASCADE)
    page_type = models.CharField(max_length=50)
    origin = models.CharField(max_length=50)
    url = models.CharField(max_length=1000)
    referrer = models.CharField(max_length=1000)
    serp_link = models.CharField(max_length=1000)
    html = models.CharField(max_length=1000000)
    start_timestamp = models.BigIntegerField()
    end_timestamp = models.BigIntegerField()
    dwell_time = models.IntegerField()
    page_timestamps = models.CharField(max_length=1000000)
    query_string = models.CharField(max_length=1000)
    page_id = models.IntegerField()
    mouse_moves = models.CharField(max_length=1000000)
    clicked_results = models.CharField(max_length=1000000)


class QueryAnnotation(models.Model):
    belong_query = models.ForeignKey(Query,on_delete=models.CASCADE)
    goal = models.CharField(max_length=1000000)
    relation = models.IntegerField()
    satisfaction = models.IntegerField()
    ending_type = models.IntegerField()
    other_reason = models.CharField(max_length=1000)


class SERPAnnotation(models.Model):
    serp_log = models.ForeignKey(PageLog,on_delete=models.CASCADE)
    usefulness_0 = models.CharField(max_length=1000)
    usefulness_1 = models.CharField(max_length=1000)
    usefulness_2 = models.CharField(max_length=1000)
    usefulness_3 = models.CharField(max_length=1000)
    usefulness_4 = models.CharField(max_length=1000)
