from django.shortcuts import render
import pandas as pd
import os
import json

# track variable change temporary
from final import config as glob

# make a home page
def home(request):
    param = request.GET.get('generate', '')
    if not (param == '' and glob.GENERATED_ == False):
        students = generateStudent()
        glob.COLUMNS_ = students["columns"]
        glob.RECORDS_ = students["records"]
        glob.AVG_SCORE_DATASCIENCE_ = students["avg_score_datascience"]
        glob.AVG_SCORE_BACKEND_ = students["avg_score_backend"]
        glob.AVG_SCORE_FRONTEND_ = students["avg_score_frontend"]
    else:
        pass
    return render(request, 'index.html', {
        'ranges': [*range(0,3)],
        'columns': glob.COLUMNS_,
        'records': glob.RECORDS_,
        'avg_score_datascience': glob.AVG_SCORE_DATASCIENCE_,
        'avg_score_backend': glob.AVG_SCORE_BACKEND_,
        'avg_score_frontend': glob.AVG_SCORE_FRONTEND_
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
    # define file path to dataset
    dirname = os.path.dirname(__file__)
    datasetpath = os.path.join(os.path.dirname(__file__), "dataset/train-tortuga.csv")
    # read df
    df = pd.read_csv(datasetpath)
    # encode students' profile
    df["PROFILE_CODE"] = df['PROFILE'].apply(profileCoding)
    # drop if a record has a null value
    df.dropna(inplace=True)
    # chunk the dataset
    columns = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND',	'AVG_SCORE_FRONTEND', 'PROFILE']].columns
    chunk = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND', 'AVG_SCORE_FRONTEND', 'PROFILE', 'PROFILE_CODE']].head(50).to_dict('records')
    # encode students' average score for every subject
    datascience = json.dumps(df['AVG_SCORE_DATASCIENCE'].tolist())
    backend = json.dumps(df['AVG_SCORE_BACKEND'].tolist())
    frontend = json.dumps(df['AVG_SCORE_FRONTEND'].tolist())
    # define the payload
    payload = {
        "columns": columns,
        "records": chunk,
        "avg_score_datascience": datascience,
        "avg_score_backend": backend,
        "avg_score_frontend": frontend
    }
    return payload

# encoding students' profile code
def profileCoding(profile):
    split_by__ = profile.split("_")
    level =  split_by__[0]
    if level == "advanced":
        return 1
    else:
        return 0

# encoding students' average score for every subject -> for radial histogram
def avgEncoding(dataframe, subject):
    return pd.DataFrame(data=dataframe[subject].value_counts()).reset_index().rename(columns={
                "index": "category",
                subject: "value"
            }).to_dict("records")
