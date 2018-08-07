from django.db import models
from core.mixins import TimeStampedMixin
from django.conf import settings


class Form(TimeStampedMixin):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default='1', on_delete=models.CASCADE, related_name='owner')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users')
    opened = models.BooleanField(default=True)
    for_new = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def is_new(self):
        return self.for_new

    def __str__(self):
        return self.title


class Question(TimeStampedMixin):
    question_text = models.CharField(max_length=200)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    QUESTION_TYPE_CHOICES = (
        ('text', '텍스트 응답'),
        ('choice_one', '1개 선택 응답'),
        ('choice_many', '다수 선택 응답'),
        ('binary', '예 / 아니오 응답')
    )
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES, default='text')

    def __str__(self):
        return self.question_text


class Choice(TimeStampedMixin):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class Answer(TimeStampedMixin):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserAnswer(Answer):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    answer = models.TextField(max_length=1000)

    def __str__(self):
        return self.answer


class TextAnswer(Answer):
    answer_text = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.id)


class ChoiceOneAnswer(Answer):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice.choice_text


class ChoiceManyAnswer(Answer):
    choices = models.ManyToManyField(Choice)

    def get_choices(self):
        return ",".join([str(choice) for choice in self.choices.all()])

    def __str__(self):
        return str(self.id)


class BinaryAnswer(Answer):
    ANSWER_OPTIONS = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    answer_option = models.CharField(max_length=3, choices=ANSWER_OPTIONS)

    def __str__(self):
        return self.answer_option
