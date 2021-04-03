#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'defaultstr'

import math
from collections import defaultdict
from .models import *
from user_system.models import *

try:
    import simplejson as json
except ImportError:
    import json
from django.core.mail import EmailMultiAlternatives
import smtplib
import time


def store_data(message):
    try:
        page_log = PageLog()
        user = User.objects.get(username=message['username'])
        page_log.user = user
        page_log.page_type = message['type']
        page_log.origin = message['origin']
        page_log.url = message['url']
        page_log.referrer = message['referrer']
        page_log.serp_link = message['serp_link']
        page_log.html = message['html']
        page_log.start_timestamp = int(message['start_timestamp'])
        page_log.end_timestamp = int(message['end_timestamp'])
        page_log.dwell_time = int(message['dwell_time'])
        page_log.page_timestamps = message['page_timestamps']
        page_log.query_string = message['query']
        page_log.mouse_moves = message['mouse_moves']
        page_log.clicked_results = message['clicked_results']
        if message['page_id']:
            page_id = int(message['page_id'])
        else:
            page_id = 1
        page_log.page_id = page_id

        if message['type'] == 'SERP':
            if page_id == 1:
                # 新query
                new_query = Query()
                new_query.user = user
                lis = TaskAnnotation.objects.filter(annotation_status=True)
                if len(lis) == 0 :
                    task_annotation = TaskAnnotation()
                    task_annotation.user = user
                    task_annotation.timelocation = ""
                    task_annotation.background = ""
                    task_annotation.intent = ""
                    task_annotation.satisfaction = -1
                    task_annotation.ending_type = -1
                    task_annotation.other_reason = ""
                    task_annotation.information_difficulty = -1
                    task_annotation.query_difficulty = -1
                    task_annotation.experience = -1
                    task_annotation.annotation_status = False
                    task_annotation.save()
                    new_query.task_annotation = task_annotation
                else :
                    new_query.task_annotation = lis[0]
                new_query.partition_status = False
                new_query.annotation_status = False
                new_query.query_string = message['query']
                new_query.start_timestamp = int(message['start_timestamp'])
                new_query.life_start = int(time.time())
                new_query.save()
                page_log.belong_query = new_query
            else:
                # 在未分组的SERP log里面寻找时间戳离它最近的相同query
                lis = sorted(PageLog.objects.filter(user=user, page_type='SERP', query_string=message['query']), key=lambda item: item.start_timestamp, reverse=True)
                if len(lis) == 0 :
                    nearest_log = page_log
                    belong_query = Query()
                    belong_query.user = user
                    belong_query.partition_status = False
                    belong_query.annotation_status = False
                    belong_query.query_string = ""
                    belong_query.start_timestamp = -1
                    belong_query.life_start = -1
                    
                    task_annotation = TaskAnnotation()
                    task_annotation.user = user
                    task_annotation.timelocation = ""
                    task_annotation.background = ""
                    task_annotation.intent = ""
                    task_annotation.satisfaction = -1
                    task_annotation.ending_type = -1
                    task_annotation.other_reason = ""
                    task_annotation.information_difficulty = -1
                    task_annotation.query_difficulty = -1
                    task_annotation.experience = -1
                    task_annotation.annotation_status = False
                    task_annotation.save()  

                    belong_query.task_annotation = task_annotation
                    belong_query.save()
                
                else :
                    nearest_log = lis[0]
                    belong_query = nearest_log.belong_query
                    belong_query.life_start = int(time.time())
                    page_log.belong_query = belong_query
                
        else:
            #print('not SERP')
            lis = Query.objects.filter(annotation_status=True)
            if len(lis) == 0 :
                belong_query = Query()
                belong_query.user = user
                belong_query.partition_status = False
                belong_query.annotation_status = False
                belong_query.query_string = "NOT SERP RESULTS"
                belong_query.start_timestamp = int(message['start_timestamp'])
                belong_query.life_start = int(message['start_timestamp'])
                
                task_annotation = TaskAnnotation()
                task_annotation.user = user
                task_annotation.timelocation = ""
                task_annotation.background = ""
                task_annotation.intent = ""
                task_annotation.satisfaction = -1
                task_annotation.ending_type = -1
                task_annotation.other_reason = ""
                task_annotation.information_difficulty = -1
                task_annotation.query_difficulty = -1
                task_annotation.experience = -1
                task_annotation.annotation_status = False
                task_annotation.save()

                belong_query.task_annotation = task_annotation
                belong_query.save()
                page_log.belong_query = belong_query
            else :
                page_log.belong_query = lis[0]
        page_log.save()
    except Exception as e:
        #print 'store_data'
        print('exception', e)


