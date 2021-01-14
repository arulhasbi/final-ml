from django.shortcuts import render
import os

# make a home page
def home(request):
    return render(request, 'index.html', {
        'ranges': range(2)
    })

# make a recommendation page
def recommendation(request):
    courses = generateCourse()
    return render(request, 'recommendation.html', {
        'courses': courses
    })

# generate courses data
def generateCourse():
    courses = [{
        "image": "https://images.unsplash.com/photo-1501526029524-a8ea952b15be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
        "title": "MACHINE LEARNING: AN INTRODUCTION",
        "lecturer": "Prof. Dr. Shaliza K",
        "hours": 5
    },
    {
        "image": "https://images.unsplash.com/photo-1496942299866-9e7ab403e614?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80",
        "title": "ARTIFICIAL INTELLIGENCE: AN INTRODUCTION",
        "lecturer": "Dr. Nilam N",
        "hours": 4
    }]
    return courses
