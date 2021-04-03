#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'defaultstr'
import sys
import csv
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext

from user_system.utils import *
from user_system.models import *
from .models import *

from .utils import *
from django.views.decorators.csrf import csrf_exempt
import urllib
import time

try:
    import simplejson as json
except ImportError:
    import json


@csrf_exempt
def data(request):
    if request.method == 'POST':
        message = json.loads(request.POST['message'])
        store_data(message)
        return HttpResponse('nice')
    else:
        return HttpResponse('oh no')


@csrf_exempt
@require_login
def page_annotation_submit(user, request, page_id):
    if request.method == 'POST':
        message = request.POST['message']
        store_page_annotation(message, page_id)
        return HttpResponse('nice')
    else:
        return HttpResponse('oh no')

@require_login
def export(user, request):
    clear_expired_query(user)
    # 根据条件查询相关数据
    page_lis = sorted(PageLog.objects.filter(user=user), key=lambda item: item.start_timestamp)
    response = HttpResponse(content_type='text/csv', charset='UTF-8')
    # 自定义文件名
    time_now = time.strftime('%Y%m%d')
    filename = str(user) + '_' + time_now
    # 添加header，attachment表示以附件方式下载
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
	# 生成一个对象
    writer = csv.writer(response)
    # 定义表头
    writer.writerow(['id', 'page_type', 'origin','url','referrer','serp_link','html','start_timestamp','end_timestamp','dwell_time','page_timestamps','query_string','page_id','mouse_moves','clicked_results','belong_query_id','user_id'])
    
    # 添加数据
    #writer.writerows(page_lis)
    for page in page_lis:
        writer.writerow([page.id,page.page_type,page.origin,page.url,page.referrer,page.serp_link,page.html,page.start_timestamp,page.end_timestamp,page.dwell_time,page.page_timestamps,page.query_string,page.page_id,page.mouse_moves,page.clicked_results,page.belong_query_id,page.user_id])

    return response


@require_login
def task_home(user, request):
    clear_expired_query(user)
    annotation_num = len(Query.objects.filter(user=user, annotation_status=True))
    partition_num = len(Query.objects.filter(user=user, partition_status=True, annotation_status=False))
    remain_num = len(Query.objects.filter(user=user, partition_status=False))
    return render(
        request,
        'task_home.html',
        {
            'cur_user': user,
            'annotation_num': annotation_num,
            'partition_num': partition_num,
            'remain_num': remain_num
        })


@require_login
def task_partition(user, request):
    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        if action_type == "partition":
            query_ids = request.POST.getlist('unpartition_checkbox')
            # print("partition", query_ids)
            if query_ids:
                partition(user, query_ids)

        if action_type == "delete":
            query_ids = request.POST.getlist('unpartition_checkbox')
            # print("delete", query_ids)
            if query_ids:
                delete(user, query_ids)

        if action_type == "unpartition":
            task_ids = request.POST.getlist('partition_checkbox')
            # print("unpartition", task_ids)
            if task_ids:
                unpartition(user, task_ids)
        return HttpResponseRedirect('/task/partition/')

    clear_expired_query(user)
    unpartition_queries = sorted(Query.objects.filter(user=user, partition_status=False), key=lambda item: item.start_timestamp)
    unpartition_queries_to_pages = []
    for query in unpartition_queries:
        unpartition_queries_to_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)))

    unannotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=False)
    unannotated_tasks_to_queries = []
    for task in unannotated_tasks:
        unannotated_tasks_to_queries.append((task.id, sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task), key=lambda item: item.start_timestamp)))
    return render(
        request,
        'task_partition.html',
        {
            'cur_user': user,
            'unpartition_queries_to_pages': unpartition_queries_to_pages,
            'partition_tasks_to_queries': unannotated_tasks_to_queries
        })


@require_login
def annotation_home(user, request):
    clear_expired_query(user)
    annotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=True)
    unannotated_tasks = TaskAnnotation.objects.filter(user=user, annotation_status=False)
    annotated_tasks_to_queries = []
    unannotated_tasks_to_queries = []
    for task in unannotated_tasks:
        unannotated_tasks_to_queries.append((task.id, sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task), key=lambda item: item.start_timestamp)))
    for task in annotated_tasks:
        annotated_tasks_to_queries.append((task.id, sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task), key=lambda item: item.start_timestamp)))

    return render(
        request,
        'annotation_home.html',
        {
            'cur_user': user,
            'unannotated_tasks_to_queries': unannotated_tasks_to_queries,
            'annotated_tasks_to_queries': annotated_tasks_to_queries
        })


@require_login
def task_annotation1(user, request, task_id):
    if request.method == 'POST':
        timelocation = request.POST.get('timelocation_text')
        background = request.POST.get('background_text')
        intent = request.POST.get('intent_text')
        task_annotation = TaskAnnotation.objects.get(id=task_id, user=user, annotation_status=False)
        task_annotation.timelocation = timelocation
        task_annotation.background = background
        task_annotation.intent = intent
        task_annotation.save()
        return HttpResponseRedirect('/task/query_annotation/'+str(task_id))

    task_annotation = TaskAnnotation.objects.filter(id=task_id, user=user, annotation_status=False)
    if len(task_annotation) == 0:
        return HttpResponseRedirect('/task/home/')
    task_annotation = task_annotation[0]
    queries = sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task_annotation), key=lambda item: item.start_timestamp)
    queries_to_pages = []
    for query in queries:
        queries_to_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)))

    return render(
        request,
        'task_annotation1.html',
        {
            'cur_user': user,
            'task': task_annotation,
            'queries_to_pages': queries_to_pages
        })


