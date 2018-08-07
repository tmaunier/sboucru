"""
Oxford University Clinical Research Unit
Serum bank manager
MIT License
Copyright (c) 2018 tmaunier
link : https://github.com/tmaunier/sboucru
Written by Tristan Maunier
Bioinformatics Master Degree - University of Bordeaux, France
"""

from django.shortcuts import render


def home(request):
    return render (request, "pages/home.html")

def about(request):
    return render (request, "pages/about.html")
