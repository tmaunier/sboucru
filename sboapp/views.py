from django.shortcuts import get_object_or_404, render, redirect #render is mainly used with templates while HttpResponse is used for data (for example)
from django.http import HttpResponse, HttpResponseBadRequest
from sboapp.models import Serum, Site, Ward, Freezer
from django import forms
from django.db.models import Count
import openpyxl #module to read Excel files in Django
import pyexcel
import django_excel as excel
from IPython.display import IFrame


# ERRORS 404 & 500

def error_404_view(request, exception):
    return render(request,'sboapp/pages/error_404.html')

#def error_500_view(request, exception):
#    return render(request,'sboapp/pages/error_500.html')

# STAFF DASHBOARD
def staff(request):
    return render (request, "sboapp/pages/staff.html")
#---IMPORT DATA FROM FILE TO DATABASE

#---QUERY + EXPORT FROM DATABASE TO FILE

def query(request):
    # filter by parameters
    dataserum = Serum.objects.all()
    datasite = Site.objects.all()
    dataward = Ward.objects.all()
    datafreezer = Freezer.objects.all()
    args = {"serum_nb": dataserum,"site_nb": datasite,"ward_nb": dataward,"freezer_nb": datafreezer}
    return render (request, "sboapp/pages/query.html", args)

def display_export(request):
    # display query answer and export button
    return render (request, "sboapp/pages/display_export.html")

#---DISPLAY TABLES

def databasetest(request):
    dataserum = Serum.objects.all()
    datasite = Site.objects.all()
    dataward = Ward.objects.all()
    datafreezer = Freezer.objects.all()
    args = {"serum_nb": dataserum,"site_nb": datasite,"ward_nb": dataward,"freezer_nb": datafreezer}
    return render (request, "sboapp/pages/databasetest.html", args)



# WORK IN PROGRESS

def import_data(request):
    if "GET" == request.method:
        return render(request, "sboapp/pages/import_data.html", {})
    else:
        excel_file = request.FILES["excel_file"]
        records = request.FILES["excel_file"].get_records()
        #print('file size in bytes : ',excel_file.size)
        excel_data = list()

        # you may put validations here to check extension or file size
        try:
            #print('Check before import')
            # wb = openpyxl.load_workbook(excel_file)
            wb = openpyxl.reader.excel.load_workbook(excel_file,data_only=True)
            #print('import OK')
        except:
            warning = 'WARNING !\n file not exist'
            print('import failed')
            return render (request, "sboapp/pages/import_data.html",{'warning':warning})
        else:
            # getting a particular sheet by name out of many sheets
            worksheet = wb["Sheet1"]
            # print(worksheet)


            # iterating over the rows and
            # getting value from each cell in row
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)

            # sheet = pyexcel.get_sheet(worksheet, row, cell)
            # sheet.save_as('display_import.html', display_length=10)
            # IFrame("display_import.html",width=600, height=500)

    return render(request, "sboapp/pages/import_data.html", {"excel_data":excel_data})

def display_import(request):
    if "GET" == request.method:
        return render(request, "sboapp/pages/display_import.html", {})
    else:
        excel_file = request.FILES["excel_file"]
        sheet = pyexcel.get_sheet(file_name='excel_file')
        sheet.save_as('display_import.html', display_length=10)
        IFrame("display_import.html",width=600, height=500)
        return render (request, "sboapp/pages/display_import.html", {})

def import_excel(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        # def ward_func(row):
        #     s = Serum.objects.filter(ward=row[0])[0]
        #     row[0] = s
        #     return row
        if form.is_valid():
            request.FILES['file'].save_to_database(
                model=Serum,
                # ,Ward,Site],
                initializers=None,
                # [None,ward_func],
                mapdicts__iexact=[
                    ['local_sample_id', 'site', 'coll_num', 'sample_id','birth_year','age_min','age_max','gender_1ismale_value','coll_date','day_value','month_value','year','ward']
                    # ,
                    # ['ward_id','ward_name','khoa'],
                    # ['site_id','site_name']
                    ]
            )
            return HttpResponse("Your data has been successfully imported")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request,'sboapp/pages/upload_form.html',
        {
            'form': form,
        })



class UploadFileForm(forms.Form):
    file = forms.FileField()

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return import_excel(request)
    else:
        form = UploadFileForm()
    return render(request,'sboapp/pages/upload_form.html',{
            'form': form,
            'title': 'Excel file upload',
            'header': 'Please choose a valid excel file'
        })

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
