from django.urls import path

from . import views

app_name = "sboapp"

urlpatterns = [
    path('dbtest/',views.databasetest, name='dbtest'),
    path('staff/', views.staff, name='staff'),
    path('staff/query', views.query, name ='query'),
    path('staff/query/display_export', views.display_export, name ='display_export'),
    path('import_data/',views.import_data, name='import_data'),
    path('import_data/display_import',views.display_import, name='display_import'),
     # ex: /sboapp/
    path('', views.indextest, name='indextest'),
    # ex: /sboapp/5/
    path('<sample_id>/', views.detail, name='detail'),
    # ex: /sboapp/5/vote/
    path('<sample_id>/vote/', views.vote, name='vote'),
]
