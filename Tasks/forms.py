from django import forms
from .models import *


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'created_date',
            'due_date',
            'created_by',
            'assigned_to_user',
            'assigned_to_group',
            'message',
            'priority'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type':'date'}),
            'created_date' : forms.DateInput(attrs={'type':'date'})
        }


class TaskDoneForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'completed'
        ]        
       


class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields  = [
            'deleted'
        ]


class TaskTransferForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_to_user']
