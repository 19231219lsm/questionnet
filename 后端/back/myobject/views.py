# Create your views here.
import csv
import operator
import os
from contextvars import Context
from html import escape

import httplib2
import qrcode
import hashlib
import json
import random
import io
from urllib.parse import urlencode
from datetime import datetime
import reportlab
import xlwt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
import pickle
import re
from back import settings
from myobject.models import *
from io import StringIO

from django.template.loader import get_template

from django.template import Context

from django.http import HttpResponse

#internet = "http://localhost:8080/tosurvey?id="


internet = "http://39.104.170.158:80/tosurvey?id="


def getIP(request):
    if 'HTTP_X_FORWARD_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARD']
    else:
        ip = request.META['REMOTE_ADDR']
    res = {'ip': ip}
    return JsonResponse(res)


def getLocation(request):
    # from urllib import urlencode #python2 .decode("utf-8")
    if 'HTTP_X_FORWARD_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARD']
    else:
        ip = request.META['REMOTE_ADDR']
    params = urlencode({'ip': ip, 'datatype': 'jsonp', 'callback': 'find'})
    url = 'http://api.ip138.com/query/?' + params
    headers = {"token": "39e087470c2856e0b4801a6deec6ad22"}  # token为示例
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers=headers)
    content = content.decode('utf-8')
    content = re.sub("[A-Za-z0-9\!\%\[\]\,\。\(\{\"\:\.\}\)]", "", content)
    return JsonResponse({'location': content})


def end3(request):
    if request.method == 'GET':
        res_dtct = {}
        if 'HTTP_X_FORWARD_FOR' in request.META.keys():
            ip = request.META['HTTP_X_FORWARD']
        else:
            ip = request.META['REMOTE_ADDR']
        node = request.GET.get('id')
        se = Node.objects.get(node=node)
        id = se.surveyId
        statistic = []
        survey = Survey.objects.get(id=id)
        res_dtct['name'] = survey.name
        res_dtct['class'] = survey.type
        res_dtct['titleContent'] = survey.description
        num = 0
        question = QuestionSelectData.objects.filter(survey_id=id).filter(ip=ip)
        num += question.count()
        for i in question:
            q = QuestionSelect.objects.get(survey_id=id, sequenceNumber=i.sequenceNumber)
            r = {}
            r['type'] = q.type
            r['quesnumber'] = q.sequenceNumber
            r['isRequired'] = q.required
            r['title'] = q.name
            r['quesContent'] = q.description
            r['correctAnswer'] = q.result
            r['yourAnswer'] = i.answer
            option = Option.objects.filter(questionId=q.id)
            choice = []
            for j in option:
                choice.append(j.content)
            r['choicesContent'] = choice
            r['point'] = q.score
            statistic.append(r)
        question = QuestionMulSelectData.objects.filter(survey_id=id).filter(ip=ip)
        num += question.count()
        for i in question:
            q = QuestionMulSelect.objects.get(survey_id=id, sequenceNumber=i.sequenceNumber)
            r = {}
            r['type'] = q.type
            r['quesnumber'] = q.sequenceNumber
            r['isRequired'] = q.required
            r['title'] = q.name
            r['quesContent'] = q.description
            s = []
            for j in q.result:
                s.append(j)
            r['correctAnswer'] = s
            s = []
            for j in i.answer:
                s.append(j)
            r['yourAnswer'] = s
            option = MulOption.objects.filter(questionId=q.id)
            choice = []
            for i in option:
                choice.append(i.content)
            r['choicesContent'] = choice
            r['point'] = q.score
            statistic.append(r)
        question = QuestionFillBlankData.objects.filter(survey_id=id).filter(ip=ip)
        num += question.count()
        for i in question:
            q = QuestionFillBlank.objects.get(survey_id=id, sequenceNumber=i.sequenceNumber)
            r = {}
            r['type'] = q.type
            r['quesnumber'] = q.sequenceNumber
            r['isRequired'] = q.required
            r['title'] = q.name
            r['quesContent'] = q.description
            r['correctAnswer'] = q.result
            r['yourAnswer'] = i.answer
            r['point'] = q.score
            statistic.append(r)
        question = QuestionRemarkData.objects.filter(survey_id=id).filter(ip=ip)
        num += question.count()
        for i in question:
            q = QuestionRemark.objects.get(survey_id=id, sequenceNumber=i.sequenceNumber)
            r = {}
            r['type'] = q.type
            r['quesnumber'] = q.sequenceNumber
            r['isRequired'] = q.required
            r['title'] = q.name
            r['quesContent'] = q.description
            r['correctAnswer'] = q.result
            r['yourAnswer'] = i.answer
            r['point'] = q.score
            statistic.append(r)
        question = QuestionJudgementData.objects.filter(survey_id=id).filter(ip=ip)
        num += question.count()
        for i in question:
            q = QuestionJudgement.objects.get(survey_id=id, sequenceNumber=i.sequenceNumber)
            r = {}
            r['type'] = q.type
            r['quesnumber'] = q.sequenceNumber
            r['isRequired'] = q.required
            r['title'] = q.name
            r['quesContent'] = q.description
            r['correctAnswer'] = q.result
            r['yourAnswer'] = i.answer
            r['point'] = q.score
            statistic.append(r)
        res_dtct['totalNum'] = num
        res_dtct['statistic'] = sorted(statistic, key=operator.itemgetter("quesnumber"))
        return JsonResponse(res_dtct)


