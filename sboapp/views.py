from django.shortcuts import get_object_or_404, render, redirect #render is mainly used with templates while HttpResponse is used for data (for example)
from django.http import HttpResponse, HttpResponseBadRequest
from sboapp.models import Serum, Site, Ward, Freezer, Elisa
from django import forms
from .forms import NameForm, PathogenForm
from django.views.generic.edit import FormView
from django.db.models import Count
import openpyxl
import pyexcel #module to read Excel files in Django
import django_excel as excel
from IPython.display import IFrame
import re #Regular expression python module
import random



# ERRORS 404 & 500

def error_404_view(request, exception):
    return render(request,'sboapp/pages/error_404.html')

#def error_500_view(request, exception):
#    return render(request,'sboapp/pages/error_500.html')

# DATA
def get_data(request):
    dataserum = Serum.objects.all()
    datasite = Site.objects.all()
    dataward = Ward.objects.all()
    datafreezer = Freezer.objects.all()
    dataelisa = Elisa.objects.all()
    args = {"serum_nb": dataserum,"site_nb": datasite,"ward_nb": dataward,"freezer_nb": datafreezer, "elisa_nb": dataelisa}
    return args

def count_data(request):
    counts = []
    count_serum = count_element(Serum)
    count_site = count_element(Site)
    count_ward = count_element(Ward)
    counts = {"count_serum":count_serum,"count_site":count_site,"count_ward":count_ward}
    return counts

def count_element(Model):
    count = Model.objects.all().count()
    return count

# STAFF DASHBOARD
def staff(request):
    args = get_data(request)
    counts = count_data(request)
    return render (request, "sboapp/pages/staff.html", args, counts)

def get_name(request): #display the user's name in the navbar (NOT DONE)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user_name = {"user_name":user_name}
            return render(request,'sboapp/pages/staff.html',user_name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'sboapp/pages/staff.html', {'form': form})


#---IMPORT DATA FROM FILE TO DATABASE
def sample_id_exists(sample_test_id): #Check if the serum_id exists in the Serum table, return Boolean
    exist_count = Serum.objects.filter(sample_id = sample_test_id).count()
    if exist_count >=1:
        return True
    else:
        return False

def ward_id_exists(ward_test_id): #Check if the ward_id exists in the Ward table, return Boolean
    exist_count = Ward.objects.filter(ward_id = int(ward_test_id)).count()
    if exist_count == 1:
        return True
    else:
        return False

def site_id_exists(site_test_id): #Check if the site_id exists in the Site table, return Boolean
    exist_count = Site.objects.filter(site_id= site_test_id).count()
    if exist_count == 1:
        return True
    else:
        return False

def sample_id_exists_in_freezer(sample_test_id): #Check if the sample_id exists in the Freezer table, return Boolean
    exist_count = Freezer.objects.filter(sample= sample_test_id).count()
    if exist_count == 1:
        return True
    else:
        return False

def index_finder(headers_list, header_test_list):
    for i in range(len(headers_list)):
        for j in range(len(header_test_list)):
            if re.match(header_test_list[j], headers_list[i], re.IGNORECASE) is not None:
                return i
    # print ('Index finder failed, no match for this header : ', header_test_list)
    return None

def regex_serum(input_list, output_list, match_index):
    if match_index is None:
        output_list.append("")
    else:
        for i in range(len(input_list)):
            if i == match_index:
                output_list.append(input_list[i])


def site_instance_converter(input_list,output_list,site_id_index):
    for i in range(len(input_list)):
        if i == site_id_index:
            s = Site.objects.get(site_id=input_list[i])
            output_list.append(s)

def ward_instance_converter(input_list,output_list,ward_id_index):
    for i in range(len(input_list)):
        if i == ward_id_index:
            w = Ward.objects.get(ward_id=input_list[i])
            output_list.append(w)

def serum_instance_converter(input_list,output_list,sample_id_index):
    for i in range(len(input_list)):
        if i == sample_id_index:
            s = Serum.objects.get(sample_id=input_list[i])
            output_list.append(s)

