from django.shortcuts import render
import os

# make a home page
def home(request):
    return render(request, 'index.html', {
        'range': range(1)
    })
