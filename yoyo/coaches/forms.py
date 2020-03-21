from django import forms
from .models import Coach


class CoachAdminForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CoachAdminForm, self).__init__(*args, **kwargs)

        self.fields['born'].required = True
        self.fields['city'].required = True
