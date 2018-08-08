'''
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
'''
from django.contrib import admin

from .models import Form, Question, Choice, TextAnswer, ChoiceOneAnswer, \
    ChoiceManyAnswer, BinaryAnswer


class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'form')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_text', 'question')


class TextAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'user')


class McqOneAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice', 'question', 'user')


class McqManyAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_choices', 'question', 'user')


class BinaryAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_option', 'question', 'user')


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(TextAnswer, TextAnswerAdmin)
admin.site.register(ChoiceOneAnswer, McqOneAnswerAdmin)
admin.site.register(ChoiceManyAnswer, McqManyAnswerAdmin)
admin.site.register(BinaryAnswer, BinaryAnswerAdmin)