def store_page_annotation(message, page_id):
    try:
        usefulness_list = message.split('\t')
        page_log = PageLog.objects.get(id=page_id)
        serp_annotations = SERPAnnotation.objects.filter(serp_log=page_log)
        if serp_annotations:
            serp_annotation = serp_annotations[0]
            serp_annotation.usefulness_0 = usefulness_list[0]
            serp_annotation.usefulness_1 = usefulness_list[1]
            serp_annotation.usefulness_2 = usefulness_list[2]
            serp_annotation.usefulness_3 = usefulness_list[3]
            serp_annotation.usefulness_4 = usefulness_list[4]
        else:
            serp_annotation = SERPAnnotation()
            serp_annotation.serp_log = page_log
            serp_annotation.usefulness_0 = usefulness_list[0]
            serp_annotation.usefulness_1 = usefulness_list[1]
            serp_annotation.usefulness_2 = usefulness_list[2]
            serp_annotation.usefulness_3 = usefulness_list[3]
            serp_annotation.usefulness_4 = usefulness_list[4]
        serp_annotation.save()
    except Exception as e:
        #print 'store_page'
        print('exception', e)


def partition(user, query_ids):
    task = TaskAnnotation()
    task.user = user
    task.timelocation = ""
    task.background = ""
    task.intent = ""
    task.satisfaction = -1
    task.ending_type = -1
    task.information_difficulty = -1
    task.query_difficulty = -1
    task.experience = -1
    task.annotation_status = False
    task.save()
    for query_id in query_ids:
        query_id = int(query_id)
        query = Query.objects.get(id=query_id)
        query.partition_status = True
        query.task_annotation = task
        query.save()
        query__annotation = QueryAnnotation()
        query__annotation.belong_query = query
        query__annotation.goal = ""
        query__annotation.relation = -1
        query__annotation.satisfaction = -1
        query__annotation.ending_type = -1
        query__annotation.other_reason = ""
        query__annotation.save()


def delete(user, query_ids):
    for query_id in query_ids:
        query_id = int(query_id)
        query = Query.objects.get(user=user, id=query_id)
        pagelogs = PageLog.objects.filter(user=user, belong_query=query)
        for pagelog in pagelogs:
            pagelog.delete()
        query.delete()


def unpartition(user, task_ids):
    for task_id in task_ids:
        task = TaskAnnotation.objects.get(user=user, id=task_id)
        queries = Query.objects.filter(user=user, partition_status=True, task_annotation=task)
        for query in queries:
            query.partition_status = False
            query.task_annotation = TaskAnnotation.objects.filter(annotation_status=True)[0]
            query.save()
            query_annotation = QueryAnnotation.objects.get(belong_query=query)
            query_annotation.delete()
            pagelogs = PageLog.objects.filter(user=user, belong_query=query)
            for pagelog in pagelogs:
                for serp_annotation in SERPAnnotation.objects.filter(serp_log=pagelog):
                        serp_annotation.delete()
        task.delete()


def clear_expired_query(user):
    unpartition_queries = Query.objects.filter(user=user, partition_status=False)
    for query in unpartition_queries:
        if int(time.time()) - query.life_start > 172800:
            pagelogs = PageLog.objects.filter(user=user, belong_query=query)
            for pagelog in pagelogs:
                pagelog.delete()
            query.delete()

    unannotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=False)
    for task in unannotated_tasks:
        queries = Query.objects.filter(user=user, partition_status=True, task_annotation=task)
        expired = False
        for query in queries:
            if int(time.time()) - query.life_start > 172800:
                expired = True
                break
        if expired:
            for query in queries:
                for pagelog in PageLog.objects.filter(user=user, belong_query=query):
                    for serp_annotation in SERPAnnotation.objects.filter(serp_log=pagelog):
                        serp_annotation.delete()
                    pagelog.delete()
                query_annotation = QueryAnnotation.objects.get(belong_query=query)
                query_annotation.delete()
                query.delete()
            task.delete()


def get_items_list(user, queries):
    items_list = []
    for i in range(len(queries)):
        query = queries[i]
        query__annotation = QueryAnnotation.objects.filter(belong_query=query)[0]
        pages = sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)
        pages_and_status = []
        for page in pages:
            if SERPAnnotation.objects.filter(serp_log=page):
                pages_and_status.append((page, True))
            else:
                pages_and_status.append((page, False))
        if i == 0:
            prequery = None
        else:
            prequery = queries[i-1]
        items_list.append((query, prequery, query__annotation, pages_and_status))
    return items_list


def check_serp_annotations(user, queries):
    flag = True
    for query in queries:
        pages = sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)
        for page in pages:
            if not SERPAnnotation.objects.filter(serp_log=page):
                flag = False
                break
    return flag


def send_task_finished_email(request, task, user, admin_emails=[]):
    subject = u'task accomplished'

    message = u'user%s ' % user.username

    message += u'has finished the annotation of %s: %s' % (task.task_name, task.task_description)
    message += u'task detail, please click：'
    host = u'http://' + request.get_host()
    url = unicode(host + '/task/info/%s/' % task.id)
    html_content = message + u'<a href="%s">%s</a>.' % (url, url)
    message += url

    source = 'thuir_annotation@163.com'
    for target in admin_emails:
        msg = EmailMultiAlternatives(subject, message, source, [target])
        msg.attach_alternative(html_content, 'text/html')
        try:
            msg.send()
        except smtplib.SMTPException as e:
            print(type(e))
            print(e)
