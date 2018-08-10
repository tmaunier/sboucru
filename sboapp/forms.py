"""
Oxford University Clinical Research Unit
Serum bank manager
MIT License
Copyright (c) 2018 tmaunier
link : https://github.com/tmaunier/sboucru
Written by Tristan Maunier
Bioinformatics Master Degree - University of Bordeaux, France
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import datetime
from datetime import date
from sboapp.models import Elisa, Site, Serum, Freezer, Ward, Elisa, Chik_elisa, Dengue_elisa, Rickettsia_elisa, Pma, Pma_result
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, StrictButton, InlineCheckboxes, InlineRadios, Accordion, AccordionGroup, Field

def get_choices(model,field):
    query=model.objects.values_list(field).distinct()
    choices=[]
    for i in range(query.count()):
        if query[i][0] is not None:
            choices.append((query[i][0],query[i][0],))
    choices.sort()
    if str(field) != "site_id":
        choices.insert(0,(None,'----'))
    return choices

def get_pma_results_fields():
    choices=[('all','all results fields')]
    for f in Pma_result._meta.get_fields():
        if f.name != 'pma':
            choices.append((f.name,f.name,))
    return choices

def get_pma_fields():
    choices=[('all','all fields')]
    fields_exceptions=['pma_result','sample','result_id','import_date','import_time','import_user']
    for f in Pma._meta.get_fields():
        if f.name not in fields_exceptions:
            if f.name == 'processed_day':
                choices.append((f.name,'Day of PMA test (processed_day)',))
            elif f.name == 'processed_month':
                choices.append((f.name,'Month of PMA test (processed_month)',))
            elif f.name == 'processed_year':
                choices.append((f.name,'Year of PMA test (processed_year)',))
            elif f.name == 'scanned_day':
                choices.append((f.name,'Day of PMA scan (scanned_day)',))
            elif f.name == 'scanned_month':
                choices.append((f.name,'Month of PMA scan (scanned_month)',))
            elif f.name == 'scanned_year':
                choices.append((f.name,'Year of PMA scan (scanned_year)',))
            else :
                choices.append((f.name,f.name,))
    return choices

def get_serum_fields():
    choices=[('all','all fields')]
    fields_exceptions=['sample_id','freezer','pma','elisa','site','coll_num','coll_date','ward_id','ward','import_date','import_time','import_user']
    for f in Serum._meta.get_fields():
        if f.name not in fields_exceptions:
            choices.append((f.name,f.name,))
    return choices

def get_freezer_fields():
    choices=[('all','all fields')]
    fields_exceptions=['import_date','import_time','import_user']
    for f in Freezer._meta.get_fields():
        if f.name not in fields_exceptions:
            if f.name == 'subdivision_1_position':
                choices.append((f.name,'Shelf (subdivision_1_position)'))
            elif f.name == 'subdivision_2_position':
                choices.append((f.name,'Rack (subdivision_2_position)'))
            elif f.name == 'subdivision_3_position':
                choices.append((f.name,'Box (subdivision_3_position)'))
            elif f.name == 'subdivision_4_position':
                choices.append((f.name,'Tube (subdivision_4_position)'))
            elif f.name != 'sample':
                choices.append((f.name,f.name,))
    return choices

def get_elisa_fields():
    choices=[('all','all fields')]
    fields_exceptions=['import_date','import_time','import_user']
    for e in Elisa._meta.get_fields():
        if e.name not in fields_exceptions:
            if e.name == 'pathogen':
                choices.append((e.name,'Name of the disease (pathogen)'))
            elif e.name == 'elisa_day':
                choices.append((e.name,'Day of the Elisa test (processed day)'))
            elif e.name == 'elisa_month':
                choices.append((e.name,'Month of the Elisa test (processed month)'))
            elif e.name == 'elisa_year':
                choices.append((e.name,'Year of the Elisa test (processed year)'))
    return choices

def get_pathogen():
    query=Elisa.objects.values_list('pathogen').distinct()
    pathogen_list=[]
    for i in range(query.count()):
        pathogen_list.append((query[i][0],query[i][0],))
    pathogen_list.sort()
    final_pathogen_list = [('all','all pathogens')]
    final_pathogen_list.extend(pathogen_list)
    return final_pathogen_list

def get_years():
    query=Serum.objects.values_list('year').distinct()
    year_list=[]
    for i in range(query.count()):
        year_list.append(query[i][0])
    year_list.sort()
    return year_list

def get_last_three_days():
    datetoday = datetime.date.today()
    dayminusone = datetoday + datetime.timedelta(days=-1)
    dayminustwo = datetoday + datetime.timedelta(days=-2)
    dayminusthree = datetoday + datetime.timedelta(days=-3)
    days_list = [(None,'----'),(datetoday,datetoday),(dayminusone,dayminusone),(dayminustwo,dayminustwo),(dayminusthree,dayminusthree)]
    return days_list

def get_wards():
    ward_list=[]
    query=Ward.objects.values_list('ward_id','ward_name').distinct()
    for i in range(query.count()):
        ward_value='{} - {}'.format(query[i][0],query[i][1])
        ward_list.append((query[i][0], ward_value))
    return ward_list

def sample_validator(value):
    if Serum.objects.filter(sample_id=value).exists() is False:
        raise ValidationError("This sample doesn't exist in the database")
        return value

class UploadFileForm(forms.Form):
    file = forms.FileField()

class YesNoForm(forms.Form):
    answer = forms.ChoiceField(label='',widget=forms.RadioSelect,choices=((0,'Yes'),(1,'No')), initial=1, help_text='Warning ! Are you sure about it ? This action is definitive')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'validate_undo_form'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
        Fieldset(
        'Validate Undo Import',
        'answer',
        ),
        StrictButton(
        '<span class="glyphicon glyphicon-trash" \
        aria-hidden="true"></span> %s' % "Erase",
        type='submit', color='red',
        css_class='btn-danger col-md-offset-10', href='undo_import/delete_import'
        ),)

class UndoForm(forms.Form):
    import_type = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}),label='', choices=((None,'----'),
    ("serum","Serum"),
    ("freezer","Serum's location"),
    ("elisa_chik","Elisa Chikungunya"),
    ("elisa_dengue","Elisa Dengue"),
    ("elisa_rickettsia","Elisa Rickettsia"),
    ("pma","PMA"),
    ), help_text='.')
    import_date = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}),choices=get_last_three_days(),label='', help_text='.')
    import_time = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}),label='', choices=((None,'----'),
    ("0-2","00:00 -> 01:59"),
    ("2-4","02:00 -> 03:59"),
    ("4-6","04:00 -> 05:59"),
    ("6-8","06:00 -> 07:59"),
    ("8-10","08:00 -> 09:59"),
    ("10-12","10:00 -> 11:59"),
    ("12-14","12:00 -> 13:59"),
    ("14-16","14:00 -> 15:59"),
    ("16-18","16:00 -> 17:59"),
    ("18-20","18:00 -> 19:59"),
    ("20-22","20:00 -> 21:59"),
    ("22-24","22:00 -> 23:59")
    ), help_text='.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'undo_form'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
        Fieldset(
        'Import Type',
        'import_type',
        ),
        Fieldset(
        'Import date',
        'import_date',
        ),
        Fieldset(
        'Import Time',
        'import_time',
        ),
        StrictButton(
        '<span class="glyphicon glyphicon-ok" \
        aria-hidden="true"></span> %s' % "Submit",
        type='submit', color='green',
        css_class='btn-success col-md-offset-10'
        ),)


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class PathogenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PathogenForm, self).__init__(*args, **kwargs)
        self.fields['pathogen'] = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))

class FileTypeForm(forms.Form):
    file_type = forms.ChoiceField(widget=forms.Select,required=True,choices=(('csv','csv'),('xls','xls'),('xlsx','xlsx'),))

class DownloadTemplateForm(forms.Form):
    file_type = forms.ChoiceField(widget=forms.Select,required=True,choices=(('csv','csv'),('xls','xls'),('xlsx','xlsx'),))
    template = forms.ChoiceField(label='',widget=forms.RadioSelect,choices=(('import_serum','Import Serum'),
    ('location','Import or Modify Serum\'s location'),
    ('elisa_chik','Import Elisa Chikungunya results'),
    ('elisa_dengue','Import Elisa Dengue results'),
    ('elisa_rickettsia','Import Elisa Rickettsia results'),
    ('pma','Import PMA results'),
    ('status_and_sort','Switch Serum Status or Import list of Sera (Sort_data)'),), help_text='.')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'download_template_form'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
        Fieldset(
        'Files Templates',
        'template',
        ),
        Fieldset(
        'File type',
        'file_type',
        ),
        StrictButton(
        '<span class="glyphicon glyphicon-download-alt" \
        aria-hidden="true"></span> %s' % "Download",
        type='submit', color='blue',
        css_class='btn-primary col-md-offset-10'
        ),)

class SortDataForm(forms.Form):
    sample_id = forms.CharField(label='Sample_id',validators=[validators.MaxLengthValidator(8,message=None)], required=False,widget=forms.TextInput(attrs={
            "class":"form-control",
            'placeholder': 'Ex : AG020015'}))
    status = forms.MultipleChoiceField(required=False, label='Status', widget=forms.CheckboxSelectMultiple, choices=(('Available','Available'),('Unavailable','Unavailable')))
    site_id = forms.MultipleChoiceField(required=False,label='Site_id',widget=forms.CheckboxSelectMultiple,choices=get_choices(Site,'site_id'))
    coll_num = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'coll_num'),label='Collection number', required=False)
    age_min = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect4"}), choices=get_choices(Serum,'age_min'),label='Age min', required=False)
    age_max = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect5"}), choices=get_choices(Serum,'age_max'),label='Age max', required=False, help_text='Note : Age max must be greater than age min !')
    gender = forms.MultipleChoiceField(required=False,label='Gender',widget=forms.CheckboxSelectMultiple,choices=((0,'F'),(1,'M')))
    coll_date = forms.DateField(widget=forms.SelectDateWidget(years=get_years()),label='Date of collection', required=False)
    year = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect6"}), choices=get_choices(Serum,'year'),label='Year of collection', required=False)
    ward_id = forms.MultipleChoiceField(required=False,label='Ward_id',widget=forms.CheckboxSelectMultiple,choices=get_wards(), help_text='.')
    study_code = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect7"}), choices=get_choices(Freezer,'study_code'),label='Study code', required=False)
    sample_type = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect8"}), choices=get_choices(Freezer,'sample_type'),label='Sample type', required=False)
    aliquot_no = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect9"}), choices=get_choices(Freezer,'aliquot_no'),label='AliquotNo', required=False)
    volume = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect10"}), choices=get_choices(Freezer,'volume'),label='Volume', required=False)
    freezer_section_name = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect11"}), choices=get_choices(Freezer,'freezer_section_name'),label='Freezer section name', required=False)
    subdivision_1_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect12"}), choices=get_choices(Freezer, 'subdivision_1_position'), label='Shelf', required=False)
    subdivision_2_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect13"}), choices=get_choices(Freezer, 'subdivision_2_position'), label='Rack', required=False)
    subdivision_3_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect14"}), choices=get_choices(Freezer, 'subdivision_3_position'), label='Box', required=False)
    subdivision_4_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect15"}), choices=get_choices(Freezer, 'subdivision_4_position'), label='Tube', required=False, help_text='.')
    serum_file = forms.FileField(required=False, label='Serum list', help_text='Note : If you don\'t import your serums set, the initial serums set will contain every serums in the database')
    all_test = forms.MultipleChoiceField(required=False,label='All tests',widget=forms.CheckboxSelectMultiple,choices=((0,'Yes'),(1,'No')), help_text='Check YES on all tests fields means that you\'ll select the sera on which ones ALL TESTS have been performed, Check NO means that you\'ll select the sera on which ones NO test has been performed')
    elisa_chik_test = forms.MultipleChoiceField(required=False,label='Elisa Chikungunya',widget=forms.CheckboxSelectMultiple,choices=((0,'Yes'),(1,'No')), help_text='.')
    elisa_dengue_test = forms.MultipleChoiceField(required=False,label='Elisa Dengue',widget=forms.CheckboxSelectMultiple,choices=((0,'Yes'),(1,'No')), help_text='.')
    elisa_rickettsia_test = forms.MultipleChoiceField(required=False,label='Elisa Rickettsia',widget=forms.CheckboxSelectMultiple,choices=((0,'Yes'),(1,'No')), help_text='.')
    pma_test = forms.MultipleChoiceField(required=False,label='PMA',widget=forms.CheckboxSelectMultiple,choices=((0,'Yes'),(1,'No')), help_text='Check YES means that you\'ll select the sera on which ones the test has been performed, Check NO means that you\'ll select the sera on which ones the test has not been performed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'sort-form'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Step 1 - Initial Serums Set',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-11 btnNext',
                    ),
                    Fieldset(
                    'Import list of serums',
                    'serum_file',
                    )
                ),
                Tab(
                    'Step 2 - Serum',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-11 btnNext',
                    ),
                    Fieldset(
                    'Serum fields',
                    'sample_id',
                    'status',
                    'site_id',
                    'coll_num',
                    'age_min',
                    'age_max',
                    'gender',
                    'coll_date',
                    'year',
                    'ward_id',
                    )
                ),
                Tab(
                    'Step 3 - Freezer',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-11 btnNext',
                    ),
                    Fieldset(
                    'Freezer fields',
                    'study_code',
                    'sample_type',
                    'aliquot_no',
                    'volume',
                    'freezer_section_name',
                    'subdivision_1_position',
                    'subdivision_2_position',
                    'subdivision_3_position',
                    'subdivision_4_position',
                    )
                ),
                Tab(
                    'Step 4 - Tests',
                    StrictButton(
                    '<span class="glyphicon glyphicon-arrow-left" \
                    aria-hidden="true"></span> %s' % 'Previous',
                    type='button',
                    css_class='btn-danger btnPrevious',
                    ),
                    StrictButton(
                    '<span class="glyphicon glyphicon-ok" \
                    aria-hidden="true"></span> %s' % "Submit",
                    type='submit', color='green',
                    css_class='btn-success col-md-offset-10'
                    ),
                    Fieldset(
                    'Select Serum based on the tests performed',
                    'all_test',
                    'elisa_chik_test',
                    'elisa_dengue_test',
                    'elisa_rickettsia_test',
                    'pma_test',
                    )
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        sample_id = cleaned_data.get("sample_id")
        age_min = cleaned_data.get("age_min")
        age_max = cleaned_data.get("age_max")
        coll_date = cleaned_data.get("coll_date")
        year = cleaned_data.get("year")

        if sample_id:
            if Serum.objects.filter(sample_id=sample_id).exists() is False:
                sample_error = "Warning ! This sample doesn't exist in the database, please enter a valid sample_id"
                self.add_error('sample_id', sample_error)
        if coll_date and year:
            coll_date_error = "Warning ! Must choose between coll_date and year of collect  "
            self.add_error('coll_date', coll_date_error)

        if age_min and age_max:
            if age_min>age_max:
                msg = "Warning ! Age_min must be lower than Age_max "
                self.add_error('age_min', msg) #link an error to a specific field
                self.add_error('age_max', msg)

        return cleaned_data

class DisplayDataForm(forms.Form):
    serum_fields = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=get_serum_fields(), initial=['all'], required=False, label='', help_text='Note : sample_id, site_id, coll_num, coll_date & ward_id are exported by default ')
    freezer_fields = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=get_freezer_fields(), initial=['all'], required=False, label='', help_text='.')
    elisa_general_fields = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=get_elisa_fields(), initial=['all'], label='', help_text='Note : sample_id & result_id are exported by default ')
    pathogen = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=get_pathogen(), initial=['all'], required=False, label='', help_text='Note: If you want Elisa info you need to check at least one pathogen, if you don\'t you won\'t have any Elisa result in your file')
    pma_general_fields = forms.MultipleChoiceField(label='',widget=forms.CheckboxSelectMultiple,choices=get_pma_fields(), initial=['all'], required=False, help_text='Note : sample_id & result_id are exported by default ')
    pma_results_fields = forms.MultipleChoiceField(required=False, label='',widget=forms.CheckboxSelectMultiple, help_text='.',choices=(('all','all pathogens'),
    ('Chikungunya','Chikungunya (chikv_e1_mutant, chikv_e2)'),
    ('Dengue','Dengue (dv1_ns1, dv2_ns1, dv3_ns1, dv4_ns1)'),
    ('Japanese Encephalisis','Japanese Encephalisis (jev_ns1)'),
    ('Saint-Louis Encephalisis', 'Saint-Louis Encephalisis (slev_ns1)'),
    ('Tick-borne Encephalisis', 'Tick-borne Encephalisis (tbev_ns1)'),
    ('West Nile', 'West Nile (wnv_ns1)'),
    ('Yellow Fever', 'Yellow Fever (yfv_ns1)'),
    ('Zika', 'Zika (zikv_brasil_ns1, zikv_ns1)')), initial=['all'])
    file_type = forms.ChoiceField(widget=forms.Select,required=True, label='',choices=(('csv','csv'),('xls','xls'),('xlsx','xlsx'),))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'sort-form'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Step 1 - Serum',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-10 btnNext',
                    ),
                    Fieldset(
                    'Serum Fields',
                    'serum_fields',
                    )
                ),
                Tab(
                    'Step 2 - Freezer',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Previous',
                        type='button',
                        css_class='btn-danger btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-10 btnNext',
                    ),
                    Fieldset(
                    'Freezer Fields',
                    'freezer_fields',
                    )
                ),
                Tab(
                    'Step 3 - Results',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Previous',
                        type='button',
                        css_class='btn-danger btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-10 btnNext',
                    ),
                    Fieldset(
                    'Elisa',
                    Fieldset(
                    'General',
                    'elisa_general_fields',
                    ),
                    Fieldset(
                    'Pathogens',
                    'pathogen',
                    ),
                    ),
                    Fieldset(
                    'Protein MicroArray',
                    Fieldset(
                    'General',
                    'pma_general_fields',
                    ),
                    Fieldset(
                    'Pathogens',
                    'pma_results_fields',
                    ),
                    ),
                ),
                Tab(
                    'Step 4 - Export',
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Previous',
                        type='button',
                        css_class='btn-danger btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Export Data",
                        type='submit',
                        css_class='btn-success col-md-offset-11'
                    ),
                    Fieldset(
                    'Select a type of file',
                    'file_type',
                    )
                ),
            ),
        )
