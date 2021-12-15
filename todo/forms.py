from django.db.models import fields
from django.forms import ModelForm
from .models import tasktodo

class TodoForm(ModelForm):
    class Meta:
        model = tasktodo
        fields = [
            'title', 'memo', 'important',
        ]