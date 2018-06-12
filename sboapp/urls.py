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
        #Query + Export
    path('staff/query', views.query, name ='query'),
    path('staff/query/display_export', views.display_export, name ='display_export'),
        #Display Tables
    path('staff/tables/',views.display_tables, name='tables'),


    #WORK IN PROGRESS
    path('staff/init_elisa',views.init_elisa, name='init_elisa'),


    # # ex: /sboapp/
    # path('', views.indextest, name='indextest'),
    # # ex: /sboapp/5/
    # path('<sample_id>/', views.detail, name='detail'),
    # # ex: /sboapp/5/vote/
    # path('<sample_id>/vote/', views.vote, name='vote'),

    #import django-excel
    path('handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    # path('embedded_handson_view/',views.embed_handson_table, name="embed_handson_view"),
    path('embedded_handson_view_single/',views.embed_handson_table_from_a_single_table,name="embed_handson_view"),
]