def survey(request):
    if request.method == 'GET':
        try:
            res_dtct = {}
            if 'HTTP_X_FORWARD_FOR' in request.META.keys():
                ip = request.META['HTTP_X_FORWARD']
            else:
                ip = request.META['REMOTE_ADDR']
            node = request.GET.get('id')

            se = Node.objects.get(node=node)
            id = se.surveyId
            if Record.objects.filter(survey_id=id).filter(ip=ip).exists():
                res_dtct['status'] = 0
                return JsonResponse(res_dtct)

            res_dtct['id'] = node
            survey = Survey.objects.get(id=id)
            editStatus = request.GET.get('editStatus')
            print(editStatus)
            if survey.status != 1 and int(editStatus) != 1:
                res_dtct['res'] = 3
                return JsonResponse(res_dtct)
            res_dtct['class'] = survey.type
            res_dtct['titleContent'] = survey.name
            res_dtct['info'] = survey.description
            res_dtct['needOrder'] = survey.isNeed
            res_dtct['status'] = survey.status
            res_dtct['stopTime'] = str(survey.stop_at.strftime('%Y-%m-%d %H:%M:%S'))
            if survey.type == 6:
                res_dtct['surveyNum'] = survey.quota
            a = []
            # 读取问题
            questionselect = QuestionSelect.objects.filter(survey_id=survey.id)
            for i in questionselect:
                r = {}
                r['type'] = 1
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""
                r['correctAnswer'] = i.result
                r['point'] = i.score
                r['number'] = i.sequenceNumber
                choices = []
                options = Option.objects.filter(questionId=i.id)
                for j in options:
                    choices.append(j.content)
                r['choices'] = choices
                a.append(r)
            questionmulselect = QuestionMulSelect.objects.filter(survey_id=survey.id)
            for i in questionmulselect:
                r = {}
                r['type'] = 2
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""
                r['correctAnswer'] = i.result
                r['point'] = i.score
                r['number'] = i.sequenceNumber
                choices = []
                options = MulOption.objects.filter(questionId=i.id)
                for j in options:
                    choices.append(j.content)
                r['choices'] = choices
                a.append(r)
            questionremark = QuestionRemark.objects.filter(survey_id=survey.id)
            for i in questionremark:
                r = {}
                r['type'] = 4
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""
                r['correctAnswer'] = i.result
                r['point'] = i.score
                r['number'] = i.sequenceNumber
                r['choices'] = i.starNum
                a.append(r)
            questionfillblank = QuestionFillBlank.objects.filter(survey_id=survey.id)
            for i in questionfillblank:
                r = {}
                r['type'] = 3
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""
                r['correctAnswer'] = i.result
                r['point'] = i.score
                r['number'] = i.sequenceNumber
                a.append(r)
            questionjudgement = QuestionJudgement.objects.filter(survey_id=survey.id)
            for i in questionjudgement:
                r = {}
                r['type'] = 5
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""
                r['correctAnswer'] = i.result
                r['point'] = i.score
                r['number'] = i.sequenceNumber
                a.append(r)
            questionquota = QuestionQuota.objects.filter(survey_id=survey.id)
            for i in questionquota:
                r = {}
                r['type'] = 6
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""

                r['number'] = i.sequenceNumber
                choices = []
                options = QuestionQuotaOption.objects.filter(questionId=i.id)
                for j in options:
                    x = {'content': j.content, 'limit': j.quota - j.numbers}
                    choices.append(x)
                r['choices'] = choices
                a.append(r)
            questionpunch = QuestionPunch.objects.filter(survey_id=survey.id)
            for i in questionpunch:
                r = {}
                r['type'] = 7
                r['id'] = i.id
                r['title'] = i.name
                r['description'] = i.description
                r['must'] = i.required
                r['answer'] = ""

                r['number'] = i.sequenceNumber
                a.append(r)
            list1 = sorted(a, key=operator.itemgetter("number"))
            res_dtct['survey'] = list1

            res_dtct['res'] = 1
            return JsonResponse(res_dtct)
        except Exception as error:
            res_dtct['res'] = 0
            print(error)
            return JsonResponse(res_dtct)
    if request.method == 'POST':
        # try:
        res_dict = {}
        da = json.loads(request.body)
        node = da.get('id')
        se = Node.objects.get(node=node)

        id = se.surveyId
        if 'HTTP_X_FORWARD_FOR' in request.META.keys():
            ip = request.META['HTTP_X_FORWARD']
        else:
            ip = request.META['REMOTE_ADDR']
        data = da.get('data')

        survey = Survey.objects.get(id=id)
        survey.recoveryNum = survey.recoveryNum + 1
        survey.save()
        if survey.quota != 0 and survey.recoveryNum >= survey.quota:
            survey.status = 0
            survey.save()

        record = Record()
        record.survey_id = id
        record.ip = ip
        record.save()
        survey = data['survey']
        for i in survey:
            if i['type'] == 1:
                r = QuestionSelectData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                q = QuestionSelect.objects.get(id=i['id'])
                n = i['answer']
                if n:
                    m = Option.objects.filter(questionId=q.id)[n - 1]
                    m.numbers += 1
                    m.save()
                    r.answer = n
                r.save()

            elif i['type'] == 2:
                r = QuestionMulSelectData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                string = ""
                if i['answer']:
                    q = QuestionMulSelect.objects.get(id=i['id'])

                    for j in i['answer']:
                        string += str(j)
                        m = MulOption.objects.filter(questionId=q.id)[j - 1]
                        m.numbers += 1
                        m.save()

                r.answer = string
                r.save()
            elif i['type'] == 3:
                r = QuestionFillBlankData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                r.answer = i['answer']

                r.save()
            elif i['type'] == 4:

                x = i['answer']
                r = QuestionRemarkData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                r.answer = x
                r.save()


            elif i['type'] == 5:
                r = QuestionJudgementData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                r.answer = i['answer'] - 1
                q = QuestionJudgement.objects.get(id=i['id'])
                x = i['answer']
                if i['answer'] is None:
                    continue
                if x == 1:
                    q.correctAnswers += 1
                else:
                    q.wrongAnswers += 1
                q.save()
                r.save()
            elif i['type'] == 6:
                r = QuestionQuotaData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                q = QuestionQuota.objects.get(id=i['id'])
                n = i['answer']
                if n:
                    m = QuestionQuotaOption.objects.filter(questionId=q.id)[n - 1]
                    m.numbers += 1
                    m.save()
                    r.answer = n
                r.save()
            elif i['type'] == 7:
                r = QuestionPunchData()
                r.sequenceNumber = i['number']
                r.survey_id = id
                r.ip = ip
                r.answer = i['answer']
                r.save()

        res_dict['res'] = 1
        return JsonResponse(res_dict)
    # except Exception as error:
    #     print(error)
    #     res_dict['res'] = 0
    #     return JsonResponse(res_dict)


def search(request):
    """浏览信息"""
    try:
        smod = Survey.objects
        slist = smod.filter(status__lt=9).filter(user_id=request.session['user']['id'])
        # slist = smod.filter(status__lt=9).filter(user_id=1)
        # 获取并判断搜索条件
        data = json.loads(request.body)

        kw = data.get("keyword")
        if kw:
            slist = slist.filter(name__contains=kw)
        else:
            slist = smod.filter(status__lt=9).filter(user_id=request.session['user']['id'])
        # 获取、判断并封装状态status搜索条件
        # slist = slist.order_by("id")  # 对id排序
        # 执行分页处理
        # pIndex = int(pIndex)
        # page = Paginator(slist, 10)  # 以每页10条数据分页
        # maxpages = page.num_pages  # 获取最大页数
        # 判断当前页是否越界
        # if pIndex > maxpages:
        #     pIndex = maxpages
        # if pIndex < 1:
        #     pIndex = 1
        # list2 = page.page(pIndex)  # 获取当前页数据
        # plist = page.page_range  # 获取页码列表信息
        res = []
        for i in slist:
            print(i.id)
            res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                        "recoverNum": i.recoveryNum,
                        "createtime": i.create_at.strftime('%Y-%m-%d '),
                        'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status}
            res.append(res_dict)
        return JsonResponse({'res': res})
    except Exception as err:
        print(err)
        res_dict = {}
        res_dict['res'] = 2
        return JsonResponse(res_dict)