def import_serum(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_exist_list = []
            no_match_site = []
            no_match_ward = []
            db_list = [['local_sample_id','site','coll_num','sample_id','birth_year','age','age_min','age_max','gender_1ismale_value','coll_date','day_value','month_value','year','ward']]
            sample_id_index = index_finder(sheet_array[0], [r'sample_id'])
            site_id_index = index_finder(sheet_array[0], [r'site_id'])
            ward_id_index = index_finder(sheet_array[0], [r'ward_id'])
            if sample_id_index is not None and site_id_index is not None and ward_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == True:
                        sample_exist_list.append(sheet_array[j][sample_id_index])
                        # print ('sample exists already')
                    elif site_id_exists(sheet_array[j][site_id_index]) == False:
                        # print ('site_id doesn\'t exist')
                        tmp = []
                        tmp.append('Sample_id : '+sheet_array[j][sample_id_index])
                        tmp.append('Site_id : '+sheet_array[j][site_id_index])
                        no_match_site.append(tmp)
                    elif ward_id_exists(sheet_array[j][ward_id_index]) == False:
                        # print('ward_id doesn\'t exist')
                        tmp = []
                        tmp.append('Sample_id : '+sheet_array[j][sample_id_index])
                        tmp.append('Ward_id : '+str(sheet_array[j][ward_id_index]))
                        no_match_ward.append(tmp)
                    else:
                        tmp=[]
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'local_sample_id']))
                        site_instance_converter(sheet_array[j],tmp,site_id_index) #Need to convert in Site instance
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'coll_num']))
                        regex_serum(sheet_array[j],tmp,sample_id_index)
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'birth year']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'original age',r'age_original']))#special regex
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'age_min']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'age_max']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'gender_1ismale_value']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'coll_date']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'day_value']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'month_value']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'year',r'year_value']))#special regex
                        ward_instance_converter(sheet_array[j],tmp,ward_id_index) #Need to convert in Ward instance
                        db_list.append(tmp)
                #save list to database
                pyexcel.save_as(array=db_list,name_columns_by_row=0, dest_model=Serum, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for sample_id, site_id or ward_id \n These data can\'t be imported'

            if len(sample_exist_list) != 0 or len(no_match_site) !=0 or len(no_match_ward) !=0:
                headings_error=''
                sample_exist_warning = 'Warning ! These following samples already exist in the serum bank, they were not imported : \n'
                site_exist_warning = 'Warning ! The site_id of these samples doesn\'t match with any of those existing in the database, they were not imported : \n'
                ward_exist_warning = 'Warning ! The ward_id of these samples doesn\'t match with any of those existing in the database, they were not imported : \n'
                args = {'form': form, 'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array,'sheet':sheet, 'db_list': db_list, 'sample_exist':sample_exist_list, 'sample_exist_warning':sample_exist_warning, 'site_exist':no_match_site, 'site_exist_warning':site_exist_warning, 'ward_exist':no_match_ward, 'ward_exist_warning':ward_exist_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array, 'db_list': db_list}
            return render (request, "sboapp/pages/import_serum.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/import_serum.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render(request,'sboapp/pages/import_serum.html', {'form': form })


def import_location(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_doesnt_exist_list = []
            sample_exist_in_freezer_list = []
            db_list = [['study_code','sample','sample_type','aliquot_no','volume','freezer_section_name','subdivision_1_position','subdivision_2_position','subdivision_3_position','subdivision_4_position']]
            sample_id_index = index_finder(sheet_array[0], [r'ParticipantNo'])
            if sample_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_list.append(sheet_array[j][sample_id_index])
                        # print ('sample exists already')
                    elif sample_id_exists_in_freezer(sheet_array[j][sample_id_index]) == True:
                        sample_exist_in_freezer_list.append(sheet_array[j][sample_id_index])
                    else:
                        tmp=[]
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'StudyCode']))
                        # regex_serum(sheet_array[j],tmp,sample_id_index)
                        serum_instance_converter(sheet_array[j],tmp,sample_id_index) #Need to convert in Serum instance
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'SampleType']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'AliquotNo']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'Volume']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'freezer section name']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_1_position']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_2_position']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_3_position']))
                        regex_serum(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_4_position']))
                        db_list.append(tmp)

                #save list to database
                pyexcel.save_as(array=db_list,name_columns_by_row=0, dest_model=Freezer, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for sample_id, site_id or ward_id \n These data can\'t be imported'

            if len(sample_doesnt_exist_list) != 0 or len(sample_exist_in_freezer_list) != 0:
                headings_error=''
                sample_doesnt_exist_warning = 'Warning ! These following samples don\'t exist in the serum bank, you can\'t add their location before to add them in the serum bank: \n'
                sample_exist_in_freezer_warning = 'Warning ! These following samples already have a location, please use serum location modification function: \n'
                args = {'form': form, 'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array,'sheet':sheet, 'db_list': db_list, 'sample_doesnt_exist':sample_doesnt_exist_list, 'sample_doesnt_exist_warning':sample_doesnt_exist_warning, 'sample_exist_in_freezer_list':sample_exist_in_freezer_list, 'sample_exist_in_freezer_warning':sample_exist_in_freezer_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array, 'db_list': db_list}
            return render (request, "sboapp/pages/import_location.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/import_location.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render(request,'sboapp/pages/import_location.html', {'form': form })

# class ElisaPathogen(FormView):
#     template_name = 'import_elisa_choices.html'
#     form_class = PathogenForm
#     success_url = 'sboapp/staff/import_elisa/choices/'
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.set_pathogen()
#         return super().form_valid(form)

# def get_elisa_pathogens(request):
#     args = get_data(request)
#     pathogens = Elisa.objects.values('pathogen').distinct()
#     args["pathogens"]= pathogens
#     return render (request, "sboapp/pages/import_elisa_choices.html", args)

def init_elisa(request):
    ER1 = Elisa.objects.create(result_id='ElisaChik_1', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020001'), elisa_day='25', elisa_month='02', elisa_year='2010')
    ER1.save()
    ER2 = Elisa.objects.create(result_id='ElisaChik_2', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020002'), elisa_day='25', elisa_month='02', elisa_year='2010')
    ER2.save()
    ER3 = Elisa.objects.create(result_id='ElisaChik_3', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020003'), elisa_day='25', elisa_month='02', elisa_year='2010')
    ER3.save()
    ER4 = Elisa.objects.create(result_id='ElisaChik_4', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020004'), elisa_day='25', elisa_month='02', elisa_year='2010')
    ER4.save()
    return redirect('import_elisa_choices')

def import_elisa_choices(request):
    # get_elisa_pathogens(request)
    if request.method == "POST":
        form = PathogenForm(request.POST)
        # form.widget.choices = ()
        # form.choices = (('1', 'First and only',),('2', 'Baguette du fromage',),)
        if form.is_valid():
            pathogen = "Chikungunya"
            #pathogen = form.save() ???? refund from cleaned_data ?
            #if pathogen == chik
            return redirect('import_chik_elisa', pathogen)
            #if pathogen == dengue
            # return redirect('import_dengue_elisa', pathogen)
            #if pathogen == rickettsia
            # return redirect('import_rickettsia_elisa', pathogen)

    else:
        form = PathogenForm()
        # form.widget.choices = ()
        # form.choices = (('1', 'First and only',),('2', 'Baguette du fromage',),)
    #Depending on the form response, send the user to import_chik_elisa, import_dengue_elisa or import_rickettsia_elisa
    return render (request, "sboapp/pages/import_elisa_choices.html", {'form':form})

def import_chik_elisa(request):
    #import function
    #When you fill each line you have to add 'chikungunya' to the pathogen value
    return render (request, "sboapp/pages/import_chik_elisa.html")

def import_dengue_elisa(request):
    #import function
    #When you fill each line you have to add 'dengue' to the pathogen value
    return render (request, "sboapp/pages/import_dengue_elisa.html")

def import_rickettsia_elisa(request):
    #import function
    #When you fill each line you have to add 'rickettsia' to the pathogen value
    return render (request, "sboapp/pages/import_rickettsia_elisa.html")

    # def import_pma(request):
    #     return render (request, "sboapp/pages/staff.html")


#---QUERY + EXPORT FROM DATABASE TO FILE

def query(request):
    # filter by parameters
    args = get_data(request)
    return render (request, "sboapp/pages/query.html", args)


def display_export(request):
    # display query answer and export button
    return render (request, "sboapp/pages/display_export.html")

#---DISPLAY TABLES

def display_tables(request):
    # TODO --> 20 RANDOM samples from db with corresponding location
    args = get_data(request)
    sample_id_list = list(Serum.objects.all().values_list('sample_id', flat=True))
    random_sample_id_list = random.sample(sample_id_list, min(len(sample_id_list), 20))
    freezer_sample_list = Freezer.objects.filter(sample__in=random_sample_id_list)
    serum_sample_list = Serum.objects.filter(sample_id__in=random_sample_id_list)
    args['serum_sample_list'] = serum_sample_list
    args['freezer_sample_list'] = freezer_sample_list
    return render (request, "sboapp/pages/display_tables.html", args)



# WORK IN PROGRESS

class UploadFileForm(forms.Form):
    file = forms.FileField()

def upload(request):
    pass
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         filehandle = request.FILES['file']
    #         return import_excel(request)
    # else:
    #     form = UploadFileForm()
    # return render(request,'sboapp/pages/upload_form.html',{
    #         'form': form,
    #         'title': 'Excel file upload',
    #         'header': 'Please choose a valid excel file'
    #     })

def handson_table(request):
    return excel.make_response_from_tables(
        [Serum], 'sboapp/pages/handsontable.html')

# def embed_handson_table(request):
#     """
#     Renders two table in a handsontable
#     """
#     content = excel.pe.save_book_as(
#         models=[Question, Choice],
#         dest_file_type='sboapp/pages/handsontable.html',
#         dest_embed=True)
#     content.seek(0)
#     return render(
#         request,
#         'custom-handson-table.html',
#         {
#             'handsontable_content': content.read()
#         })


def embed_handson_table_from_a_single_table(request):
    """
    Renders one table in a handsontable
    """
    content = excel.pe.save_as(
        model=Serum,
        dest_file_type='sboapp/pages/handsontable.html',
        dest_embed=True)
    content.seek(0)
    return render(
        request,
        'custom-handson-table.html',
        {
            'handsontable_content': content.read()
        })


#--------FIRST TESTS

# def detail(request, sample_id):
#     serum = get_object_or_404(Serum, pk=sample_id)
#     return render(request, 'sboapp/pages/detail.html', {'serum': serum}) #example with render --> template
#
# def vote(request, sample_id):
#     return HttpResponse("You're voting on serum %s." % sample_id) #example with HttpResponse --> no errors if the sample_id is unknown !
#
# def indextest(request):
#     first_3_serum = Serum.objects.order_by('local_sample_id')[:3]
#     note = 'Here are the first 3 serum added on the database: \n '
#     output = ', '.join([s.sample_id for s in first_3_serum])
#     return HttpResponse(note + output)

#-----------TEST IMPORT Data

# def import_data(request):
#     # le but de cette fonction est de upload des data à partir d'un sample_file de sera et de les transformer dans un nouveau tableau
#     # pour controler, il faudra display l'ancien et le nouveau tableau
#     if request.method == "POST":
#         form = UploadFileForm(request.POST,request.FILES)
#         if form.is_valid():
#             sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
#             colnames = list(sheet.colnames)
#             old_data = list()
#             for row in list(sheet.rows()):
#                 row_data = list()
#                 for cell in row:
#                     row_data.append(str(cell))
#                 old_data.append(row_data)
#             return render(request,'sboapp/pages/import_data.html',{'form':form,'note':'Your data has been imported successfully',"old_data":old_data, "colnames":colnames})
#         else:
#             warning = 'WARNING !\n import has failed \n the form is not valid'
#             print('import has failed')
#             return render (request, "sboapp/pages/import_data.html",{'warning':warning})
#     else:
#         form = UploadFileForm()
#     return render(request,'sboapp/pages/import_data.html',{'form': form})
#
# def display_import(request):
#     if "GET" == request.method:
#         return render(request, "sboapp/pages/display_import.html", {})
#     else:
#         excel_file = request.FILES["excel_file"]
#         sheet = pyexcel.get_sheet(file_name='excel_file')
#         sheet.save_as('display_import.html', display_length=10)
#         IFrame("display_import.html",width=600, height=500)
#         return render (request, "sboapp/pages/display_import.html", {})
#
# def import_excel(request):
#     #NOT OVER
#     #using pyexcel here
#     #Works for one table, Pay attention to the sensitive case
#     if request.method == "POST":
#         form = UploadFileForm(request.POST,request.FILES)
#         # def ward_func(row):
#         #     s = Serum.objects.filter(ward=row[0])[0]
#         #     row[0] = s
#         #     return row
#         if form.is_valid():
#             sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
#             sheet.save_to_django_model(
#                 model=Serum,
#                 # ,Ward,Site],
#                 initializer=None,
#                 # [None,ward_func],
#                 mapdict=None,
#                 # [
#                 #     ['local_sample_id', 'site', 'coll_num', 'sample_id','birth_year','age','age_min','age_max','gender_1ismale_value','coll_date','day_value','month_value','year','ward']
#                 #     # ,
#                 #     # ['ward_id','ward_name','khoa'],
#                 #     # ['site_id','site_name']
#                 #     ]
#             )
#             return render(request,'sboapp/pages/import_excel.html',{'form':form,'note':'Your data has been imported successfully'})
#         else:
#             warning = 'WARNING !\n import has failed \n the form is not valid'
#             print('import has failed')
#             return render (request, "sboapp/pages/import_excel.html",{'warning':warning})
#     else:
#         form = UploadFileForm()
#     return render(request,'sboapp/pages/import_excel.html',{'form': form})

# excel_f = request.FILES["excel_f"]
# sheet = excel.ExcelMixin.get_sheet(sheet_name=None, name_columns_by_row=0)
# colnames = list(sheet.colnames())
# # records = request.FILES["excel_file"].get_records()
# old_data = list(sheet.rows())
# new_data = list()

# you may put validations here to check extension or file size
# try:
#     wb = openpyxl.reader.excel.load_workbook(excel_f,data_only=True)
#     #print('import OK')
# except:
#     warning = 'WARNING !\n file not exist'
#     print('import failed')
#     return render (request, "sboapp/pages/import_data.html",{'warning':warning})
# else:
#     worksheet = wb["Sheet1"]
#     # iterating over the rows and
#     # getting value from each cell in row
#     for row in worksheet.iter_rows():
#         row_data = list()
#         for cell in row:
#             row_data.append(str(cell.value))
#         old_data.append(row_data)
# return render(request, "sboapp/pages/import_data.html", {"old_data":old_data, "colnames":colnames})
