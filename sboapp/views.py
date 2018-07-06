from django.shortcuts import get_object_or_404, render, redirect #render is mainly used with templates while HttpResponse is used for data (for example)
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from sboapp.models import Serum, Site, Ward, Freezer, Elisa, Chik_elisa, Dengue_elisa, Rickettsia_elisa, Pma, Pma_result
from django import forms
from .forms import NameForm, PathogenForm, ExportFormatForm, DisplayDataForm, SortDataForm
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
    count_serum = count_element(Serum)
    count_site = count_element(Site)
    count_ward = count_element(Ward)
    args = {"serum_nb": dataserum,"site_nb": datasite,"ward_nb": dataward,"freezer_nb": datafreezer, "elisa_nb": dataelisa,"count_serum":count_serum,"count_site":count_site,"count_ward":count_ward}
    return args

def count_element(Model):
    count = Model.objects.all().count()
    return count

class UploadFileForm(forms.Form):
    file = forms.FileField()

# STAFF DASHBOARD
def staff(request):
    args = get_data(request)

    sample_id_list = list(Serum.objects.all().values_list('sample_id', flat=True))
    random_sample_id_list = random.sample(sample_id_list, min(len(sample_id_list), 5))
    serum_sample_list = Serum.objects.filter(sample_id__in=random_sample_id_list)
    args['serum_sample_list'] = serum_sample_list
    year_list=[]

    ag_list=[]
    bd_list=[]
    dc_list=[]
    dt_list=[]
    hc_list=[]
    hu_list=[]
    kg_list=[]
    kh_list=[]
    qn_list=[]
    st_list=[]

    query_year=Serum.objects.values_list('year').distinct()
    query_year=query_year.order_by('year')
    count_year=query_year.count()
    for i in range(count_year):
        year_list.append(query_year[i][0])
    args['year_list']=year_list
    site_list=['AG','BD','DC','DT','HC','HU','KG','KH','QN','ST']
    for i in range(len(year_list)):
        for j in range(len(site_list)):
            if site_list[j] == 'AG':
                ag_list.append(Serum.objects.filter(site_id='AG',year=year_list[i]).count())
            elif site_list[j] == 'BD':
                bd_list.append(Serum.objects.filter(site_id='BD',year=year_list[i]).count())
            elif site_list[j] == 'DC':
                dc_list.append(Serum.objects.filter(site_id='DC',year=year_list[i]).count())
            elif site_list[j] == 'DT':
                dt_list.append(Serum.objects.filter(site_id='DT',year=year_list[i]).count())
            elif site_list[j] == 'HC':
                hc_list.append(Serum.objects.filter(site_id='HC',year=year_list[i]).count())
            elif site_list[j] == 'HU':
                hu_list.append(Serum.objects.filter(site_id='HU',year=year_list[i]).count())
            elif site_list[j] == 'KG':
                kg_list.append(Serum.objects.filter(site_id='KG',year=year_list[i]).count())
            elif site_list[j] == 'KH':
                kh_list.append(Serum.objects.filter(site_id='KH',year=year_list[i]).count())
            elif site_list[j] == 'QN':
                qn_list.append(Serum.objects.filter(site_id='QN',year=year_list[i]).count())
            elif site_list[j] == 'ST':
                st_list.append(Serum.objects.filter(site_id='ST',year=year_list[i]).count())
    args['data_ag']=ag_list
    args['data_bd']=bd_list
    args['data_dc']=dc_list
    args['data_dt']=dt_list
    args['data_hc']=hc_list
    args['data_hu']=hu_list
    args['data_kg']=kg_list
    args['data_kh']=kh_list
    args['data_qn']=qn_list
    args['data_st']=st_list
    return render (request, "sboapp/pages/staff.html", args)

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            user_name = {"user_name":user_name}
            return render(request,'sboapp/pages/staff.html',user_name)
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
    if exist_count >= 1:
        return True
    else:
        return False

def site_id_exists(site_test_id): #Check if the site_id exists in the Site table, return Boolean
    exist_count = Site.objects.filter(site_id= site_test_id).count()
    if exist_count >= 1:
        return True
    else:
        return False

def sample_id_exists_in_freezer(sample_test_id): #Check if the sample_id exists in the Freezer table, return Boolean
    exist_count = Freezer.objects.filter(sample= sample_test_id).count()
    if exist_count >= 1:
        return True
    else:
        return False

def sample_id_exists_in_elisa(sample_test_id): #Check if the sample_test_id exists in Elisa table, return Boolean
    exist_count = Elisa.objects.filter(sample= sample_test_id).count()
    if exist_count >= 1:
        return True
    else:
        return False

def sample_id_exists_in_pma(sample_test_id): #Check if the sample_test_id exists in Pma table, return Boolean
    exist_count = Pma.objects.filter(sample= sample_test_id).count()
    if exist_count >= 1:
        return True
    else:
        return False

def index_finder(headers_list, header_test_list):
    for i in range(len(headers_list)):
        for j in range(len(header_test_list)):
            if re.match(header_test_list[j], headers_list[i], re.IGNORECASE) is not None:
                return i
    return None

