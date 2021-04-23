from django.forms import *
from .models import *


class TechnicianForm(ModelForm):
    class Meta:
        model = Technician
        exclude = ['deleted']
        widgets = {
            'added_by': HiddenInput(),
        }


class TechnicianDeleteForm(ModelForm):
    class Meta:
        model = Technician
        fields = ['deleted']
