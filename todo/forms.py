from django.forms import ModelForm
from .models import Todo

class create_todoform(ModelForm):
    """Form definition for MODELNAME."""

    class Meta:
        """Meta definition for MODELNAMEform."""

        model = Todo
        fields = ('title', 'memo', 'important')
