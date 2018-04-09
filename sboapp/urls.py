from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('dbtest/',views.databasetest, name='dbtest'),

     # ex: /sboapp/
    path('', views.indextest, name='indextest'),
    # ex: /sboapp/5/
    path('<int:local_sample_id>/', views.detail, name='detail'),
    # ex: /sboapp/5/results/
    path('<int:local_sample_id>/results/', views.results, name='results'),
    # ex: /sboapp/5/vote/
    path('<int:local_sample_id>/vote/', views.vote, name='vote'),
]