@csrf_exempt
def publish_or_delete(request):
    data = json.loads(request.body)
    type = data.get("type")
    if type == 1:
        survey_id = data.get("survey_id")
        if survey_id:
            node = Node.objects.get(node=survey_id)
            survey = Survey.objects.get(id=node.surveyId)
            if survey.status == 1:
                survey.status = 0
                survey.update_at = datetime.now()
            else:
                survey.status = 1
                survey.update_at = datetime.now()
            survey.save()

            return JsonResponse({'res': 1})
        else:
            return JsonResponse({'res': 2})
    elif type == 2:
        userid = data.get('userid')
        survey_id = data.get("survey_id")
        node = Node.objects.get(node=survey_id)
        Survey.objects.filter(id=node.surveyId).update(status=9)
        res_dict = {'res': 1}
        smod = Survey.objects
        slist = smod.filter(status__lt=9).filter(user_id=userid)
        res = []
        for i in slist:
            res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                        "recovernum": i.recoveryNum,
                        "createtime": i.create_at.strftime('%Y-%m-%d '),
                        'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status, 'class': i.type}
            res.append(res_dict)
        r = {}
        r['res'] = res
        return JsonResponse(r)
    elif type == 3:
        """浏览信息"""
        # try:
        userid = data.get('userid')
        smod = Survey.objects
        slist = smod.filter(status__lt=9).filter(user_id=userid)

        # 获取并判断搜索条件
        data = json.loads(request.body)

        kw = data.get("keyword")
        if kw:
            slist = slist.filter(name__contains=kw).filter(status__lt=9).filter(
                user_id=userid)
        else:
            slist = smod.filter(status__lt=9).filter(user_id=userid)

        # 获取、判断并封装状态status搜索条件
        # slist = slist.order_by("id")  # 对id排序
        # 执行分页处理
        # pIndex = int(pIndex)
        # page = Paginator(slist, 10)  # 以每页10条数据分页
        # maxpages = page.num_pages  # 获取最大页数
        # 判断当前页是否越界
        # if pIndex > maxpages:
        #     pIndex = maxpages
        # if pIndex < 1:
        #     pIndex = 1
        # list2 = page.page(pIndex)  # 获取当前页数据
        # plist = page.page_range  # 获取页码列表信息
        res = []
        for i in slist:
            res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                        "recovernum": i.recoveryNum,
                        "createtime": i.create_at.strftime('%Y-%m-%d '),
                        'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status, 'class': i.type}
            res.append(res_dict)
        return JsonResponse({'res': res})
        # except Exception as err:
        #     print(err)
        #     res_dict = {}
        #     res_dict['res'] = 2
        #     return JsonResponse(res_dict)
    elif type == 4:
        try:
            '''浏览信息'''
            smod = Survey.objects
            userid = data.get('userid')
            slist = smod.filter(status__lt=9).filter(user_id=userid)
            # slist = smod.filter(status__lt=9).filter(user_id=1)
            # 获取并判断搜索条件
            kw = data.get("judge", 1)  # 1 默认是按照id排序

            if kw == 1:
                slist = slist.order_by("id")  # 对id排序
            elif kw == 2:
                slist = slist.order_by("-id", )
            elif kw == 3:
                slist = slist.order_by("recoveryNum")
            elif kw == 4:
                slist = slist.order_by("-recoveryNum")
            elif kw == 5 or kw == 6:
                if kw == 5:
                    slist = slist.filter(status=1).order_by("update_at")
                else:
                    slist = slist.filter(status=1).order_by("-update_at")
                res = []
                for i in slist:
                    res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'publish': i.status, 'name': i.name,
                                "status": i.status,
                                "recovernum": i.recoveryNum,
                                "createtime": i.create_at.strftime('%Y-%m-%d'),
                                'publish_at': i.update_at.strftime('%Y-%m-%d '), 'class': i.type}
                    res.append(res_dict)
                slist = slist.filter(status=0)
                for i in slist:
                    res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, 'publish': i.status,
                                "status": i.status,
                                "recovernum": i.recoveryNum,
                                "createtime": i.create_at.strftime('%Y-%m-%d'),
                                'publish_at': i.update_at.strftime('%Y-%m-%d '), 'class': i.type}
                    res.append(res_dict)
                return JsonResponse({'res': res})
            # # 执行分页处理
            # pIndex = int(pIndex)
            # page = Paginator(slist, 10)  # 以每页10条数据分页
            # maxpages = page.num_pages  # 获取最大页数
            # # 判断当前页是否越界
            # if pIndex > maxpages:
            #     pIndex = maxpages
            # if pIndex < 1:
            #     pIndex = 1
            # list2 = page.page(pIndex)  # 获取当前页数据
            # plist = page.page_range  # 获取页码列表信息
            # context = {"surveylist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages}
            res = []
            for i in slist:
                res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, 'publish': i.status,
                            "status": i.status,
                            "recovernum": i.recoveryNum,
                            "createtime": i.create_at.strftime('%Y-%m-%d'),
                            'publish_at': i.update_at.strftime('%Y-%m-%d '), 'class': i.type}
                res.append(res_dict)
            return JsonResponse({'res': res, 'kw': kw})
        except Exception as err:
            print(err)
            res_dict = {}
            res_dict['res'] = 2
            return JsonResponse(res_dict)
    elif type == 5:
        res_dict = {}
        survey_id = data.get("survey_id")

        res_dict['link'] = internet + str(survey_id)

        photo = createQRcode(survey_id, res_dict['link'])
        s = 'http://39.104.170.158:80/' + photo
        #s = 'http://localhost:8000/' + photo
        res_dict['photo'] = s
        return JsonResponse(res_dict)
    elif type == 6:
        id = data.get('survey_id')
        node = Node.objects.get(node=id)
        oldSurvey = Survey.objects.get(id=node.surveyId)
        newSurvey = Survey()
        newname = oldSurvey.name + "-副本"
        newSurvey.name = newname
        newSurvey.status = 0
        newSurvey.user_id = oldSurvey.user_id
        newSurvey.isNeed = oldSurvey.isNeed
        newSurvey.stop_at = oldSurvey.stop_at
        newSurvey.description = oldSurvey.description
        newSurvey.save()
        rand = random.randint(100000, 999999)
        node = Node()
        node.surveyId = newSurvey.id
        node.node = rand
        node.save()

        questionSelect = QuestionSelect.objects.filter(survey_id=oldSurvey.id)
        for i in questionSelect:
            question = QuestionSelect()
            question.name = i.name
            question.result = i.result

            question.type = 1
            question.description = i.description
            question.sequenceNumber = i.sequenceNumber
            question.required = i.required
            question.survey_id = newSurvey.id
            question.save()
            option = Option.objects.filter(questionId=i.id)
            for j in option:
                k = Option()
                k.questionId = question.id
                k.content = j.content
                k.save()
        questionSelect = QuestionMulSelect.objects.filter(survey_id=oldSurvey.id)
        for i in questionSelect:
            question = QuestionMulSelect()
            question.name = i.name
            question.type = 2
            question.description = i.description
            question.result = i.result
            question.sequenceNumber = i.sequenceNumber
            question.required = i.required
            question.survey_id = newSurvey.id
            question.save()
            option = MulOption.objects.filter(questionId=i.id)
            for j in option:
                k = MulOption()
                k.questionId = question.id
                k.content = j.content
                k.save()
        questionSelect = QuestionFillBlank.objects.filter(survey_id=oldSurvey.id)
        for i in questionSelect:
            question = QuestionFillBlank()
            question.name = i.name
            question.result = i.result
            question.sequenceNumber = i.sequenceNumber
            question.required = i.required
            # question.context = i.context
            question.type = 3
            question.description = i.description
            question.survey_id = newSurvey.id
            question.save()
        questionremark = QuestionRemark.objects.filter(survey_id=oldSurvey.id)
        for i in questionremark:
            question = QuestionRemark()
            question.name = i.name
            question.type = 4
            question.starNum = i.starNum
            question.required = i.required
            question.sequenceNumber = i.sequenceNumber
            question.description = i.description
            question.survey_id = newSurvey.id
            question.save()
        questionjudgement = QuestionJudgement.objects.filter(survey_id=oldSurvey.id)
        for i in questionjudgement:
            question = QuestionJudgement()
            question.name = i.name
            question.type = 5
            question.required = i.required
            question.sequenceNumber = i.sequenceNumber
            question.description = i.description
            question.survey_id = newSurvey.id
            question.result = i.result
            question.save()
        questionSelect = QuestionQuota.objects.filter(survey_id=oldSurvey.id)
        for i in questionSelect:
            question = QuestionQuota()
            question.name = i.name
            question.result = i.result

            question.type = 6
            question.description = i.description
            question.sequenceNumber = i.sequenceNumber
            question.required = i.required
            question.survey_id = newSurvey.id
            question.save()
            option = QuestionQuotaOption.objects.filter(questionId=i.id)
            for j in option:
                k = QuestionQuotaOption()
                k.questionId = question.id
                k.quota = j.quota
                k.content = j.content
                k.save()
        questionSelect = QuestionPunch.objects.filter(survey_id=oldSurvey.id)
        for i in questionSelect:
            question = QuestionPunch()
            question.name = i.name
            question.result = i.result
            question.sequenceNumber = i.sequenceNumber
            question.required = i.required
            # question.context = i.context
            question.type = 7
            question.description = i.description
            question.survey_id = newSurvey.id
            question.save()
        red_dict = {'res': 1}
        smod = Survey.objects
        userid = data.get('userid')
        slist = smod.filter(status__lt=9).filter(user_id=userid)
        res = []
        for i in slist:
            print(i.id)
            res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                        "recovernum": i.recoveryNum,
                        "createtime": i.create_at.strftime('%Y-%m-%d '),
                        'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status, 'class': i.type}
            res.append(res_dict)
        red_dict['res'] = res
        return JsonResponse(red_dict)
    elif type == 7:
        id = data.get('survey_id')
        res_dict = {}
        rand = random.randint(100000, 999999)
        node = Node.objects.get(node=id)
        node.node = rand
        node.save()
        res_dict['link'] = internet + str(rand)
        photo = createQRcode(id, res_dict['link'])
        s = 'http://39.104.170.158:80/' + photo
        #s = 'http://localhost:8000/' + photo
        res_dict['photo'] = s
        return JsonResponse(res_dict)


