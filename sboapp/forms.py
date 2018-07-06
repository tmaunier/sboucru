from django import forms
from sboapp.models import Elisa, Site, Serum, Freezer, Ward
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import TabHolder, Tab, StrictButton, InlineCheckboxes, InlineRadios

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
    # sample_id = forms.CharField(label='Sample_id', min_length=8, required=False)
    # site_id = forms.MultipleChoiceField(required=False,label='Site_id',choices=get_choices(Site,'site_id'))
    # coll_num = forms.ChoiceField(choices=get_choices(Serum,'coll_num'),label='Collection number', required=False)
    # birth_year = forms.ChoiceField(choices=get_choices(Serum,'birth_year'),label='Birth year', required=False)
    # age = forms.ChoiceField(choices=get_choices(Serum,'age'),label='Exact age', required=False)
    # age_min = forms.ChoiceField(choices=get_choices(Serum,'age_min'),label='Age min', required=False)
    # age_max = forms.ChoiceField(choices=get_choices(Serum,'age_max'),label='Age max', required=False, help_text='Note : Age max must be greater than age min !')
    # gender = forms.MultipleChoiceField(required=False,label='Gender',choices=((1,'F'),(2,'M')))
    # coll_date = forms.DateField(widget=forms.SelectDateWidget(years=get_years()),label='Date of collection', required=False)
    # year = forms.ChoiceField(choices=get_choices(Serum,'year'),label='Year of collection', required=False)
    # ward_id = forms.MultipleChoiceField(required=False,label='Ward_id',choices=get_wards())
    # freezer_section_name = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer,'freezer_section_name'),label='Freezer section name', required=False)
    # subdivision_1_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_1_position'), label='Shelf', required=False)
    # subdivision_2_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_2_position'), label='Rack', required=False)
    # subdivision_3_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_3_position'), label='Box', required=False)
    # subdivision_4_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_4_position'), label='Tube', required=False)
    sample_id = forms.CharField(label='Sample_id', min_length=8, required=False,widget=forms.TextInput(attrs={
            # 'style': 'border-color: blue;',
            "class":"form-control",
            # "size" : "10",
            'placeholder': 'Ex : AG020015'}))
    site_id = forms.MultipleChoiceField(required=False,label='Site_id',widget=forms.CheckboxSelectMultiple,choices=get_choices(Site,'site_id'))
    coll_num = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'coll_num'),label='Collection number', required=False)
    birth_year = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}),choices=get_choices(Serum,'birth_year'),label='Birth year', required=False)
    age = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'age'),label='Exact age', required=False)
    age_min = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'age_min'),label='Age min', required=False)
    age_max = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'age_max'),label='Age max', required=False, help_text='Note : Age max must be greater than age min !')
    gender = forms.MultipleChoiceField(required=False,label='Gender',widget=forms.CheckboxSelectMultiple,choices=((1,'F'),(2,'M')))
    coll_date = forms.DateField(widget=forms.SelectDateWidget(years=get_years()),label='Date of collection', required=False)
    year = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Serum,'year'),label='Year of collection', required=False)
    ward_id = forms.MultipleChoiceField(required=False,label='Ward_id',widget=forms.CheckboxSelectMultiple,choices=get_wards())
    study_code = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer,'study_code'),label='Study code', required=False)
    sample_type = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer,'sample_type'),label='Sample type', required=False)
    aliquot_no = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer,'aliquot_no'),label='AliquotNo', required=False)
    volume = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer,'volume'),label='Volume', required=False)
    freezer_section_name = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer,'freezer_section_name'),label='Freezer section name', required=False)
    subdivision_1_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_1_position'), label='Shelf', required=False)
    subdivision_2_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_2_position'), label='Rack', required=False)
    subdivision_3_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_3_position'), label='Box', required=False)
    subdivision_4_position = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "id":"exampleFormControlSelect1"}), choices=get_choices(Freezer, 'subdivision_4_position'), label='Tube', required=False)

    def __init__(self, *args, **kwargs):
        """
        Surcharge de l'initialisation du formulaire
        """
        super().__init__(*args, **kwargs)
        # Tu utilises FormHelper pour customiser ton formulaire
        self.helper = FormHelper()
        # Tu définis l'id et la classe bootstrap de ton formulaire
        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'sort-form'
        # Tu définis la taille des labels et des champs sur la grille
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        # Tu crées l'affichage de ton formulaire
        self.helper.layout = Layout(
            # Le formulaire va contenir 3 onglets
            TabHolder(
                # Premier onglet
                Tab(
                    # Label de l'onglet
                    'Step 1 - Serum',
                    # Liste des champs du modèle à afficher dans l'onglet
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-11 btnNext',
                    ),
                    'sample_id',
                    # InlineCheckboxes('site_id'),
                    'site_id',
                    'coll_num',
                    'birth_year',
                    'age',
                    'age_min',
                    'age_max',
                    'gender',
                    'coll_date',
                    'year',
                    'ward_id',
                    # Tu rajoutes un bouton "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-right" \
                        aria-hidden="true"></span> %s' % "Next",
                        type='button',
                        css_class='btn-warning col-md-offset-11 btnNext',
                    )

                ),
                # Deuxième onglet
                Tab(
                    # Label de l'onglet
                    'Step 2 - Freezer',
                    # Liste des champs à afficher
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
                    # css_class='btn-default col-md-offset-8'
                    ),
                    'study_code',
                    'sample_type',
                    'aliquot_no',
                    'volume',
                    'freezer_section_name',
                    'subdivision_1_position',
                    'subdivision_2_position',
                    'subdivision_3_position',
                    'subdivision_4_position',
                    # Tu rajoutes des boutons "Précédent" et "Suivant"
                    StrictButton(
                        '<span class="glyphicon glyphicon-arrow-left" \
                        aria-hidden="true"></span> %s' % 'Previous',
                        type='button',
                        css_class='btn-danger btnPrevious',
                    ),
                    StrictButton(
                        '<span class="glyphicon glyphicon-ok" \
                        aria-hidden="true"></span> %s' % "Submit",
                        type='submit',
                        css_class='btn-success col-md-offset-10'
                    )
                ),
            ),
        )

