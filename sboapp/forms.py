from django import forms
from sboapp.models import Elisa, Site, Serum, Freezer, Ward

# def get_pathogen_choices():
#     query=Elisa.objects.values_list('pathogen').distinct()
#     count=query.count()
#     choices=[]
#     for i in range(count):
#         choices.append((query[i][0],query[i][0],))
#     return choices
# def get_site_choices():
#     query=Site.objects.values_list('site_id').distinct()
#     choices=[]
#     for i in range(query.count()):
#         choices.append((query[i][0],query[i][0],))
#     return choices

def get_choices(model,field):
    query=model.objects.values_list(field).distinct()
    choices=[]
    for i in range(query.count()):
        if query[i][0] is not None:
            choices.append((query[i][0],query[i][0],))
    choices.sort()
    return choices

def get_years():
    query=Serum.objects.values_list('year').distinct()
    year_list=[]
    for i in range(query.count()):
        year_list.append(query[i][0])
    year_list.sort()
    return year_list

def get_wards():
    ward_list=[]
    query=Ward.objects.values_list('ward_id','ward_name').distinct()
    for i in range(query.count()):
        ward_value='{} - {}'.format(query[i][0],query[i][1])
        ward_list.append((query[i][0], ward_value))
    return ward_list

class NameForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    user_name = forms.CharField(label='User name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    user_id = forms.CharField(label='User id',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Userid'})) #a remplacer par le vrai password
    # user_password = forms.PasswordInput()

class PathogenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PathogenForm, self).__init__(*args, **kwargs)
        self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))

class ExportFormatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExportFormatForm, self).__init__(*args,**kwargs)
        self.fields['format'] = forms.ChoiceField(widget=forms.Select,choices=((1,'xls'),(2,'xlsx'),(3,'ods'),(4,'csv'),))

class SortDataForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(SortDataForm, self).__init__(*args, **kwargs)
    #     self.fields['sample_id'] = forms.CharField(label='Sample_id', min_length=8, required=False, widget=forms.TextInput(attrs={
    #             # 'style': 'border-color: blue;',
    #             "class":"form-control",
    #             "size" : "100",
    #             'placeholder': 'Ex : AG020015'}))
    #     self.fields['site_id'] = forms.MultipleChoiceField(required=False,label='Site_id',widget=forms.CheckboxSelectMultiple,choices=get_choices(Site,'site_id'))
    #     self.fields['coll_num'] = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'coll_num'),label='Collection number', required=False)
    #     self.fields['birth_year'] = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'birth_year'),label='Birth year', required=False)
    #     self.fields['age'] = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age'),label='Exact age', required=False)
    #     self.fields['age_min'] = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age_min'),label='Age min', required=False)
    #     self.fields['age_max'] = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age_max'),label='Age max', required=False, help_text='Note : Age max must be higher than age min !')
    #     self.fields['gender'] = forms.MultipleChoiceField(required=False,label='Gender',widget=forms.CheckboxSelectMultiple,choices=((1,'F'),(2,'M')))
    #     self.fields['coll_date'] = forms.DateField(widget=forms.SelectDateWidget(years=get_years()),label='Date of collection', required=False)
    #     self.fields['year'] = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'year'),label='Year of collection', required=False)
    #     self.fields['ward_id'] = forms.MultipleChoiceField(required=False,label='Ward_id',widget=forms.CheckboxSelectMultiple,choices=get_wards())
    sample_id = forms.CharField(label='Sample_id', min_length=8, required=False, widget=forms.TextInput(attrs={
            # 'style': 'border-color: blue;',
            "class":"form-control",
            "size" : "10",
            'placeholder': 'Ex : AG020015'}))
    site_id = forms.MultipleChoiceField(required=False,label='Site_id',widget=forms.CheckboxSelectMultiple,choices=get_choices(Site,'site_id'))
    coll_num = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'coll_num'),label='Collection number', required=False)
    birth_year = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'birth_year'),label='Birth year', required=False)
    age = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age'),label='Exact age', required=False)
    age_min = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age_min'),label='Age min', required=False)
    age_max = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age_max'),label='Age max', required=False, help_text='Note : Age max must be higher than age min !')
    gender = forms.MultipleChoiceField(required=False,label='Gender',widget=forms.CheckboxSelectMultiple,choices=((1,'F'),(2,'M')))
    coll_date = forms.DateField(widget=forms.SelectDateWidget(years=get_years()),label='Date of collection', required=False)
    year = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'year'),label='Year of collection', required=False)
    ward_id = forms.MultipleChoiceField(required=False,label='Ward_id',widget=forms.CheckboxSelectMultiple,choices=get_wards())


class DisplayDataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DisplayDataForm, self).__init__(*args, **kwargs)
        self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
        self.fields['pa'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
        self.fields['pat'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
        self.fields['patho'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
        self.fields['pathoge'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
# chaque champ de serum et freezer independant
# tout de serum et freezer (un bouton pour chaque)
# les noms complets pour les sites et ward (un bouton pour chaque)
# resultats par test ou par pathogen (fichier resultats independant ?)
# boolean -> use Form.has_changed() --> set initial value to False (True for sample_id, site, year of collect)