def rank(request):
    try:
        '''浏览信息'''
        smod = Survey.objects
        slist = smod.filter(status__lt=9).filter(user_id=request.session['user']['id'])
        # 获取并判断搜索条件
        kw = request.GET.get("judge", 1)  # 1 默认是按照id排序
        if kw == 1:
            slist = slist.order_by("id")  # 对id排序
        elif kw == 2:
            slist = slist.order_by("-id", )
        elif kw == 3:
            slist = slist.order_by("recoveryNum")
        # # 执行分页处理
        # pIndex = int(pIndex)
        # page = Paginator(slist, 10)  # 以每页10条数据分页
        # maxpages = page.num_pages  # 获取最大页数
        # # 判断当前页是否越界
        # if pIndex > maxpages:
        #     pIndex = maxpages
        # if pIndex < 1:
        #     pIndex = 1
        # list2 = page.page(pIndex)  # 获取当前页数据
        # plist = page.page_range  # 获取页码列表信息
        # context = {"surveylist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages}
        res = []
        for i in slist:
            res_dict = {'id': i.id, 'name': i.name, "status": i.status, "recoverNum": i.recoveryNum,
                        "caretetime": i.create_at}
            res.append(res_dict)
        return JsonResponse(res)
    except Exception as err:
        print(err)
        res_dict = {}
        res_dict['res'] = 2
        return JsonResponse(res_dict)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        res_dict = {}
        data = json.loads(request.body)
        try:
            ob = User()
            ob.username = data.get('username')
            user = User.objects.filter(username=ob.username)
            if user:
                # return HttpResponse("username exists")
                res_dict['res'] = 3
                return JsonResponse(res_dict)

            ob.nickname = data.get('rename')

            s1 = data.get('password1')
            s2 = data.get('password2')
            if s1 != s2:
                # return HttpResponse("password is wrong")
                res_dict['res'] = 2
                return JsonResponse(res_dict)
            # 密码由6-18位构成，至少含有两种字符
            if len(str(s1)) < 6 or len(str(s1)) > 18:
                res_dict['res'] = 1
                response = JsonResponse(res_dict)
                return response
            n = m = 0
            for i in s1:
                if str.isdigit(i):
                    n = 1
                elif str.isalpha(i):
                    m = 1
                else:
                    res_dict['res'] = 1
                    return JsonResponse(res_dict)
            if n + m < 2:
                res_dict['res'] = 1
                return JsonResponse(res_dict)

            # 将当的密码做md5处理

            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = data.get('password1') + str(n)  # 从表单中获取密码并添加干扰值
            md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
            ob.password_hash = md5.hexdigest()  # 获取md5值
            ob.password_salt = n
            ob.status = 1
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            # context = {'info': "添加成功！"}
            res_dict['res'] = 4
            return JsonResponse(res_dict)
        except:
            res_dict['res'] = 5
            return JsonResponse(res_dict)


@csrf_exempt
# 登录表单
def login(request):
    try:
        # 执行验证码的校验
        # if request.POST['code'] != request.session['verifycode']:
        #   context = {"info": "验证码错误！"}
        #   return render(request, "#", context)
        res_dict = {}
        # 根据登录账号获取登录者信息
        data = json.loads(request.body)
        user = User.objects.get(username=data.get('username'))

        # 判断登录密码是否相同
        md5 = hashlib.md5()
        s = data.get('password') + user.password_salt  # 从表单中获取密码并添加干扰值

        md5.update(s.encode('utf-8'))
        if user.password_hash == md5.hexdigest():

            request.session['user'] = user.toDict()
            res_dict['res'] = 2
            res_dict['userid'] = user.id

            return JsonResponse(res_dict)
        else:
            res_dict['res'] = 1
            return JsonResponse(res_dict)
    except Exception as err:
        print(err)
        res_dict['res'] = 1
        return JsonResponse(res_dict)


@csrf_exempt
def logout(request):
    del request.session['user']
    return redirect(reverse("user_login"))


# 开启问卷

