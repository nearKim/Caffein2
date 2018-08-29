from django.forms import ModelForm, Textarea

from comments.models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['rows'] = 3
        self.fields['content'].label = ''