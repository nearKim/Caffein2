import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from accounts.models import User
from .models import Form, Question, Choice, UserAnswer
from core.models import OperationScheme


class FormListView(LoginRequiredMixin, ListView):
    model = Form
    template_name = 'survey/survey_list.html'


class FormCreate(LoginRequiredMixin, CreateView):
    model = Form
    template_name = 'survey/survey_create.html'
    fields = '__all__'

    def post(self, request):
        result = {"result": "", "error_reason": ""}
        unicode_body = request.body.decode('utf-8')
        dict_post_data = json.loads(unicode_body)
        # 질문 제목을 정상적으로 입력한 경우
        if len(dict_post_data['questions']) > 0:
            form = Form(title=dict_post_data['form_title'],
                        description=dict_post_data['form_description'],
                        owner=self.request.user,
                        purpose=dict_post_data['purpose'])
            form.save()
            result['result'] = '정상적으로 저장되었습니다.'
            for question_item in dict_post_data['questions']:
                question = Question(question_text=question_item['text'],
                                    question_type=question_item['type'],
                                    form=form)
                question.save()
                if question_item['type'] == 'choice_one' or question_item['type'] == 'choice_many':
                    for choice_item in question_item['options']:
                        choice = Choice(choice_text=choice_item,
                                        question=question)
                        choice.save()
        # 질문 제목을 입력하지 않은 경
        else:
            result['result'] = '질문 제목을 입력해주세요.'
        return HttpResponse(json.dumps(result))


# user id와 form의 pk를 넘겨받음. 해당 form의 question, choice를 반환하거나, 결과 제출.
@login_required
def survey_fill(request, user_id, pk):
    if request.method == 'GET':
        form = Form.objects.get(id=pk)
        questions = Question.objects.filter(form=form)
        questions = list(questions)
        questions.reverse()
        choices = Choice.objects.filter(question__in=questions)
        context = {
            'form': form,
            'questions': questions,
            'choices': choices,
            'can_register': OperationScheme.can_old_register()
        }
        return render(request, 'survey/survey_fill.html', context)
    elif request.method == 'POST':
        user = User.objects.get(id=user_id)
        form = Form.objects.get(id=pk)
        form.users.add(user)
        form.save()
        questions = Question.objects.filter(form=form)
        for question in questions:
            if question.question_type == 'choice_many':
                all_answer = request.POST.getlist(question.question_text)
                answer = ''
                for text in all_answer:
                    answer += text + ','
                answer = answer[:-1]
            else:
                answer = request.POST.get(question.question_text)
            UserAnswer.objects.create(question=question,
                                      answer=answer,
                                      form=form,
                                      user=user)
        info = OperationScheme.latest()
        context = {
            'purpose': form.purpose,
            'bank': info.get_bank_display(),
            'account': info.bank_account,
            'boss_name': info.boss.user.name,
            'pay': info.old_pay
        }
        return render(request, 'survey/survey_fill_submit.html', context)


# 신입 가입을 위한 함수. 로그인이 필요 없이 동작.
def survey_fill_new(request, user_id):
    if request.method == 'GET':
        try:
            # 가장 최근의 신입양식을 보여줌
            form = Form.objects.filter(purpose='join_new', opened=True)[0]
            questions = Question.objects.filter(form=form)
            questions = list(questions)
            questions.reverse()
            choices = Choice.objects.filter(question__in=questions)
        # 신입 가입을 위한 양식이 없는 경우 예외처리
        except (ObjectDoesNotExist, IndexError):
            form = None
            questions = ''
            choices = ''
        context = {
            'user_id': user_id,
            'form': form,
            'questions': questions,
            'choices': choices,
            'can_register': OperationScheme.can_new_register()
        }
        return render(request, 'survey/survey_fill_new.html', context)
    elif request.method == 'POST':
        user = User.objects.get(id=user_id)
        form = Form.objects.filter(purpose='join_new', opened=True)[0]
        form.users.add(user)
        form.save()
        questions = Question.objects.filter(form=form)
        # choice_many의 경우 여러 응답을 표시
        for question in questions:
            if question.question_type == 'choice_many':
                all_answer = request.POST.getlist(question.question_text)
                answer = ''
                for text in all_answer:
                    answer += text + ','
                answer = answer[:-1]
            else:
                answer = request.POST.get(question.question_text)
            UserAnswer.objects.create(question=question,
                                      answer=answer,
                                      form=form,
                                      user=user)
        info = OperationScheme.latest()
        context = {
            'purpose': form.purpose,
            'bank': info.get_bank_display(),
            'account': info.bank_account,
            'boss_name': info.boss.user.name,
            'pay': info.new_pay
        }
        return render(request, 'survey/survey_fill_submit.html', context)


# 응답 결과를 표시. 같은 form에 같은 user가 복수의 응답을 한 경우에는 최신 응답만 표시
@login_required
def survey_result(request, pk):
    form = Form.objects.get(id=pk)
    answers = UserAnswer.objects.filter(form=form)
    users = form.users.all()
    lists = []
    for user in users:
        user_answer = list(answers.filter(user=user).order_by('created'))[-len(form.question_set.all()):]
        user_answer.reverse()
        lists.append({
            'user': user,
            'user_answer': user_answer
        })
    context = {
        'lists': lists,
    }
    return render(request, 'survey/survey_result.html', context)


@login_required
def delete_form(request, pk):
    form = Form.objects.get(id=pk)
    form.delete()
    return redirect('survey:survey-list')


# form의 상태를 open, close로 변화
@login_required
def change_form_state(request, pk):
    form = Form.objects.get(id=pk)
    if form.opened:
        form.opened = False
    else:
        form.opened = True
    form.save()
    return redirect('survey:survey-list')
