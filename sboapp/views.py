from django.shortcuts import render #render is mainly used with templates while HttpResponse is used for data (for example)
from django.http import HttpResponse
from sboapp.models import Serum, Site, Ward, Freezer
from django.db.models import Count


# Create your views here.

def index(request):
    return render (request, "sboapp/pages/index.html")


def databasetest(request):
    dataserum = Serum.objects.all()
    datasite = Site.objects.all()
    dataward = Ward.objects.all()
    datafreezer = Freezer.objects.all()
    args = {"serum_nb": dataserum,"site_nb": datasite,"ward_nb": dataward,"freezer_nb": datafreezer}
    return render (request, "sboapp/pages/databasetest.html", args)

def detail(request, local_sample_id):
    return HttpResponse("You're looking at serum %s." % local_sample_id)

def results(request, local_sample_id):
    s = Site.objects.filter(serum__local_sample_id__exact='1')
    output = "You're looking at the site of serum %s ->".join('s')
    return HttpResponse(output % local_sample_id)

def vote(request, local_sample_id):
    return HttpResponse("You're voting on serum %s." % local_sample_id)

def indextest(request):
    first_3_serum = Serum.objects.order_by('local_sample_id')[:3]
    note = 'Here are the first 3 serum added on the database: \n '
    output = ', '.join([s.sample_id for s in first_3_serum])
    return HttpResponse(note + output)
