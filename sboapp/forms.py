from django import forms
from sboapp.models import Elisa

def get_pathogen_choices():
    query=Elisa.objects.values_list('pathogen').distinct()
    count=query.count()
    choices=[]
    for i in range(count):
        choices.append((query[i][0],query[i][0],))
    return choices

class NameForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    user_name = forms.CharField(label='User name', max_length=100,error_messages={'required': 'Please enter your name'})
    # user_password = forms.PasswordInput()

class PathogenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PathogenForm, self).__init__(*args, **kwargs)
        self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,choices=get_pathogen_choices())

class SortDataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SortDataForm, self).__init__(*args, **kwargs)
        # self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,choices=get_pathogen_choices())

class DisplayDataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DisplayDataForm, self).__init__(*args, **kwargs)
        # self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,choices=get_pathogen_choices())
# chaque champ de serum et freezer independent
# tout de serum et freezer (un bouton pour chaque)
# les noms complets pour les sites et ward (un bouton pour chaque)
# resultats de elisa pma pour chaque serum (chaque champ ou pas ?)
