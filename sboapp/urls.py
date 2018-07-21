from django.urls import path

from . import views

app_name = "sboapp"

urlpatterns = [
    #Staff_dashboard
    path('staff/', views.staff, name='staff'),
        #Import_data
    path('staff/import_serum/',views.import_serum, name='import_serum'),
    path('staff/import_location/',views.import_location, name='import_location'),
    path('staff/import_elisa_choices',views.import_elisa_choices, name='import_elisa_choices'),
    path('staff/import_elisa/Chikungunya',views.import_chik_elisa, name='import_chik_elisa'),
    path('staff/import_elisa/Dengue',views.import_dengue_elisa, name='import_dengue_elisa'),
    path('staff/import_elisa/Rickettsia',views.import_rickettsia_elisa, name='import_rickettsia_elisa'),
    path('staff/import_pma',views.import_pma, name='import_pma'),
        #Modify Location
    path('staff/modify_location',views.modify_location, name='modify_location'),
        #Modify Status
    path('staff/modify_status',views.modify_status, name='modify_status'),
        #Query + Export
        #Display Tables
    path('staff/tables/',views.display_tables, name='tables'),


    #WORK IN PROGRESS
    path('staff/sort_data', views.sort_data, name ='sort_data'),
    path('staff/sort_data/check_status', views.check_status, name ='check_status'),
    path('staff/sort_data/count_results', views.count_results, name ='count_results'),
    path('staff/sort_data/display_export', views.display_export, name ='display_export'),


    path('staff/init_elisa',views.init_elisa, name='init_elisa') #Delete this with the corresponding view once you import the whole db
]
