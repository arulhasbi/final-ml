import os
import json
import pickle
import pandas as pd
from django.shortcuts import render

# track variable change temporary
from final import config as glob

# make a home page
def home(request):
    param = request.GET.get('generate', '')
    if param == '':
        if glob.GENERATED_ == False:
            students = generateStudent()
            glob.COLUMNS_ = students["columns"]
            glob.RECORDS_ = students["records"]
            glob.AVG_SCORE_DATASCIENCE_ = students["avg_score_datascience"]
            glob.AVG_SCORE_BACKEND_ = students["avg_score_backend"]
            glob.AVG_SCORE_FRONTEND_ = students["avg_score_frontend"]
        else:
            pass
    else:
        if glob.GENERATED_ == False:
            students = generateRecommendation()
            glob.COLUMNS_ = students["columns"]
            glob.RECORDS_ = students["records"]
            glob.AVG_SCORE_DATASCIENCE_ = students["avg_score_datascience"]
            glob.AVG_SCORE_BACKEND_ = students["avg_score_backend"]
            glob.AVG_SCORE_FRONTEND_ = students["avg_score_frontend"]
            glob.GENERATED_ = True
        else:
            pass
    return render(request, 'index.html', {
        'ranges': [*range(0,3)],
        'columns': glob.COLUMNS_,
        'records': glob.RECORDS_,
        'avg_score_datascience': glob.AVG_SCORE_DATASCIENCE_,
        'avg_score_backend': glob.AVG_SCORE_BACKEND_,
        'avg_score_frontend': glob.AVG_SCORE_FRONTEND_,
        'is_generated': glob.GENERATED_
    })

# make a recommendation page
def recommendation(request):
    param = request.GET.get('label', '')
    courses = generateCourse(param)
    return render(request, 'recommendation.html', {
        'courses': courses
    })

# generate courses data
def generateCourse(param):
    courses = {
        5: [{
                "image": "https://images.unsplash.com/photo-1501526029524-a8ea952b15be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
                "title": "INTRO TO JAVASCRIPT",
                "lecturer": "Dr. Dene Lizette",
                "hours": 5
            }],
        2: [{
                "image": "https://images.unsplash.com/photo-1501526029524-a8ea952b15be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
                "title": "INTRO TO ANGULARJS",
                "lecturer": "Dr. Meridith Adena",
                "hours": 5
            }],
        4: [{
                "image": "https://images.unsplash.com/photo-1501526029524-a8ea952b15be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
                "title": "MACHINE LEARNING: AN INTRODUCTION",
                "lecturer": "Prof. Dr. Shaliza K",
                "hours": 5
            }],
        3: [{
                "image": "https://images.unsplash.com/photo-1501526029524-a8ea952b15be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
                "title": "PHP BASIC",
                "lecturer": "Dr. Greta Leanna",
                "hours": 5
            }],
        1: [{
                "image": "https://images.unsplash.com/photo-1496942299866-9e7ab403e614?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80",
                "title": "ARTIFICIAL INTELLIGENCE: AN INTRODUCTION",
                "lecturer": "Dr. Randi Jessamyn",
                "hours": 4
            }],
        0: [{
                "image": "https://images.unsplash.com/photo-1501526029524-a8ea952b15be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80",
                "title": "ML DEPLOYMENT: INTRO TO DJANGO",
                "lecturer": "Dr. Felicia Maya",
                "hours": 5
            }]
    }
    return courses[int(param)]

# generate students data
def generateStudent():
    dirname = os.path.dirname(__file__)
    # define file path to dataset
    datasetpath = os.path.join(dirname, "dataset/test-tortuga.csv")
    # read df
    df = pd.read_csv(datasetpath)
    # chunk the dataset
    columns = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND',	'AVG_SCORE_FRONTEND']].columns
    chunk = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND', 'AVG_SCORE_FRONTEND']].to_dict('records')
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

# generate recommendation
def generateRecommendation():
    from sklearn.preprocessing import StandardScaler
    dirname = os.path.dirname(__file__)
    # define file path to model
    modelpath = os.path.join(dirname, "mlp_model.sav")
    # read model
    model = pickle.load(open(modelpath, 'rb'))
    # define file path to dataset
    datasetpath = os.path.join(dirname, "dataset/test-tortuga.csv")
    # read df
    df = pd.read_csv(datasetpath)
    # rescaled the data
    ss = StandardScaler()
    rescaled_X = pd.DataFrame(data=ss.fit_transform(df.drop(["Unnamed: 0", "NAME", "USER_ID"], axis=1)), columns=df.drop(["Unnamed: 0", "NAME", "USER_ID"], axis=1).columns)
    # make prediction
    preds = model.predict(rescaled_X)
    # specify code for each profile
    profile_code = {
        5: 'beginner_front_end',
        2: 'advanced_front_end',
        4: 'beginner_data_science',
        3: 'beginner_backend',
        1: 'advanced_data_science',
        0: 'advanced_backend'
    }
    # concatenate the profile code
    df["PROFILE_CODE"] = preds
    # convert the prediction to string profile
    preds = [*map(lambda code: profile_code[code], preds)]
    # concatenate the profile string
    df["PROFILE"] = preds
    # chunk the dataset
    columns = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND',	'AVG_SCORE_FRONTEND', 'PROFILE']].columns
    chunk = df[['USER_ID', 'NAME', 'AVG_SCORE_DATASCIENCE', 'AVG_SCORE_BACKEND', 'AVG_SCORE_FRONTEND', 'PROFILE', 'PROFILE_CODE']].to_dict('records')
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
