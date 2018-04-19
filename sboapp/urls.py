from django.urls import path

from . import views

app_name = "sboapp"

urlpatterns = [
    #Staff_dashboard
    path('staff/', views.staff, name='staff'),
        #Import_data
    path('staff/import_data/display_import',views.display_import, name='display_import'),
    path('staff/import_data/',views.import_data, name='import_data'),
        #Query + Export
    path('staff/query', views.query, name ='query'),
    path('staff/query/display_export', views.display_export, name ='display_export'),
        #Display Tables
    path('dbtest/',views.databasetest, name='dbtest'),


    #WORK IN PROGRESS
    path('upload/',views.upload, name='upload'),

    # # ex: /sboapp/
    # path('', views.indextest, name='indextest'),
    # # ex: /sboapp/5/
    # path('<sample_id>/', views.detail, name='detail'),
    # # ex: /sboapp/5/vote/
    # path('<sample_id>/vote/', views.vote, name='vote'),

    #import django-excel
    path('import_excel/', views.import_excel, name="import"),
    path('handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    # path('embedded_handson_view/',views.embed_handson_table, name="embed_handson_view"),
    path('embedded_handson_view_single/',views.embed_handson_table_from_a_single_table,name="embed_handson_view"),
]
