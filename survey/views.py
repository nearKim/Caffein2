'''
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'survey/index.html'
    context_object_name = 'latest_question_list'
    #context_object_name = 'question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'survey/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'survey/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'survey/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('survey:results', args=(question.id,)))
'''

#from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
#from django.contrib.auth.models import User
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import json

from .models import Form, Question, Choice, UserAnswer
#from .serializers import UserSerializer, FormSerializer, QuestionSerializer


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
        print(dict_post_data)
        if len(dict_post_data['questions']) > 0:
            form = Form.objects.create(title=dict_post_data['form_title'],
                                       description=dict_post_data['form_description'],
                                       owner=self.request.user)
            print(form)
            result['result'] = 'Form saved successfully'
            for question_item in dict_post_data['questions']:
                question = Question(question_text=question_item['text'],
                                    question_type=question_item['type'],
                                    form=form)
                print(question)
                question.save()
                if question_item['type'] == 'mcq_one' or question_item['type'] == 'mcq_many':
                    for choice_item in question_item['options']:
                        choice = Choice(choice_text=choice_item,
                                        question=question)
                        choice.save()
        else:
            result['result'] = 'Add a question title'
        return HttpResponse(json.dumps(result))

#@login_required
def view_form(request, user_id, pk):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        print(request.method)
        print(user)
        print(Form.objects.get(pk=pk))
        form = Form.objects.get(id=pk)
        questions = Question.objects.filter(form=form)
        questions = list(questions)
        #questions.reverse()
        choices = Choice.objects.filter(question__in=questions)
        context = {
            'form': form,
            'questions': questions,
            'choices': choices
        }
        return render(request, 'survey/view_form.html', context)
    elif request.method == 'POST':
        print(request.POST)
        user = User.objects.get(id=user_id)
        print(user)
        form = Form.objects.get(id=pk)
        form.users.add(user)
        form.save()
        questions = Question.objects.filter(form=form)
        for question in questions:
            if question.question_type == 'mcq_many':
                all_answer = request.POST.getlist(question.question_text)
                answer = ''
                print(question.question_text)
                print(all_answer)
                for text in all_answer:
                    answer += text + ','
                answer = answer[:-1]
            else:
                answer = request.POST.get(question.question_text)
            UserAnswer.objects.create(question=question,
                                      answer=answer,
                                      form=form,
                                      user=user)
        print(UserAnswer.objects.filter(form=form))
        print(form.users.all())

        #return render(request, 'survey/home.html')
        return redirect('survey:form-list')

def list_form(request, pk):
    #user = User.objects.get(id=user_id)
    form = Form.objects.get(id=pk)
    question_len = len(form.question_set.all())
    answers = UserAnswer.objects.filter(form=form)
    users = form.users.all()
    print(users)
    #questions = Question.objects.filter(form=form)
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
    print(request.method)
    print(Form.objects.get(pk=pk))
    form = Form.objects.get(id=pk)
    form.delete()
    return redirect('survey:form-list')
'''
# unused in app
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    '''