def openquestion(request):
    if request.method == 'POST':
        try:

            res_dict = {}
            res_dict['res'] = 1
            # createQRcode(1, "https://blog.csdn.net/zhoubihui0000/article/details/96367489")
            # return JsonResponse(res_dict)

            id = request.POST.get('surveyId')
            user = request.session['user']['id']
            question = Survey.objects.filter(id=id).filter(user_id=user)
            if not question:
                res_dict['res'] = 2
                return JsonResponse(res_dict)
            question.update(status=2)
            # 前端跳转网址未定
            res_dict['link'] = internet + id
            photo = createQRcode(id, res_dict['link'])
            res_dict['photo'] = photo
            return JsonResponse(res_dict)

        except Exception as error:
            print(error)
            res_dict['res'] = 3
            return JsonResponse(res_dict)


# 关闭问卷

def close(request):
    if request.method == 'POST':
        try:
            res_dict = {}
            id = request.POST.get('surveyId')
            user = request.session['user']['id']
            question = Survey.objects.filter(id=id).filter(user_id=user)
            if not question:
                res_dict['res'] = 2
                return JsonResponse(res_dict)
            question.update(status=3)
            res_dict['res'] = 1
            return JsonResponse(res_dict)
        except Exception as error:
            print(error)
            res_dict['res'] = 3
            return JsonResponse(res_dict)


