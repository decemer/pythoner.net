#encoding:utf-8
import random
import json
from django.http import HttpResponseBadRequest, HttpResponseNotFound,HttpResponse
from wiki.models import *
from wiki.signals import *
from accounts.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add(request):
    response = {'status':0,'info':''}
    if request.method == 'GET':
        response['info'] = 'Invalide method'
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)

    user_id = int(request.REQUEST.get('user',0))
    try:
        cat = request.REQUEST.get('category')
        category = Category.objects.get(name=cat)
    except:
        category = Category.objects.get(name=u'其它python相关')

    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=random.randrange(2,10))

    new_wiki          = Entry()
    new_wiki.author   = user
    new_wiki.title    = request.REQUEST.get('title')
    new_wiki.content  = request.REQUEST.get('content')
    new_wiki.category = category
    new_wiki.source   = request.REQUEST.get('source')
    new_wiki.public   = True

    if not new_wiki.title or not new_wiki.content:
        response['status'] = 0
        response['info'] = 'params error'
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)

    try:
        new_wiki.save()
    except Exception,e:
        response['info'] = e.message
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)

    # 发送信号
    print 13
    new_wiki_was_post.send( sender= new_wiki.__class__,wiki=new_wiki)
    
    response['status']  = 1
    response['new_wiki_id'] = new_wiki.id
    print new_wiki.title
    print response
    return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)


@csrf_exempt
def edit(request):
    if request.method == 'GET':
        return HttpResponseBadRequest('error method')

    response = {'status':0,'info':''}
    wiki_id  = request.REQUEST.get('wiki_id')
    try:
        wiki = Entry.objects.get(id=wiki_id)
    except:
        response['info'] = 'wiki {0} does not exist '.format(wiki_id)
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)

    user_id = int(request.REQUEST.get('user',0))
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(id=random.randrange(2,10))

    try:
        cat = request.REQUEST.get('category')
        category = Category.objects.get(name=cat)
    except:
        category = Category.objects.get(name='其它python相关')

    
    wiki.author   = user
    wiki.title    = request.REQUEST.get('title')
    wiki.content  = request.REQUEST.get('content')
    wiki.category = category
    wiki.source   = request.REQUEST.get('source')

    try:
        wiki.save()
    except Exception,e:
        response['info'] = e.message
        return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)
    response['status']  = 1
    return HttpResponse(json.dumps(response), mimetype='application/json; charset=utf-8',status=200)