@require_login
def query_annotation(user, request, task_id):
    task_annotation = TaskAnnotation.objects.filter(id=task_id, user=user, annotation_status=False)
    if len(task_annotation) == 0:
        return HttpResponseRedirect('/task/home/')
    task_annotation = task_annotation[0]
    queries = sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task_annotation), key=lambda item: item.start_timestamp)
    items_list = get_items_list(user, queries)

    if request.method == 'POST':
        for query in queries:
            goal = request.POST.get('goal_text_'+str(query.id))
            relation = request.POST.get('relation_ratio_'+str(query.id))
            satisfaction = request.POST.get('satisfaction_ratio_'+str(query.id))
            ending_type = request.POST.get('ending_ratio_'+str(query.id))
            other_reason = request.POST.get('ending_text_'+str(query.id))
            query__annotation = QueryAnnotation.objects.get(belong_query=query)
            query__annotation.goal = goal
            query__annotation.relation = relation
            query__annotation.satisfaction = satisfaction
            query__annotation.ending_type = ending_type
            query__annotation.other_reason = other_reason
            query__annotation.save()
        return HttpResponseRedirect('/task/task_annotation2/'+str(task_id))

    return render(
        request,
        'query_annotation.html',
        {
            'cur_user': user,
            'items_list': items_list
        })


@require_login
def task_annotation2(user, request, task_id):
    # 先判断一下该task下每个query的所有SERP的标注是否都有,如果有的没有,则提示未标注完,然后退回到query_annotation
    task_annotation = TaskAnnotation.objects.filter(id=task_id, user=user, annotation_status=False)
    if len(task_annotation) == 0:
        return HttpResponseRedirect('/task/home/')
    task_annotation = task_annotation[0]
    queries = sorted(Query.objects.filter(user=user, partition_status=True, task_annotation=task_annotation), key=lambda item: item.start_timestamp)
    flag = check_serp_annotations(user, queries)

    queries_to_pages = []
    for query in queries:
        queries_to_pages.append((query, sorted(PageLog.objects.filter(user=user, belong_query=query, page_type='SERP'), key=lambda item: item.start_timestamp)))

    if request.method == 'POST':
        satisfaction = request.POST.get('satisfaction_ratio')
        ending_type = request.POST.get('ending_ratio')
        information_difficulty = request.POST.get('information_ratio')
        query_difficulty = request.POST.get('query_ratio')
        experience = request.POST.get('experience_ratio')
        task_annotation.satisfaction = int(satisfaction)
        task_annotation.ending_type = int(ending_type)
        task_annotation.information_difficulty = int(information_difficulty)
        task_annotation.query_difficulty = int(query_difficulty)
        task_annotation.experience = int(experience)
        task_annotation.other_reason = request.POST.get('ending_text_'+str(task_id))
        task_annotation.annotation_status = True
        task_annotation.save()
        for query in queries:
            query.annotation_status = True
            query.save()
        return HttpResponseRedirect('/task/annotation/')

    return render(
        request,
        'task_annotation2.html',
        {
            'cur_user': user,
            'task': task_annotation,
            'queries_to_pages': queries_to_pages,
            'flag': flag
        })


@require_login
def show_page(user, request, page_id):
    serp = PageLog.objects.filter(id=page_id, user=user)
    if len(serp) == 0:
        return HttpResponseRedirect('/task/home/')
    serp = serp[0]
    return render(
        request,
        'show_query.html',
        {
            'html': serp.html,
        }
    )


@require_login
def page_annotation(user, request, page_id):
    page = PageLog.objects.filter(id=page_id, user=user)
    if len(page) == 0:
        return HttpResponseRedirect('/task/home/')
    page = page[0]
    clicked_results = json.loads(page.clicked_results)
    clicked_ids = []
    for result in clicked_results:
        if result['id'] not in clicked_ids:
            clicked_ids.append(result['id'])
    if page.origin == 'baidu':
        return render(
            request,
            'page_annotation_baidu.html',
            {
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
        )
    if page.origin == 'sogou':
        return render(
            request,
            'page_annotation_sogou.html',
            {
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
        )
    if page.origin == '360':
        return render(
            request,
            'page_annotation_360.html',
            {
                'html': page.html,
                'page_id': page_id,
                'clicked_ids': clicked_ids
            }
        )


@csrf_exempt
def show_me_serp(request, query_id):
    query = Query.objects.get(id=query_id)
    serp = PageLog.objects.filter(belong_query=query, page_id='1')
    serp = serp[0]
    print(serp.id)
    return render(
        request,
        'show_query.html',
        {
            'html': serp.html,
        }
    )