class DisplayDataForm(forms.Form):
    pathogen = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
    pa = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
    pat = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
    # age_max = forms.ChoiceField(widget=forms.Select, choices=get_choices(Serum,'age_max'),label='Age max', required=False, help_text='Note : Age max must be higher than age min !')
    # gender = forms.MultipleChoiceField(required=False,label='Gender',widget=forms.CheckboxSelectMultiple,choices=((1,'F'),(2,'M')))
    # coll_date = forms.DateField(widget=forms.SelectDateWidget(years=get_years()),label='Date of collection', required=False)
    patho = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
    pathoge = forms.ChoiceField(widget=forms.Select,choices=get_choices(Elisa,'pathogen'))
    file_type = forms.ChoiceField(widget=forms.Select,choices=((1,'xls'),(2,'xlsx'),(3,'ods'),(4,'csv'),))
    # def __init__(self, *args, **kwargs):
    #     """
    #     Surcharge de l'initialisation du formulaire
    #     """
    #     super().__init__(*args, **kwargs)
    #     # Tu utilises FormHelper pour customiser ton formulaire
    #     self.helper = FormHelper()
    #     # Tu définis l'id et la classe bootstrap de ton formulaire
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.form_id = 'sort-form'
    #     # Tu définis la taille des labels et des champs sur la grille
    #     self.helper.label_class = 'col-md-2'
    #     self.helper.field_class = 'col-md-8'
    #     # Tu crées l'affichage de ton formulaire
    #     self.helper.layout = Layout(
    #         # Le formulaire va contenir 3 onglets
    #         TabHolder(
    #             # Premier onglet
    #             Tab(
    #                 # Label de l'onglet
    #                 'Step 1 - Serum',
    #                 # Liste des champs du modèle à afficher dans l'onglet
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-right" \
    #                     aria-hidden="true"></span> %s' % "Next",
    #                     type='button',
    #                     css_class='btn-default col-md-offset-9 btnNext',
    #                 ),
    #                 'pathogen',
    #                 'pa',
    #                 'pat',
    #                 # Tu rajoutes un bouton "Suivant"
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-right" \
    #                     aria-hidden="true"></span> %s' % "Next",
    #                     type='button',
    #                     css_class='btn-default col-md-offset-9 btnNext',
    #                 )
    #
    #             ),
    #             Tab(
    #                 # Label de l'onglet
    #                 'Step 2 - Freezer',
    #                 # Liste des champs du modèle à afficher dans l'onglet
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-left" \
    #                     aria-hidden="true"></span> %s' % 'Previous',
    #                     type='button',
    #                     css_class='btn-default btnPrevious',
    #                 ),
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-right" \
    #                     aria-hidden="true"></span> %s' % "Next",
    #                     type='button',
    #                     css_class='btn-default col-md-offset-9 btnNext',
    #                 ),
    #                 'pathogen',
    #                 'pa',
    #                 'pat',
    #                 # 'age_max',
    #                 # 'gender',
    #                 # 'coll_date',
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-left" \
    #                     aria-hidden="true"></span> %s' % 'Previous',
    #                     type='button',
    #                     css_class='btn-default btnPrevious',
    #                 ),
    #                 # Tu rajoutes un bouton "Suivant"
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-right" \
    #                     aria-hidden="true"></span> %s' % "Next",
    #                     type='button',
    #                     css_class='btn-default col-md-offset-9 btnNext',
    #                 )
    #
    #             ),
    #             Tab(
    #                 # Label de l'onglet
    #                 'Step 3 - Results',
    #                 # Liste des champs du modèle à afficher dans l'onglet
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-left" \
    #                     aria-hidden="true"></span> %s' % 'Previous',
    #                     type='button',
    #                     css_class='btn-default btnPrevious',
    #                 ),
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-right" \
    #                     aria-hidden="true"></span> %s' % "Next",
    #                     type='button',
    #                     css_class='btn-default col-md-offset-9 btnNext',
    #                 ),
    #                 'patho',
    #                 'pathoge',
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-left" \
    #                     aria-hidden="true"></span> %s' % 'Previous',
    #                     type='button',
    #                     css_class='btn-default btnPrevious',
    #                 ),
    #                 # Tu rajoutes un bouton "Suivant"
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-right" \
    #                     aria-hidden="true"></span> %s' % "Next",
    #                     type='button',
    #                     css_class='btn-default col-md-offset-9 btnNext',
    #                 )
    #
    #             ),
    #             # Deuxième onglet
    #             Tab(
    #                 # Label de l'onglet
    #                 'Step 4 - Export',
    #                 # Liste des champs à afficher
    #                 StrictButton(
    #                 '<span class="glyphicon glyphicon-arrow-left" \
    #                 aria-hidden="true"></span> %s' % 'Previous',
    #                 type='button',
    #                 css_class='btn-default btnPrevious',
    #                 ),
    #                 StrictButton(
    #                 '<span class="glyphicon glyphicon-ok" \
    #                 aria-hidden="true"></span> %s' % "Submit",
    #                 type='submit',
    #                 css_class='btn-default col-md-offset-8'
    #                 ),
    #                 'file_type',
    #                 # Tu rajoutes des boutons "Précédent" et "Suivant"
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-arrow-left" \
    #                     aria-hidden="true"></span> %s' % 'Previous',
    #                     type='button',
    #                     css_class='btn-default btnPrevious',
    #                 ),
    #                 StrictButton(
    #                     '<span class="glyphicon glyphicon-ok" \
    #                     aria-hidden="true"></span> %s' % "Export Data",
    #                     type='submit',
    #                     css_class='btn-default col-md-offset-8'
    #                 )
    #             ),
    #         ),
    #     )
# chaque champ de serum et freezer independant
# tout de serum et freezer (un bouton pour chaque)
# les noms complets pour les sites et ward (un bouton pour chaque)
# resultats par test ou par pathogen (fichier resultats independant ?)
# boolean -> use Form.has_changed() --> set initial value to False (True for sample_id, site, year of collect)