def extract_value(input_list, output_list, match_index):
    if match_index is None:
        output_list.append("")
    else:
        for i in range(len(input_list)):
            if i == match_index:
                if str(input_list[i]) == 'NA':
                    output_list.append('')
                else:
                    input_list[i]= str(input_list[i]).strip("' ") #coll_date format
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

def count_sample(input_list, sample_test_id):
    cpt=0
    for i in range(len(input_list)):
        if str(input_list[i]) == str(sample_test_id):
            cpt+=1
    return cpt


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
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'local_sample_id']))
                        site_instance_converter(sheet_array[j],tmp,site_id_index) #Need to convert in Site instance
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'coll_num']))
                        extract_value(sheet_array[j],tmp,sample_id_index)
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'birth year']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'original age',r'age_original', r'age_value']))#special regex
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'age_min']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'age_max']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'gender_1ismale_value']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'coll_date']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'day_value']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'month_value']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'year',r'year_value']))#special regex
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
            sample_id_index = index_finder(sheet_array[0], [r'ParticipantNo',r'sample_id'])
            if sample_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_list.append(sheet_array[j][sample_id_index])
                    elif sample_id_exists_in_freezer(sheet_array[j][sample_id_index]) == True:
                        sample_exist_in_freezer_list.append(sheet_array[j][sample_id_index])
                    else:
                        tmp=[]
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'StudyCode']))
                        # extract_value(sheet_array[j],tmp,sample_id_index)
                        serum_instance_converter(sheet_array[j],tmp,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'SampleType']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'AliquotNo']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'Volume']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'freezer section name']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_1_position']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_2_position']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_3_position']))
                        extract_value(sheet_array[j],tmp,index_finder(sheet_array[0],[r'subdivision_4_position']))
                        db_list.append(tmp)

                #save list to database
                pyexcel.save_as(array=db_list,name_columns_by_row=0, dest_model=Freezer, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for ParticpantNo or sample_id \n These data can\'t be imported'

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

def modify_location(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_doesnt_exist_in_freezer_list = []
            report_list = [['sample','column','old value','new value']]
            sample_id_index = index_finder(sheet_array[0], [r'ParticipantNo',r'sample_id'])
            if sample_id_index is not None:
                print (len(sheet_array))
                for j in range(1,len(sheet_array)):
                    if sample_id_exists_in_freezer(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_in_freezer_list.append(sheet_array[j][sample_id_index])
                    else:
                        obj = Freezer.objects.get(sample=sheet_array[j][sample_id_index])
                        for k in range(len(sheet_array[0])):
                            if k == index_finder(sheet_array[0],[r'StudyCode']):
                                if str(obj.study_code) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Study Code',obj.study_code,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.study_code = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'SampleType']):
                                if str(obj.sample_type) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Sample Type',obj.sample_type,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.sample_type = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'AliquotNo']):
                                if str(obj.aliquot_no) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Aliquot No',obj.aliquot_no,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.aliquot_no = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'Volume']):
                                if str(obj.volume) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Volume',obj.volume,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.volume = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'freezer section name']):
                                if str(obj.freezer_section_name) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Freezer section name',obj.freezer_section_name,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.freezer_section_name = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'subdivision_1_position']):
                                if str(obj.subdivision_1_position) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Subdivision 1 position',obj.subdivision_1_position,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.subdivision_1_position = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'subdivision_2_position']):
                                if str(obj.subdivision_2_position) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Subdivision 2 position',obj.subdivision_2_position,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.subdivision_2_position = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'subdivision_3_position']):
                                if str(obj.subdivision_3_position) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Subdivision 3 position',obj.subdivision_3_position,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.subdivision_3_position = sheet_array[j][k]
                                    obj.save()
                            elif k == index_finder(sheet_array[0],[r'subdivision_4_position']):
                                if str(obj.subdivision_4_position) != str(sheet_array[j][k]):
                                    tmp=[]
                                    tmp.extend([sheet_array[j][sample_id_index],'Subdivision 4 position',obj.subdivision_4_position,sheet_array[j][k]])
                                    report_list.append(tmp)
                                    obj.subdivision_4_position = sheet_array[j][k]
                                    obj.save()
            else:
                headings_error = 'File\'s header error, no match for ParticipantNo or sample_id \n These data can\'t be imported'
            if len(sample_doesnt_exist_in_freezer_list) != 0 :
                headings_error=''
                sample_doesnt_exist_in_freezer_warning = 'Warning ! These following samples don\'t exist in the freezer table, you can\'t change their location \n'
                args = {'form': form, 'success':'Congratulations, your data have been modified successfully !', 'context':sheet_array,'sheet':sheet, 'report_list': report_list, 'sample_doesnt_exist_in_freezer_list':sample_doesnt_exist_in_freezer_list, 'sample_doesnt_exist_in_freezer_warning':sample_doesnt_exist_in_freezer_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been modified successfully !', 'context':sheet_array, 'report_list': report_list}
            return render (request, "sboapp/pages/modify_location.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/modify_location.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render(request,'sboapp/pages/modify_location.html', {'form': form })

def init_elisa(request): #This function was necessary to input first data in the database
    # ER1 = Elisa.objects.create(result_id='ElisaChik_AG000000_2', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020001'), elisa_day='25', elisa_month='02', elisa_year='2010')
    # ER1.save()
    # ER2 = Elisa.objects.create(result_id='ElisaChik_2', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020002'), elisa_day='25', elisa_month='02', elisa_year='2010')
    # ER2.save()
    # ER3 = Elisa.objects.create(result_id='ElisaChik_3', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020003'), elisa_day='25', elisa_month='02', elisa_year='2010')
    # ER3.save()
    # ER4 = Elisa.objects.create(result_id='ElisaChik_4', pathogen='chikungunya', sample=Serum.objects.get(sample_id='AG020004'), elisa_day='25', elisa_month='02', elisa_year='2010')
    # ER4.save()
    # ER5 = Elisa.objects.create(result_id='ElisaChik_5', pathogen='dengue', sample=Serum.objects.get(sample_id='AG020005'), elisa_day='25', elisa_month='02', elisa_year='2010')
    # ER5.save()
    # ER6 = Elisa.objects.create(result_id='ElisaChik_6', pathogen='rickettsia', sample=Serum.objects.get(sample_id='AG020006'), elisa_day='25', elisa_month='02', elisa_year='2010')
    # ER6.save()
    # ER7 = Chik_elisa.objects.create(elisa=Elisa.objects.get(result_id='ElisaChik_AG000000_2'), sample_absorbance='0.165', negative_absorbance='0.185', cut_off_1_absorbance='0.280', cut_off_2_absorbance='0.287',positive_absorbance='0.731', cut_off='0.284', novatech_units='5.820', result_chik='2')
    # ER7.save()
    # ER8 = Dengue_elisa.objects.create(elisa=Elisa.objects.get(result_id='ElisaChik_AG000000_2'), sample_absorbance='0', negative_absorbance='0', positive_absorbance='0', calibrator_1_absorbance='0', calibrator_2_absorbance='0', calibrator_3_absorbance='0', cal_factor='0', cut_off='0', positive_cut_off_ratio='0', dengue_index='0')
    # ER8.save()
    # ER9 = Rickettsia_elisa.objects.create(elisa=Elisa.objects.get(result_id='ElisaChik_AG000000_2'), scrub_typhus='0', typhus='0')
    # ER9.save()
    return redirect('import_elisa_choices')

def import_elisa_choices(request):
    if request.method == "POST":
        form = PathogenForm(request.POST)
        if form.is_valid():
            pathogen = form.cleaned_data.get('pathogen')
            if pathogen == "chikungunya":
                return redirect('import_elisa/Chikungunya')
            elif pathogen == "dengue":
                return redirect('import_elisa/Dengue')
            elif pathogen == "rickettsia":
                return redirect('import_elisa/Rickettsia')
            else:
                render (request, "sboapp/pages/import_elisa_choices.html", {'error_note':'Please select a pathogen'})

    else:
        form = PathogenForm()
    return render (request, "sboapp/pages/import_elisa_choices.html", {'form':form})

def import_chik_elisa(request):
    #import function
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_doesnt_exist_list = []
            chik_import_list = []
            db_elisa_list = [['result_id','pathogen','sample','elisa_day','elisa_month','elisa_year']]
            db_chik_list = [['elisa','sample_absorbance','negative_absorbance','cut_off_1_absorbance', 'cut_off_2_absorbance', 'positive_absorbance', 'cut_off', 'novatech_units', 'result_chik']]
            sample_id_index = index_finder(sheet_array[0], [r'sample_id'])
            if sample_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_list.append(sheet_array[j][sample_id_index])
                    elif sample_id_exists_in_elisa(sheet_array[j][sample_id_index]) == True:
                        tmp_elisa_not_first = []
                        nb = Elisa.objects.filter(sample = sheet_array[j][sample_id_index]).count()
                        result_id = 'Elisa'+'Chik'+'_'+str(sheet_array[j][sample_id_index])+'_'+str(nb+1)
                        tmp_elisa_not_first.append(result_id)
                        chik_import_list.append(result_id)
                        pathogen = 'chikungunya'
                        tmp_elisa_not_first.append(pathogen)
                        serum_instance_converter(sheet_array[j],tmp_elisa_not_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_year',r'processedyear']))
                        db_elisa_list.append(tmp_elisa_not_first)

                    else:
                        tmp_elisa_first=[]
                        result_id = str('Elisa'+'Chik'+'_'+sheet_array[j][sample_id_index]+'_'+'1')
                        tmp_elisa_first.append(result_id)
                        chik_import_list.append(result_id)
                        pathogen = 'chikungunya'
                        tmp_elisa_first.append(pathogen)
                        serum_instance_converter(sheet_array[j],tmp_elisa_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_year',r'processedyear']))
                        db_elisa_list.append(tmp_elisa_first)
                #save list to database
                pyexcel.save_as(array=db_elisa_list,name_columns_by_row=0, dest_model=Elisa, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for sample_id\n These data can\'t be imported'

            if len(chik_import_list) !=0 :
                for k in range(len(chik_import_list)):
                    elisa_obj = Elisa.objects.get(result_id=chik_import_list[k])
                    print("elisa obj : ", elisa_obj)
                    for j in range(1,len(sheet_array)):
                        print("pre test : - ", elisa_obj.sample, "sheet array : - ",sheet_array[j][sample_id_index])
                        if str(sheet_array[j][sample_id_index]) == str(elisa_obj.sample): #comparaison avec le sample_id correspondant au result_id stocke dans chik_import_list
                            print("post test elisa obj sample")
                            tmp_chik_elisa=[]
                            elisa = elisa_obj
                            tmp_chik_elisa.append(elisa)
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'sample_absorbance', r'sampleabsorbance']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'negative_absorbance', r'negativeabsorbance']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'cut_off_1_absorbance', r'cut-off1absorbance']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'cut_off_2_absorbance', r'cut-off2absorbance']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'positive_absorbance', r'positiveabsorbance']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'cut_off', r'cut-off']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'novatech_units', r'novatec_units']))
                            extract_value(sheet_array[j],tmp_chik_elisa,index_finder(sheet_array[0],[r'result']))
                            db_chik_list.append(tmp_chik_elisa)

                #save list to database
                pyexcel.save_as(array=db_chik_list,name_columns_by_row=0, dest_model=Chik_elisa, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)

            if len(sample_doesnt_exist_list) != 0 :
                headings_error=''
                sample_doesnt_exist_warning = 'Warning ! These following samples don\'t exist in the serum bank, you can\'t add elisa results before to add them in the serum bank: \n'
                args = {'form': form, 'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array,'sheet':sheet, 'db_chik_list': db_chik_list, 'db_elisa_list':db_elisa_list, 'sample_doesnt_exist':sample_doesnt_exist_list, 'sample_doesnt_exist_warning':sample_doesnt_exist_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array, 'db_chik_list': db_chik_list, 'db_elisa_list': db_elisa_list}
            return render (request, "sboapp/pages/import_chik_elisa.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/import_chik_elisa.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render (request, "sboapp/pages/import_chik_elisa.html", {'form': form})

def import_dengue_elisa(request):
    #import function
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_doesnt_exist_list = []
            dengue_import_list = []
            db_elisa_list = [['result_id','pathogen','sample','elisa_day','elisa_month','elisa_year']]
            db_dengue_list = [['elisa','sample_absorbance','negative_absorbance','positive_absorbance','calibrator_1_absorbance', 'calibrator_2_absorbance','calibrator_3_absorbance','cal_factor','cut_off','positive_cut_off_ratio','dengue_index','panbio_unit','result_dengue']]
            sample_id_index = index_finder(sheet_array[0], [r'sample_id'])
            if sample_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_list.append(sheet_array[j][sample_id_index])
                    elif sample_id_exists_in_elisa(sheet_array[j][sample_id_index]) == True:
                        tmp_elisa_not_first = []
                        nb = Elisa.objects.filter(sample = sheet_array[j][sample_id_index]).count()
                        result_id = 'Elisa'+'Dengue'+'_'+str(sheet_array[j][sample_id_index])+'_'+str(nb+1)
                        tmp_elisa_not_first.append(result_id)
                        dengue_import_list.append(result_id)
                        pathogen = 'dengue'
                        tmp_elisa_not_first.append(pathogen)
                        serum_instance_converter(sheet_array[j],tmp_elisa_not_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_year',r'processedyear']))
                        db_elisa_list.append(tmp_elisa_not_first)

                    else:
                        tmp_elisa_first=[]
                        result_id = str('Elisa'+'Dengue'+'_'+sheet_array[j][sample_id_index]+'_'+'1')
                        tmp_elisa_first.append(result_id)
                        dengue_import_list.append(result_id)
                        pathogen = 'dengue'
                        tmp_elisa_first.append(pathogen)
                        serum_instance_converter(sheet_array[j],tmp_elisa_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_year',r'processedyear']))
                        db_elisa_list.append(tmp_elisa_first)
                #save list to database
                pyexcel.save_as(array=db_elisa_list,name_columns_by_row=0, dest_model=Elisa, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for sample_id\n These data can\'t be imported'

            if len(dengue_import_list) !=0 :
                for k in range(len(dengue_import_list)):
                    elisa_obj = Elisa.objects.get(result_id=dengue_import_list[k])
                    for j in range(1,len(sheet_array)):
                        if str(sheet_array[j][sample_id_index]) == str(elisa_obj.sample): #comparaison avec le sample_id correspondant au result_id stocke dans chik_import_list
                            tmp_dengue_elisa=[]
                            elisa = elisa_obj
                            tmp_chik_elisa.append(elisa)
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'sample_absorbance', r'sampleabsorbance']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'negative_absorbance', r'negativeabsorbance']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'positive_absorbance', r'positiveabsorbance']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'calibrator_1_absorbance']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'calibrator_2_absorbance']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'calibrator_3_absorbance']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'cal_factor']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'cut_off', r'cut-off']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'positive_cut_off_ratio']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'dengue_index', r'index']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'panbio_unit']))
                            extract_value(sheet_array[j],tmp_dengue_elisa,index_finder(sheet_array[0],[r'result']))
                            db_dengue_list.append(tmp_dengue_elisa)

                #save list to database
                pyexcel.save_as(array=db_dengue_list,name_columns_by_row=0, dest_model=Dengue_elisa, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)

            if len(sample_doesnt_exist_list) != 0 :
                headings_error=''
                sample_doesnt_exist_warning = 'Warning ! These following samples don\'t exist in the serum bank, you can\'t add elisa results before to add them in the serum bank: \n'
                args = {'form': form, 'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array,'sheet':sheet, 'db_dengue_list': db_dengue_list, 'db_elisa_list':db_elisa_list, 'sample_doesnt_exist':sample_doesnt_exist_list, 'sample_doesnt_exist_warning':sample_doesnt_exist_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array, 'db_dengue_list': db_dengue_list, 'db_elisa_list': db_elisa_list}
            return render (request, "sboapp/pages/import_dengue_elisa.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/import_dengue_elisa.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render (request, "sboapp/pages/import_dengue_elisa.html", {'form': form})

def import_rickettsia_elisa(request):
    #import function
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_doesnt_exist_list = []
            rickettsia_import_list = []
            db_elisa_list = [['result_id','pathogen','sample','elisa_day','elisa_month','elisa_year']]
            db_rickettsia_list = [['elisa','scrub_typhus','typhus']]
            sample_id_index = index_finder(sheet_array[0], [r'sample_id'])
            if sample_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_list.append(sheet_array[j][sample_id_index])
                    elif sample_id_exists_in_elisa(sheet_array[j][sample_id_index]) == True:
                        tmp_elisa_not_first = []
                        nb = Elisa.objects.filter(sample = sheet_array[j][sample_id_index]).count()
                        result_id = 'Elisa'+'Ricket'+'_'+str(sheet_array[j][sample_id_index])+'_'+str(nb+1)
                        tmp_elisa_not_first.append(result_id)
                        rickettsia_import_list.append(result_id)
                        pathogen = 'rickettsia'
                        tmp_elisa_not_first.append(pathogen)
                        serum_instance_converter(sheet_array[j],tmp_elisa_not_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_elisa_not_first,index_finder(sheet_array[0],[r'elisa_year',r'processedyear']))
                        db_elisa_list.append(tmp_elisa_not_first)

                    else:
                        tmp_elisa_first=[]
                        result_id = str('Elisa'+'Ricket'+'_'+sheet_array[j][sample_id_index]+'_'+'1')
                        tmp_elisa_first.append(result_id)
                        rickettsia_import_list.append(result_id)
                        pathogen = 'rickettsia'
                        tmp_elisa_first.append(pathogen)
                        serum_instance_converter(sheet_array[j],tmp_elisa_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_elisa_first,index_finder(sheet_array[0],[r'elisa_year',r'processedyear']))
                        db_elisa_list.append(tmp_elisa_first)
                #save list to database
                pyexcel.save_as(array=db_elisa_list,name_columns_by_row=0, dest_model=Elisa, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for sample_id\n These data can\'t be imported'

            if len(rickettsia_import_list) !=0 :
                for k in range(len(rickettsia_import_list)):
                    elisa_obj = Elisa.objects.get(result_id=rickettsia_import_list[k])
                    for j in range(1,len(sheet_array)):
                        if str(sheet_array[j][sample_id_index]) == str(elisa_obj.sample): #comparaison avec le sample_id correspondant au result_id stocke dans chik_import_list
                            tmp_rickettsia_elisa=[]
                            elisa = elisa_obj
                            tmp_chik_elisa.append(elisa)
                            extract_value(sheet_array[j],tmp_rickettsia_elisa,index_finder(sheet_array[0],[r'scrub_typhus']))
                            extract_value(sheet_array[j],tmp_rickettsia_elisa,index_finder(sheet_array[0],[r'typhus']))
                            db_rickettsia_list.append(tmp_rickettsia_elisa)

                #save list to database
                pyexcel.save_as(array=db_rickettsia_list,name_columns_by_row=0, dest_model=Rickettsia_elisa, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)

            if len(sample_doesnt_exist_list) != 0 :
                serums_error =''
                headings_error=''
                sample_doesnt_exist_warning = 'Warning ! These following samples don\'t exist in the serum bank, you can\'t add elisa results before to add them in the serum bank: \n'
                args = {'form': form, 'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array,'sheet':sheet, 'db_rickettsia_list': db_rickettsia_list, 'db_elisa_list':db_elisa_list, 'sample_doesnt_exist':sample_doesnt_exist_list, 'sample_doesnt_exist_warning':sample_doesnt_exist_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array, 'db_rickettsia_list': db_rickettsia_list, 'db_elisa_list': db_elisa_list}
            return render (request, "sboapp/pages/import_rickettsia_elisa.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/import_rickettsia_elisa.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render (request, "sboapp/pages/import_rickettsia_elisa.html", {'form': form})

def import_pma(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            sheet = request.FILES['file'].get_sheet(sheet_name=None, name_columns_by_row=0)
            sheet_array = sheet.get_array()
            sample_doesnt_exist_list = []
            pma_result_import_list = []
            pma_id_import_list = []
            db_pma_list = [['result_id','ag_array_id','tray','batch_id','sample','start_dilution','file_name','processed_day','processed_month','processed_year','batch_sent_id','scanned_day','scanned_month','scanned_year','panbio_unit']]
            db_pma_result_list = [['pma','chikv_e1_mutant','chikv_e2','dv1_ns1','dv2_ns1','dv3_ns1','dv4_ns1','jev_ns1','slev_ns1','tbev_ns1','wnv_ns1','yfv_ns1','zikv_brasil_ns1','zikv_ns1']]
            sample_id_index = index_finder(sheet_array[0], [r'sample_id', r'sampleid'])
            if sample_id_index is not None:
                for j in range(1,len(sheet_array)):
                    if sample_id_exists(sheet_array[j][sample_id_index]) == False:
                        sample_doesnt_exist_list.append(sheet_array[j][sample_id_index])
                    elif sample_id_exists_in_pma(sheet_array[j][sample_id_index]) == True or count_sample(pma_result_import_list,sheet_array[j][sample_id_index]) !=0:
                        tmp_pma_not_first = []
                        nb = Pma.objects.filter(sample = sheet_array[j][sample_id_index]).count() #results in database per sample
                        cpt = count_sample(pma_result_import_list,sheet_array[j][sample_id_index])
                        result_id = 'Pma'+'_'+str(sheet_array[j][sample_id_index])+'_'+str(nb+cpt+1)
                        tmp_pma_not_first.append(result_id)
                        pma_id_import_list.append(result_id)
                        pma_result_import_list.append(sheet_array[j][sample_id_index])
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'ag_array_id',r'agarrayid']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'tray']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'batch_id',r'batchid']))
                        serum_instance_converter(sheet_array[j],tmp_pma_not_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'start_dilution',r'startdilution']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'file_name',r'filename']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'processed_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'processed_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'processed_year',r'processedyear']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'batch_sent_id',r'batchsentid']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'scanned_day',r'scannedday']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'scanned_month',r'scannedmonth']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'scanned_year',r'scannedyear']))
                        extract_value(sheet_array[j],tmp_pma_not_first,index_finder(sheet_array[0],[r'panbio_unit',r'panbiounit']))
                        db_pma_list.append(tmp_pma_not_first)

                    else: # sample not in pma database and not in the import list --> first pma result for this sample
                        tmp_pma_first=[]
                        result_id = str('Pma'+'_'+sheet_array[j][sample_id_index]+'_'+'1')
                        tmp_pma_first.append(result_id)
                        pma_id_import_list.append(result_id)
                        pma_result_import_list.append(sheet_array[j][sample_id_index])
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'ag_array_id',r'agarrayid']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'tray']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'batch_id',r'batchid']))
                        serum_instance_converter(sheet_array[j],tmp_pma_first,sample_id_index) #Need to convert in Serum instance
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'start_dilution',r'startdilution']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'file_name',r'filename']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'processed_day',r'processedday']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'processed_month',r'processedmonth']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'processed_year',r'processedyear']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'batch_sent_id',r'batchsentid']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'scanned_day',r'scannedday']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'scanned_month',r'scannedmonth']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'scanned_year',r'scannedyear']))
                        extract_value(sheet_array[j],tmp_pma_first,index_finder(sheet_array[0],[r'panbio_unit',r'panbiounit']))
                        db_pma_list.append(tmp_pma_first)
                #save list to database
                pyexcel.save_as(array=db_pma_list,name_columns_by_row=0, dest_model=Pma, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)
            else:
                headings_error = 'File\'s header error, no match for sample_id or sampleid \n These data can\'t be imported'

            if len(pma_id_import_list) !=0 :
                for k in range(len(pma_id_import_list)):
                    pma_obj = Pma.objects.get(result_id=pma_id_import_list[k])
                    for j in range(1,len(sheet_array)):
                        if str(sheet_array[j][sample_id_index]) == str(pma_obj.sample): #comparaison avec le sample_id correspondant au result_id stocke dans chik_import_list
                            tmp_pma_result=[]
                            pma = pma_obj
                            tmp_pma_result.append(pma)
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'chikv_e1_mutant',r'^chikv.e1'])) # the caret ^ means 'start by'
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'chikv_e2',r'^chikv.e2']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'dv1_ns1',r'^dv1']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'dv2_ns1',r'^dv2']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'dv3_ns1',r'^dv3']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'dv4_ns1',r'^dv4']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'jev_ns1',r'^jev']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'slev_ns1',r'^slev']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'tbev_ns1',r'^tbev']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'wnv_ns1',r'^wnv']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'yfv_ns1',r'^yfv']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'zikv_brasil_ns1',r'^zikv.brasil']))
                            extract_value(sheet_array[j],tmp_pma_result,index_finder(sheet_array[0],[r'zikv_ns1',r'zikv...ns1']))
                            db_pma_result_list.append(tmp_pma_result)

                #save list to database
                pyexcel.save_as(array=db_pma_result_list,name_columns_by_row=0, dest_model=Pma_result, dest_initializer=None, dest_mapdict=None, dest_batch_size=None)

            if len(sample_doesnt_exist_list) != 0 :
                headings_error=''
                sample_doesnt_exist_warning = 'Warning ! These following samples don\'t exist in the serum bank, you can\'t add pma results before to add them in the serum bank: \n'
                args = {'form': form, 'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array,'sheet':sheet, 'db_pma_result_list': db_pma_result_list, 'db_pma_list': db_pma_list, 'sample_doesnt_exist':sample_doesnt_exist_list, 'sample_doesnt_exist_warning':sample_doesnt_exist_warning, 'headings_error':headings_error}
            else:
                args = {'form': form,'success':'Congratulations, your data have been imported successfully !', 'context':sheet_array, 'db_pma_result_list': db_pma_result_list, 'db_pma_list': db_pma_list}
            return render (request, "sboapp/pages/import_pma.html", args)
        else:
            warning = 'WARNING !\n import has failed \n the form is not valid'
            return render (request, "sboapp/pages/import_pma.html",{'warning':warning})
    else:
        form = UploadFileForm()
    return render (request, "sboapp/pages/import_pma.html", {'form': form})

#---QUERY + EXPORT FROM DATABASE TO FILE
def check_clean_data(form,model,field):
    q = model.objects.get(field=form.cleaned_data.get(field))
    if q is not null:
        return q
    else:
        return None

def query(request):
    # filter by parameters TEST
    args = get_data(request)
    return render (request, "sboapp/pages/query.html", args)


def display_exp(request):
    # display query answer and export button TEST
    return render (request, "sboapp/pages/display_exp.html")

def sort_data(request):
    # filter by parameters
    # args = get_data(request)
    args={}
    queryset=Serum.objects.all()
    if request.method == "POST":
        sort_form = SortDataForm(request.POST)
        if sort_form.is_valid():
            args['valid_error']= "form is valid"
            if sort_form.has_changed():
                print ('changed is good')
                changed_list=sort_form.changed_data
                args['changed_list']=changed_list
                sample_id = sort_form.cleaned_data['sample_id']
                site_id = sort_form.cleaned_data['site_id']
                coll_num = sort_form.cleaned_data['coll_num']
                birth_year = sort_form.cleaned_data['birth_year']
                age = sort_form.cleaned_data['age']
                age_min = sort_form.cleaned_data['age_min']
                age_max = sort_form.cleaned_data['age_max']
                gender = sort_form.cleaned_data['birth_year']
                coll_date = sort_form.cleaned_data['coll_date']
                year = sort_form.cleaned_data['year']
                ward_id = sort_form.cleaned_data['ward_id']
                study_code = sort_form.cleaned_data['study_code']
                sample_type = sort_form.cleaned_data['sample_type']
                aliquot_no = sort_form.cleaned_data['aliquot_no']
                volume = sort_form.cleaned_data['volume']
                freezer_section_name = sort_form.cleaned_data['freezer_section_name']
                subdivision_1_position = sort_form.cleaned_data['subdivision_1_position']
                subdivision_2_position = sort_form.cleaned_data['subdivision_2_position']
                subdivision_3_position = sort_form.cleaned_data['subdivision_3_position']
                subdivision_4_position = sort_form.cleaned_data['subdivision_4_position']

                if sample_id:
                    print("j'ai le sample")
                    if Serum.objects.filter(sample_id=sort_form.cleaned_data.get('sample_id')).exists() is True:
                        queryset.filter(sample_id=sort_form.cleaned_data.get('sample_id'))

                    else:
                        print('aled')
                else:
                    print("j'ai pas le sample")

                if site_id:
                    print("j'ai le site : ",site_id)
                    queryset = queryset.filter(site__site_id__in=site_id)
                    print('queryset : ',queryset)
                    # args['site_id'] = queryset
                else:
                    print("j'ai pas le site : ",site_id)

                if coll_num:
                    print("j'ai la coll_num : ",coll_num)
                    queryset = queryset.filter(coll_num__in=coll_num)
                else:
                    print("j'ai pas la coll_num : ",coll_num)

                if birth_year:
                    print("j'ai la birth_year : ",birth_year)
                    queryset = queryset.filter(birth_year__in=birth_year)
                else:
                    print("j'ai pas la birth_year : ",birth_year)

                if age:
                    print("j'ai l'age : ",age)
                    queryset = queryset.filter(age__in=age)
                else:
                    print("j'ai pas l'age : ",age)

                if age_min:
                    print("j'ai l'age_min : ",age_min)
                    queryset = queryset.filter(age_min__in=age_min)
                else:
                    print("j'ai pas l'age_min : ",age_min)

                if age_max:
                    print("j'ai l'age_max : ",age_max)
                    queryset = queryset.filter(age_max__in=age_max)
                else:
                    print("j'ai pas l'age_max : ",age_max)

                if gender:
                    print("j'ai le gender : ",gender)
                    queryset = queryset.filter(gender__in=gender)
                else:
                    print("j'ai pas le gender : ",gender)

                if coll_date:
                    print("j'ai la coll_date : ",coll_date)
                    queryset = queryset.filter(coll_date__in=coll_date)
                else:
                    print("j'ai pas la coll_date : ",coll_date)

                if year:
                    print("j'ai la year : ",year)
                    queryset = queryset.filter(year__in=year)
                else:
                    print("j'ai pas la year : ",year)

                if ward_id:
                    print("j'ai le ward_id : ",ward_id)
                    queryset = queryset.filter(ward__ward_id__in=ward_id)
                else:
                    print("j'ai pas le ward_id : ",ward_id)

                if study_code:
                    print("j'ai le study_code : ",study_code)
                    queryset = queryset.filter(study_code__in=study_code)
                else:
                    print("j'ai pas le study_code : ",study_code)

                if sample_type:
                    print("j'ai le sample_type : ",sample_type)
                    queryset = queryset.filter(sample_type__in=sample_type)
                else:
                    print("j'ai pas le sample_type : ",sample_type)

                if aliquot_no:
                    print("j'ai le aliquot_no : ",aliquot_no)
                    queryset = queryset.filter(aliquot_no__in=aliquot_no)
                else:
                    print("j'ai pas le aliquot_no : ",aliquot_no)

                if volume:
                    print("j'ai le volume : ",volume)
                    queryset = queryset.filter(volume__in=volume)
                else:
                    print("j'ai pas le volume : ",volume)

                if freezer_section_name:
                    print("j'ai le freezer_section_name : ",freezer_section_name)
                    queryset = queryset.filter(freezer__freezer_section_name__in=freezer_section_name)
                else:
                    print("j'ai pas le freezer_section_name : ",freezer_section_name)

                if subdivision_1_position:
                    print("j'ai le subdivision_1_position : ",subdivision_1_position)
                    queryset = queryset.filter(freezer__subdivision_1_position__in=subdivision_1_position)
                else:
                    print("j'ai pas le subdivision_1_position : ",subdivision_1_position)

                if subdivision_2_position:
                    print("j'ai le subdivision_2_position : ",subdivision_2_position)
                    queryset = queryset.filter(freezer__subdivision_2_position__in=subdivision_2_position)
                else:
                    print("j'ai pas le subdivision_2_position : ",subdivision_2_position)

                if subdivision_3_position:
                    print("j'ai le subdivision_3_position : ",subdivision_3_position)
                    queryset = queryset.filter(freezer__subdivision_3_position__in=subdivision_3_position)
                else:
                    print("j'ai pas le subdivision_3_position : ",subdivision_3_position)

                if subdivision_4_position:
                    print("j'ai le subdivision_4_position : ",subdivision_4_position)
                    queryset = queryset.filter(freezer__subdivision_4_position__in=subdivision_4_position)
                else:
                    print("j'ai pas le subdivision_4_position : ",subdivision_4_position)

                if queryset == None:
                    args['queryset_error']='Warning ! There is no match for your query .'
                else:
                    args['queryset']=queryset
                    args['queryset_count']=queryset.count()
            else:
                print('Nothing has changed')
            return render (request, "sboapp/pages/validate_query.html",args)
            # return render(request,'sort_data/validate_query',args)
        else:
            args['valid_error']= "valid error"
            return render(request, "sboapp/pages/sort_data.html", args)
    else:
        sort_form = SortDataForm()
    args = {'sort_form':sort_form}
    return render (request, "sboapp/pages/sort_data.html", args)

def validate_query(request):
    #recuperer le queryset, faire un count de serum et display dans un chart
    # filter by parameters
    if request.method == "POST":
        args['oui']='oui'
        print (args)
    else:
        args['non']='non'
    return render (request, "sboapp/pages/validate_query.html",args)

def display_export(request):
    # Get queryset from sort_data function
    # display query answer and export button VOIR API django_excel
    if request.method == "POST":
        display_form = DisplayDataForm(request.POST)
        args={}
        if display_form.is_valid():
            args['valid_error']= "form is valid"
            return render (request, "display_export.html",args)
             #construire le fichier de sortie en fonction des cases selectionnees
        else:
            return render(request,"sboapp/pages/display_export.html",{'error_display_form': ' Display data form error'})
        # export_form = ExportFormatForm(request.POST)
        # if export_form.is_valid():
        #     format_choice = export_form.cleaned_data.get('format')
        #     if format_choice == "xls":
        #         pass
        #         # excel.make_response_from_query_sets(query_sets, column_names, 'xls', status=200)
        #     elif format_choice == "xlsx":
        #         pass
        #         # excel.make_response_from_query_sets(query_sets, column_names, 'xlsx', status=200)
        #     elif format_choice == "ods":
        #         pass
        #         # excel.make_response_from_query_sets(query_sets, column_names, 'ods', status=200)
        #     elif format_choice == "csv":
        #         pass
        #         # excel.make_response_from_query_sets(query_sets, column_names, 'csv', status=200)
        #     else:
        #         return render (request, "sboapp/pages/display_export.html", {'error_format_form':'Please select a file type'})
    else:
        # export_form = ExportFormatForm()
        display_form = DisplayDataForm()
    args = {'display_form':display_form}
    return render (request, "sboapp/pages/display_export.html", args)


#---DISPLAY TABLES

def display_tables(request):
    args = get_data(request)
    sample_id_list = list(Serum.objects.all().values_list('sample_id', flat=True))
    random_sample_id_list = random.sample(sample_id_list, min(len(sample_id_list), 20))
    freezer_sample_list = Freezer.objects.filter(sample__in=random_sample_id_list)
    serum_sample_list = Serum.objects.filter(sample_id__in=random_sample_id_list)
    args['serum_sample_list'] = serum_sample_list
    args['freezer_sample_list'] = freezer_sample_list
    return render (request, "sboapp/pages/display_tables.html", args)


# WORK IN PROGRESS
