
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json

from .models import Form, Question, Choice, UserAnswer


class FormListView(LoginRequiredMixin, ListView):
    model = Form
    def get_queryset(self):
        return Form.objects.filter()


class FormCreate(LoginRequiredMixin, CreateView):
    model = Form
    template_name = 'survey/form_create.html'
    fields = '__all__'

    def post(self, request):
        result = {"result": "", "error_reason": ""}
        unicode_body = request.body.decode('utf-8')
        dict_post_data = json.loads(unicode_body)
        if len(dict_post_data['questions']) > 0:
            form = Form.objects.create(title=dict_post_data['form_title'],
                                       description=dict_post_data['form_description'],
                                       owner=self.request.user)
            result['result'] = 'Form saved successfully'
            for question_item in dict_post_data['questions']:
                question = Question(question_text=question_item['text'],
                                    question_type=question_item['type'],
                                    form=form)
                question.save()
                if question_item['type'] == 'mcq_one' or question_item['type'] == 'mcq_many':
                    for choice_item in question_item['options']:
                        choice = Choice(choice_text=choice_item,
                                        question=question)
                        choice.save()
        else:
            result['result'] = 'Add a question title'
        return HttpResponse(json.dumps(result))

@login_required
def view_form(request, user_id, pk):
    if request.method == 'GET':
        form = Form.objects.get(id=pk)
        questions = Question.objects.filter(form=form)
        questions = list(questions)
        choices = Choice.objects.filter(question__in=questions)
        context = {
            'form': form,
            'questions': questions,
            'choices': choices
        }
        return render(request, 'survey/view_form.html', context)
    elif request.method == 'POST':
        user = User.objects.get(id=user_id)
        form = Form.objects.get(id=pk)
        form.users.add(user)
        form.save()
        questions = Question.objects.filter(form=form)
        for question in questions:
            if question.question_type == 'mcq_many':
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
        return redirect('survey:form-list')

def list_form(request, pk):
    form = Form.objects.get(id=pk)
    question_len = len(form.question_set.all())
    answers = UserAnswer.objects.filter(form=form)
    users = form.users.all()
    lists = []
    for user in users:
        user_answer = list(answers.filter(user=user).order_by('created'))[-question_len:]
        lists.append({
            'user': user,
            'user_answer': user_answer
        })
    context = {
        'lists': lists,
    }
    return render(request, 'survey/list_form.html', context)

def delete_form(request, pk):
    # delete answer instance?
    form = Form.objects.get(id=pk)
    form.delete()
    return redirect('survey:form-list')
