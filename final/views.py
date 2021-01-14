from django.shortcuts import render
import pandas as pd
import os

# make a home page
def home(request):
    students = generateStudent()
    return render(request, 'index.html', {
        'ranges': range(4),
        'columns': students["columns"],
        'records': students["records"]
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

# generate students data
def generateStudent():
    dirname = os.path.dirname(__file__)
    datasetpath = os.path.join(os.path.dirname(__file__), "dataset/train-tortuga.csv")

    df = pd.read_csv(datasetpath)
    columns = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND',	'AVG_SCORE_FRONTEND', 'PROFILE']].columns

    chunk = df[columns].head(5).to_dict('records')

    print(chunk)

    payload = {
        "columns": columns,
        "records": chunk
    }

    return payload
