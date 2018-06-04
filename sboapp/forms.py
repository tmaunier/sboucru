from django import forms
from sboapp.models import Elisa

def get_choices():
    # you place some logic here
    query=Elisa.objects.values_list('pathogen').distinct()
    count=query.count()
    choices=[]
    for i in range(count):
        choices.append((i,query[i]))
    return choices

class NameForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    user_name = forms.CharField(label='User name', max_length=100,error_messages={'required': 'Please enter your name'})
    # user_password = forms.PasswordInput()

class PathogenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PathogenForm, self).__init__(*args, **kwargs)
        self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,
            choices=get_choices()
        )
    error_css_class = 'error'
    required_css_class = 'required'
    pathogen = forms.ChoiceField(widget=forms.Select)
    # CHOICES = (('1', 'First',), ('2', 'Second',))
    # pathogen = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

    # def set_pathogen(self):
    #     # return pathogen value using the self.cleaned_data dictionary
    #     pass
