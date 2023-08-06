from django import forms
from .models import Comment
from django.conf import settings

User = settings.AUTH_USER_MODEL
# from django.contrib.auth.models import User


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


#         fields = ['field1', 'field2', 'field3']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if user:
#             self.initial['field1'] = user.username
