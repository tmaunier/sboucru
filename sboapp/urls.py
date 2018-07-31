from django.urls import path, reverse_lazy


from . import views
from django.contrib.auth import views as auth_views


app_name = "sboapp"

urlpatterns = [
        #Staff dashboard
    path('staff/', views.staff, name='staff'),
    path('staff/edit_profile',views.edit_profile, name='edit_profile'),
    path('staff/edit_profile/change_password',views.change_password, name='change_password'),
    path('staff/edit_profile/change_profile',views.change_profile, name='change_profile'),
    # path('staff/password_change/',auth_views.PasswordChangeView.as_view(success_url='sboapp/staff/password_change_done'), name='password_change'),
    # path('staff/password_change/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('sboapp:staff/password_change_done')), name='password_change'),
        #Import data
    path('staff/import_serum/',views.import_serum, name='import_serum'),
    path('staff/import_location/',views.import_location, name='import_location'),
    path('staff/import_elisa_choices',views.import_elisa_choices, name='import_elisa_choices'),
    path('staff/import_elisa/Chikungunya',views.import_chik_elisa, name='import_chik_elisa'),
    path('staff/import_elisa/Dengue',views.import_dengue_elisa, name='import_dengue_elisa'),
    path('staff/import_elisa/Rickettsia',views.import_rickettsia_elisa, name='import_rickettsia_elisa'),
    path('staff/import_pma',views.import_pma, name='import_pma'),
        #Undo Import
    path('staff/undo_import',views.undo_import, name='undo_import'),
    path('staff/undo_import/delete_import',views.delete_import, name='delete_import'),
        #Modify Location
    path('staff/modify_location',views.modify_location, name='modify_location'),
        #Modify Status
    path('staff/modify_status',views.modify_status, name='modify_status'),
        #Query + Export
    path('staff/sort_data', views.sort_data, name ='sort_data'),
    path('staff/sort_data/check_status', views.check_status, name ='check_status'),
    path('staff/sort_data/count_results', views.count_results, name ='count_results'),
    path('staff/sort_data/display_export', views.display_export, name ='display_export'),
        #Display Tables
    path('staff/tables/',views.display_tables, name='tables'),

    #Delete this with the corresponding view once you import the whole db
    path('staff/init_elisa',views.init_elisa, name='init_elisa')
]
