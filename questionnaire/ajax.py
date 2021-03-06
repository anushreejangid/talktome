from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from dajax.core import Dajax
from datetime import datetime
from datetime import timedelta
from datetime import time
from datetime import date
from questionnaire.models import *
import jsonpickle
from django.db.models import Q
from django.template.loader import get_template
from django.template import RequestContext
from django.template import Context
from django.conf import settings
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Min
@dajaxice_register()
def response_user(request,question,option):
    dajax = Dajax()
    user = request.user
    question = Ques.objects.get(pk=question)
    option = Option.objects.get(pk=option)
    ques_bank = question.ques_bank
    answer = Answer.objects.get(question=question)
    ques=Ques.objects.filter(ques_bank__name=ques_bank)
    #sub_name=Sub_Qb.objects.filter(ques_bank__name=ques_bank)
    #for s in sub_name:
     #print s.subject
    ques_count=Ques.objects.filter(ques_bank__name=ques_bank).count()
    print "number of questions in this set"
    print ques_count
    response = Response(question=question, response=option, user=user)
    response.save()
    try:
        user_score = UserScore.objects.get(user=user, ques_bank=ques_bank)
    except (UserScore.DoesNotExist):
        user_score = UserScore(user=user, ques_bank=ques_bank, score=0)
    if answer.option == option:
        user_score.score = user_score.score + question.score
    user_score.save()
    get_mid=Ques.objects.filter(ques_bank__name=ques_bank).aggregate(Min('id') )
    quesno = int(request.COOKIES.get('quesno',0))
    max_age = 14*24*60*60 # two weeks
    expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    if(quesno < (ques_count-1)):
        print "here"
        question = Ques.objects.get(pk=(quesno+get_mid['id__min']))
        ques_bank = question.ques_bank
        ques_list = Ques.objects.filter(ques_bank=ques_bank)
        question = ques_list[quesno+1]
        #print question
        option = Option.objects.filter(question__id=question.id)
        context = RequestContext(request,{'question':question,'opt_list':option,'q_counter':quesno+2})
        template = get_template('questionnaire/mcq_template.html')
        content = template.render(context)
        #data = serializers.serialize('json', [question ,], fields=('content'))
        #data = simplejson.dumps( [{'content': question.content}] )
        #print data.content
        #quesno = quesno + 1
        print quesno
        dajax.add_data({'name':'quesno', 'value':quesno+1},"setCookie")
        print dajax.json()
        dajax.assign('#form_section', 'innerHTML',content)
        print content
    else:
        print "I am here now"
        context = RequestContext(request,{'user_score':user_score.score})
        template = get_template('questionnaire/score.html')
        content = template.render(context)
        dajax.assign('#form_section', 'innerHTML',content)
    return dajax.json()