@csrf_exempt
# 复制
def copy(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('surveyId')

            id = Node.objects.get(node=id).surveyId

            oldSurvey = Survey.objects.get(id=id)
            newSurvey = Survey()
            name = oldSurvey.name.split('(')[0]
            num = Survey.objects.filter(user_id=oldSurvey.user_id).filter(name_contains=name).count()
            num += 1
            newname = name + '(' + num + ')'
            newSurvey.name = newname
            newSurvey.status = 0
            newSurvey.user_id = oldSurvey.user_id
            newSurvey.save()
            questionSelect = QuestionSelect.objects.filter(surveyId=oldSurvey.id)
            for i in questionSelect:
                question = QuestionSelect()
                question.name = i.name
                question.result = i.result
                question.type = 1
                question.description = i.description
                question.sequenceNumber = i.sequenceNumber
                question.required = i.required
                question.survey_id = newSurvey.id
                question.save()
                option = Option.objects.filter(questionId=i.id)
                for j in option:
                    k = Option()
                    k.questionId = question.id
                    k.content = j.content
                    k.save()
            questionSelect = QuestionMulSelect.objects.filter(surveyId=oldSurvey.id)
            for i in questionSelect:
                question = QuestionMulSelect()
                question.name = i.name
                question.type = 2
                question.description = i.description
                question.result = i.result
                question.sequenceNumber = i.sequenceNumber
                question.required = i.required
                question.survey_id = newSurvey.id
                question.save()
                option = MulOption.objects.filter(questionId=i.id)
                for j in option:
                    k = MulOption()
                    k.questionId = question.id
                    k.content = j.content
                    k.save()
            questionSelect = QuestionFillBlank.objects.filter(surveyId=oldSurvey.id)
            for i in questionSelect:
                question = QuestionFillBlank()
                question.name = i.name
                question.result = i.result
                question.sequenceNumber = i.sequenceNumber
                question.required = i.required
                # question.context = i.context
                question.type = 3
                question.description = i.description
                question.correctAnswers = 0
                question.wrongAnswers = 0
                question.survey_id = newSurvey.id
                question.save()
            questionremark = QuestionRemark.objects.filter(survey_id=oldSurvey.id)
            for i in questionremark:
                question = QuestionRemark()
                question.name = i.name
                question.status = 4
                question.required = i.required
                question.sequenceNumber = i.sequenceNumber
                question.description = i.description
                question.survey_id = newSurvey.id
                question.result = i.result
                question.save()
            questionjudgement = QuestionJudgement.objects.filter(survey_id=oldSurvey.id)
            for i in questionjudgement:
                question = QuestionJudgement()
                question.name = i.name
                question.type = 5
                question.required = i.required
                question.sequenceNumber = i.sequenceNumber
                question.description = i.description
                question.survey_id = newSurvey.id
                question.result = i.result
                question.save()
            res_dict = {'res': 1}

            return JsonResponse(res_dict)
        except Exception as error:
            print(error)
            res_dict = {'res': 2}
            return JsonResponse(res_dict)


@csrf_exempt
# # 删除
# def delete(request):
#     if request.method == 'GET':
#         try:
#             Survey.objects.filter(id=request.GET.get('SurveyId')).update(status=9)
#             res_dict = {'res': 1}
#         except Exception as error:
#             print(error)
#             res_dict = {'res': 2}
#         return JsonResponse(res_dict)

# 输出验证码
def verify(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = '0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('static/arial.ttf', 21)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

    # def edit(request):
    '''加载信息编辑表单'''
    # try:
    #     sb = Survey.objects.get(id=request.GET.get("id"))
    #     category = request.GET.get("category")
    #     if category == 1:
    #         insertquestion(sb, category)
    #     elif category == 2:
    #         insertquestion(sb, category)
    #     elif category == 3:
    #         insertquestion(sb, category)       有待继续讨论
    #     elif category == 4:
    #         insertquestion(sb, category)
    #     context = {'survey': sb}
    #
    #     return HttpResponse(context)
    # except Exception as err:
    #     print(err)
    #     context = {'info': "没有找到要修改的信息！"}
    #     return HttpResponse(context)


def insertquestion(request, sb, categroy):
    if categroy == 1:
        newquestion = QuestionSelect()
        newquestion.name = request.POST.get("name")
        newquestion.status = 1
        newquestion.ChoiceA = request.POST.get("choiceA")
        newquestion.ChoiceB = request.POST.get("choiceB")
        newquestion.ChoiceC = request.POST.get("choiceC")
        newquestion.ChoiceD = request.POST.get("choiceD")
        newquestion.required = request.POST.get("required")  # 是否必填
        newquestion.survey_id = sb.id
        newquestion.description = request.POST.get("description")
        newquestion.save()
    if categroy == 2:
        newquestion = QuestionMulSelect()
        newquestion.name = request.POST.get("name")
        newquestion.status = 1
        newquestion.ChoiceA = request.POST.get("choiceA")
        newquestion.ChoiceB = request.POST.get("choiceB")
        newquestion.ChoiceC = request.POST.get("choiceC")
        newquestion.ChoiceD = request.POST.get("choiceD")
        newquestion.required = request.POST.get("required")  # 是否必填
        newquestion.survey_id = sb.id
        newquestion.description = request.POST.get("description")
        newquestion.save()
    if categroy == 1:
        newquestion = QuestionSelect()
        newquestion.name = request.POST.get("name")
        newquestion.status = 1
        newquestion.ChoiceA = request.POST.get("choiceA")
        newquestion.ChoiceB = request.POST.get("choiceB")
        newquestion.ChoiceC = request.POST.get("choiceC")
        newquestion.ChoiceD = request.POST.get("choiceD")
        newquestion.required = request.POST.get("required")  # 是否必填
        newquestion.survey_id = sb.id
        newquestion.save()
    if categroy == 1:
        newquestion = QuestionSelect()
        newquestion.name = request.POST.get("name")
        newquestion.status = 1
        newquestion.ChoiceA = request.POST.get("choiceA")
        newquestion.ChoiceB = request.POST.get("choiceB")
        newquestion.ChoiceC = request.POST.get("choiceC")
        newquestion.ChoiceD = request.POST.get("choiceD")
        newquestion.required = request.POST.get("required")  # 是否必填
        newquestion.survey_id = sb.id
        newquestion.save()


def shuffle(request, sid, comp=lambda x, y: x > y):
    # 读取问题
    questionselect = QuestionSelect.objects.filter(survey_id=sid)
    questionmulselect = QuestionMulSelect.objects.filter(survey_id=sid)
    questionremark = QuestionRemark.objects.filter(survey_id=sid)
    questionfillblank = QuestionFillBlank.objects.filter(survey_id=sid)
    questionjudgement = QuestionJudgement.objects.filter(survey_id=sid)
    question = questionfillblank + questionmulselect + questionselect + questionremark + questionjudgement
    num_examples = len(question)
    indices = list(range(num_examples))
    random.shuffle(indices)  # 样本的读取顺序是随机的
    for i in range(num_examples):
        question[i].sequenceNumber = indices[i] + 1

    for i in range(num_examples - 1):
        swapped = False
        for j in range(num_examples - 1 - i):
            if comp(question[j].sequenceNumber, question[j + 1].sequenceNumber):
                question[j], question[j + 1] = question[j + 1], question[j]
                swapped = True
        if not swapped:
            break
    context = {'questionlist': question}  # question是问提列表
    return HttpResponse(context)


def createPDF(request):
    data = {'msg': "星震宇123abc"}
    template = get_template('1.html')
    html = template.render(data)
    file = open('test.pdf', "wb+")
    font_patch()
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    file.seek(0)
    pdf = file.read()
    file.close()
    os.remove('test.pdf')
    return HttpResponse(pdf, 'application/pdf')


def createQRcode(surveyId, str):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )  # 设置二维码的大小
    qr.add_data(str)
    qr.make(fit=True)
    img = qr.make_image()
    string = "media/photos/%s.png" % surveyId
    img.save(string)
    return string


def font_patch():
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from xhtml2pdf.default import DEFAULT_FONT
    pdfmetrics.registerFont(TTFont('yh', '{}/font/msyh.ttf'.format(
        settings.BASE_DIR)))
    DEFAULT_FONT['helvetica'] = 'yh'


def get_select_data(request):
    sid = request.POST.get('id')
    queryset1 = QuestionSelect.objects.filter(survey_id=sid)  # 得到所有问题
    names1 = [question.name for question in queryset1]  # 得到所有问题的名称
    options = {}
    for i, question in enumerate(queryset1):
        options['i'] = Option.objects.filter(questionId=question.id)  # 得到options字典，存储question的选项
    numbers = {}
    for i, options in enumerate(options):
        numbers['i'] = [option.numbers for option in options]  # 得到numbers字典，存储question选项的人数
    result1 = [question.result for question in queryset1]  # 得到答案字典
    return JsonResponse(
        {'names': names1, "options": options, "result": result1, "numbers": numbers})


def get_mulselect_data(request):
    sid = request.POST.get('id')
    queryset1 = QuestionSelect.objects.filter(survey_id=sid)  # 得到所有问题
    names1 = [question.name for question in queryset1]  # 得到所有问题的名称
    options = {}
    for i, question in enumerate(queryset1):
        options['i'] = MulOption.objects.filter(questionId=question.id)  # 得到options字典，存储question的选项
    numbers = {}
    for i, options in enumerate(options):
        numbers['i'] = [option.numbers for option in options]  # 得到numbers字典，存储question选项的人数
    result1 = [question.result for question in queryset1]  # 得到答案字典
    return JsonResponse(
        {'names': names1, "options": options, "result": result1, "numbers": numbers})


def get_fillbank_data(request):
    sid = request.POST.get('id')
    queryset1 = QuestionFillBlank.objects.filter(survey_id=sid)
    names1 = [question.name for question in queryset1]
    result = [question.result for question in queryset1]
    rights = [question.correctAnswers for question in queryset1]
    wrongs = [question.wrongAnswers for question in queryset1]
    return JsonResponse(
        {'names': names1, 'rights': rights, 'wrongs': wrongs, "result": result})


def get_remark_data(request):
    sid = request.POST.get('id')
    queryset1 = QuestionRemark.objects.filter(survey_id=sid)
    names1 = [question.name for question in queryset1]
    score1 = [question.score1 for question in queryset1]  # 打一星的人数
    score2 = [question.score2 for question in queryset1]
    score3 = [question.score3 for question in queryset1]
    score4 = [question.score4 for question in queryset1]
    score5 = [question.score5 for question in queryset1]
    return JsonResponse(
        {'names': names1, 'score1': score1, 'score2': score2, 'score3': score3, 'score4': score4, 'score5': score5})


def get_judgement_data(request):
    sid = request.POST.get('id')
    queryset1 = QuestionJudgement.objects.filter(survey_id=sid)
    names1 = [question.name for question in queryset1]
    result = [question.result for question in queryset1]
    rights = [question.correctAnswers for question in queryset1]
    wrongs = [question.wrongAnswers for question in queryset1]
    return JsonResponse(
        {'names': names1, 'rights': rights, 'wrongs': wrongs, 'result': result})


def edit(request):
    if request.method == 'POST':
        # try:
        res_dict = {}

        data = json.loads(request.body)
        id = data.get('id')
        print(id)
        if id:
            if id != '2333333':
                x = Node.objects.get(node=id)
                Survey.objects.filter(id=x.surveyId).delete()
                x.delete()
        survey = Survey()
        question = data.get('survey')
        survey.type = data.get('class')
        kind = survey.type
        res_dict['sad'] = kind
        survey.isNeed = data.get('needOrder')
        survey.name = data.get('titleContent')
        survey.description = data.get('info')
        if data.get('class') == 6:
            survey.quota = data.get('surveyNum')
        survey.user_id = data.get('userid')
        survey.stop_at = data.get('stopTime')
        # survey.stop_at = datetime.now()
        survey.status = 0
        survey.save()

        rand = random.randint(100000, 999999)
        node = Node()
        node.surveyId = survey.id
        node.node = rand
        node.save()
        for i in question:

            if i['type'] == 1:

                q = QuestionSelect()
                q.type = 1
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.status = 1
                if survey.type == 4:
                    if i['point']:
                        if i['point'] >= 0:
                            q.score = i['point']
                    if i['correctAnswer']:
                        q.result = i['correctAnswer']
                q.sequenceNumber = i['number']
                q.description = i['description']
                q.save()

                for j in i['choices']:
                    option = Option()
                    option.questionId = q.id
                    option.content = j
                    option.save()
            elif i['type'] == 2:
                q = QuestionMulSelect()
                q.type = 2
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.sequenceNumber = i['number']
                q.description = i['description']
                if survey.type == 4:
                    if i['point']:
                        if i['point'] >= 0:
                            q.score = i['point']
                    if i['correctAnswer']:
                        string = ''
                        for j in i['correctAnswer']:
                            string += str(j)

                        q.result = string
                q.save()
                for j in i['choices']:
                    option = MulOption()
                    option.questionId = q.id
                    option.content = j
                    option.save()
            elif i['type'] == 3:

                q = QuestionFillBlank()
                q.type = 3
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.sequenceNumber = i['number']
                q.description = i['description']
                if survey.type == 4:
                    if i['point']:
                        if i['point'] > 0:
                            q.score = i['point']
                    if i['correctAnswer']:
                        q.result = i['correctAnswer']
                q.save()
            elif i['type'] == 4:
                q = QuestionRemark()
                q.type = 4
                q.starNum = i['choices']
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.sequenceNumber = i['number']

                q.description = i['description']
                if survey.type == 4:
                    if i['point']:
                        if i['point'] >= 0:
                            q.score = i['point']
                    if i['correctAnswer']:
                        q.result = i['correctAnswer']
                q.save()
            elif i['type'] == 5:
                q = QuestionJudgement()
                q.type = 5
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.sequenceNumber = i['number']
                q.description = i['description']
                res_dict['happy'] = kind
                res_dict['hahah'] = survey.type
                if survey.type == 4:

                    if i['point']:
                        if i['point'] >= 0:
                            q.score = i['point']
                    if i['correctAnswer'] == 0 or i['correctAnswer'] == 1:
                        q.result = i['correctAnswer']

                q.save()
            elif i['type'] == 6:
                q = QuestionQuota()
                q.type = 6
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.status = i['status']
                q.sequenceNumber = i['number']
                q.description = i['description']
                if survey.type == 4:

                    if i['correctAnswer']:
                        i['correctAnswer'].sort()
                        string = ""
                        for p in i['correctAnswer']:
                            string += str(p)
                        q.result = string
                q.save()
                for j in i['choices']:
                    option = QuestionQuotaOption()
                    option.questionId = q.id
                    option.content = j['content']
                    option.quota = j['limit']
                    option.save()
            elif i['type'] == 7:
                q = QuestionPunch()
                q.type = 7
                q.survey_id = survey.id
                q.required = i['must']
                q.name = i['title']
                q.status = i['status']
                q.sequenceNumber = i['number']
                q.description = i['description']
                if survey.type == 4:
                    if i['point'] >= '0':
                        q.score = i['point']
                    if i['correctAnswer']:
                        i['correctAnswer'].sort()
                        string = ""
                        for p in i['correctAnswer']:
                            string += str(p)
                        q.result = string
                q.save()
        res_dict['res'] = 1
        xtype = data.get('type')
        res_dict['type'] = xtype

        if xtype == int(2):
            # id = request.POST.get('surveyId')
            # user = request.session['user']['id']
            # question = Survey.objects.filter(id=id).filter(user_id=user)
            # if not question:
            #     res_dict['res'] = 2
            #     return JsonResponse(res_dict)
            # question.update(status=2)
            # 前端跳转网址未定
            survey.status = 1
            survey.save()
            res_dict['link'] = internet + str(rand)
            photo = createQRcode(survey.id, res_dict['link'])
            s = 'http://39.104.170.158:80/' + photo
            #s = 'http://localhost:8000/' + photo
            res_dict['photo'] = s
        return JsonResponse(res_dict)
    # except Exception as err:
    #     print(err)
    #     res_dict['res'] = 2
    #     return JsonResponse(res_dict)


def recycle_bin(request):
    if request.method == 'POST':
        r = {}
        try:
            data = json.loads(request.body)
            user_id = data.get('userid')
            type = data.get('type')

            if type == 1:
                slist = Survey.objects.filter(user_id=user_id).filter(status=9)
                res = []
                for i in slist:
                    res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                                "recovernum": i.recoveryNum,
                                "createtime": i.create_at.strftime('%Y-%m-%d '),
                                'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status}
                    res.append(res_dict)
                r['res'] = res
            elif type == 2:
                survey_id = data.get('survey_id')
                Survey.objects.filter(id=Node.objects.get(node=survey_id).surveyId).update(status=0)
                slist = Survey.objects.filter(user_id=user_id).filter(status=9)
                res = []
                for i in slist:
                    res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                                "recovernum": i.recoveryNum,
                                "createtime": i.create_at.strftime('%Y-%m-%d '),
                                'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status}
                    res.append(res_dict)
                r['res'] = res
            elif type == 3:
                survey_id = data.get('survey_id')
                node = Node.objects.get(node=survey_id)
                Survey.objects.filter(id=node.surveyId).delete()
                slist = Survey.objects.filter(user_id=user_id).filter(status=9)
                res = []
                for i in slist:
                    res_dict = {'id': Node.objects.get(surveyId=i.id).node, 'name': i.name, "status": i.status,
                                "recovernum": i.recoveryNum,
                                "createtime": i.create_at.strftime('%Y-%m-%d '),
                                'publish_at': i.update_at.strftime('%Y-%m-%d '), 'publish': i.status}
                    res.append(res_dict)
                r['res'] = res
            elif type == 4:
                Survey.objects.filter(user_id=user_id).filter(status=9).delete()
                r['data'] = 1
            return JsonResponse(r)
        except Exception as error:
            print(error)
            r['wq'] = 1
            return JsonResponse(r)


def analysis(request):
    if request.method == 'GET':

        surveyId = request.GET.get('id')
        surveyId = Node.objects.get(node=surveyId).surveyId
        survey = Survey.objects.get(id=surveyId)
        if survey.type != 4:
            res_dict = {}
            res_dict['totalNum'] = survey.recoveryNum
            res_dict['name'] = survey.name
            res_dict['class'] = survey.type
            s = []
            q = QuestionSelect.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                data = QuestionSelectData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = Option.objects.filter(questionId=i.id).count()
                sum = data.count()
                answer = []
                for j in data:
                    answer.append(j.answer)
                chooseNumber = []
                chooseRatio = []
                for j in range(1, num + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionMulSelect.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                data = QuestionMulSelectData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = MulOption.objects.filter(questionId=i.id).count()
                sum = data.count()
                answer = []
                for j in data:
                    for k in j.answer:
                        answer.append(int(k))
                chooseNumber = []
                chooseRatio = []
                for j in range(1, num + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['answer'] = answer
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionRemark.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                data = QuestionRemarkData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = MulOption.objects.filter(questionId=i.id).count()
                sum = data.count()
                answer = []
                for j in data:
                    answer.append(j.answer)
                chooseNumber = []
                chooseRatio = []
                for j in range(1, i.starNum + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionJudgement.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                chooseNumber = []
                chooseNumber.append(i.correctAnswers)
                chooseNumber.append(i.wrongAnswers)
                chooseRatio = []
                sum = i.correctAnswers + i.wrongAnswers

                rate = float(i.correctAnswers / sum)
                rate1 = round(rate, 6)
                turnover_rate = format(rate1, '.4%')
                chooseRatio.append(turnover_rate)
                rate = float(i.wrongAnswers / sum)
                rate1 = round(rate, 6)
                turnover_rate = format(rate1, '.4%')
                chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionQuota.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                data = QuestionQuotaData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = QuestionQuotaOption.objects.filter(questionId=i.id).count()
                sum = data.count()
                answer = []
                for j in data:
                    answer.append(j.answer)
                chooseNumber = []
                chooseRatio = []
                for j in range(1, num + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            list1 = sorted(s, key=operator.itemgetter("quesnumber"))
            res_dict['statistic'] = list1
        elif survey.type == 4:
            res_dict = {}
            res_dict['totalNum'] = survey.recoveryNum
            res_dict['name'] = survey.name
            res_dict['class'] = survey.type
            s = []
            q = QuestionSelect.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['correctAnswer'] = i.result
                w['type'] = i.type
                w['point'] = i.score
                w['correctAnswer'] = i.result
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                data = QuestionSelectData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = Option.objects.filter(questionId=i.id).count()
                sum = data.count()
                answer = []
                for j in data:
                    answer.append(j.answer)
                chooseNumber = []
                chooseRatio = []
                for j in range(1, num + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionMulSelect.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['point'] = i.score
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                data = QuestionMulSelectData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = MulOption.objects.filter(questionId=i.id).count()
                sum = data.count()
                correct = 0
                answer = []
                string = ""
                x = []
                for t in i.result:
                    x.append(t)
                x.sort()
                for i in x:
                    string += i
                for j in data:
                    if string == j.answer:
                        correct += 1
                    for k in j.answer:
                        answer.append(int(k))
                chooseNumber = []
                chooseRatio = []
                w['correctRatio'] = format(round(float(correct / sum), 6), '.4%')
                for j in range(1, num + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['correctAnswer'] = string
                w['correctNumber'] = correct

                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionRemark.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['type'] = i.type
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                w['point'] = i.score
                w['correctAnswer'] = i.result
                data = QuestionRemarkData.objects.filter(sequenceNumber=i.sequenceNumber).filter(survey_id=surveyId)
                num = MulOption.objects.filter(questionId=i.id).count()
                sum = data.count()
                answer = []
                for j in data:
                    answer.append(j.answer)
                chooseNumber = []
                chooseRatio = []
                for j in range(1, i.starNum + 1):
                    chooseNumber.append(answer.count(j))
                    rate = float(answer.count(j) / sum)
                    rate1 = round(rate, 6)
                    turnover_rate = format(rate1, '.4%')
                    chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            q = QuestionJudgement.objects.filter(survey_id=surveyId)
            for i in q:
                w = {}
                w['title'] = i.name
                w['point'] = i.score
                w['type'] = i.type
                w['correctAnswer'] = i.result
                w['quesnumber'] = i.sequenceNumber
                w['isRequired'] = i.required
                chooseNumber = []
                chooseNumber.append(i.correctAnswers)
                chooseNumber.append(i.wrongAnswers)
                chooseRatio = []
                sum = i.correctAnswers + i.wrongAnswers

                rate = float(i.correctAnswers / sum)
                rate1 = round(rate, 6)
                turnover_rate = format(rate1, '.4%')
                chooseRatio.append(turnover_rate)
                rate = float(i.wrongAnswers / sum)
                rate1 = round(rate, 6)
                turnover_rate = format(rate1, '.4%')
                chooseRatio.append(turnover_rate)
                w['chooseNumber'] = chooseNumber
                w['chooseRatio'] = chooseRatio
                s.append(w)
            list1 = sorted(s, key=operator.itemgetter("quesnumber"))
            res_dict['statistic'] = list1
        return JsonResponse(res_dict)


def link(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        surveyId = data.get('surveyId')
        res_dict = {}
        rand = random.randint(100000, 999999)
        node = Node.objects.get(surveyId=surveyId)
        node.node = rand
        node.save()
        res_dict['link'] = internet + str(rand)
        photo = createQRcode(rand, res_dict['link'])
        s = 'http://39.104.170.158:80/' + photo
        #s = 'http://localhost:8000/' + photo
        res_dict['photo'] = s
        return JsonResponse(res_dict)


# name 问卷名
# totalNum 数据量
# statistic 用户数组
# username
# date填写时间
# choices 题目数组
#
def printf(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        id = Node.objects.get(node=id).surveyId
        res_dict = {}
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="myfile.csv"'
        writer = csv.writer(response)
        survey = Survey.objects.get(id=id)
        record = Record.objects.filter(survey_id=id)
        res_dict['name'] = survey.name
        res_dict['totalNum'] = record.count()

        count = 0
        count += QuestionSelect.objects.filter(survey_id=id).count()
        count += QuestionMulSelect.objects.filter(survey_id=id).count()
        count += QuestionFillBlank.objects.filter(survey_id=id).count()
        count += QuestionRemark.objects.filter(survey_id=id).count()
        count += QuestionJudgement.objects.filter(survey_id=id).count()
        count += QuestionQuota.objects.filter(survey_id=id).count()
        count += QuestionPunch.objects.filter(survey_id=id).count()
        s = []
        s.append('用户名')
        s.append('填写时间')
        for i in range(1, count + 1):
            s.append('第%d题' % i)
        writer.writerow(s)
        for i in record:
            r = {}
            choices = []
            r['username'] = i.username
            r['date'] = i.submitTime
            data = QuestionSelectData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = chr(ord('A') + i.answer - 1)
                choices.append(a)
            data = QuestionMulSelectData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                string = ""
                for j in i.answer:
                    string += chr(ord('A') + int(j) - 1)
                a['answer'] = string
                choices.append(a)
            data = QuestionFillBlankData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            data = QuestionRemarkData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            data = QuestionJudgementData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            data = QuestionPunchData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            list1 = sorted(choices, key=operator.itemgetter("sequenceNumber"))
            choices = []
            choices.append(r['username'])
            choices.append(r['date'])
            for j in list1:
                choices.append(j['answer'])
            writer.writerow(choices)
        return response


def analysisForUser(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        res_dict = {}
        node = Node.objects.get(node=id)
        id = node.surveyId
        survey = Survey.objects.get(id=id)
        record = Record.objects.filter(survey_id=id)
        res_dict['name'] = survey.name
        res_dict['totalNum'] = record.count()
        statistic = []
        for i in record:
            r = {}
            choices = []
            r['username'] = i.username
            r['date'] = i.submitTime
            data = QuestionSelectData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = chr(ord('A') + i.answer - 1)
                choices.append(a)
            data = QuestionMulSelectData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                string = ""
                for j in i.answer:
                    string += chr(ord('A') + int(j) - 1)
                a['answer'] = string
                choices.append(a)
            data = QuestionFillBlankData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            data = QuestionRemarkData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            data = QuestionJudgementData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                if i.answer == 0:
                    a['answer'] = 'True'
                else:
                    a['answer'] = 'False'
                choices.append(a)
            data = QuestionQuotaData.objects.filter(survey_id=id).filter(ip=i.ip)
            for i in data:
                a = {}
                a['sequenceNumber'] = i.sequenceNumber
                a['answer'] = i.answer
                choices.append(a)
            list1 = sorted(choices, key=operator.itemgetter("sequenceNumber"))
            r['choices'] = list1
            statistic.append(r)
        print(statistic)
        res_dict['statistic'] = statistic
        return JsonResponse(res_dict)
