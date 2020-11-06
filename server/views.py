from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect,FileResponse
from server import models
import json
import uuid
from roadMapMatching.RoadMapMatching import filePoints
from roadMapMatching.RoadMapMatching import oriTra
import os

def to_json1(df,orient='split'):
    df_json = df.to_json(orient=orient , force_ascii=False)
    return json.loads(df_json)

def write_server(request):
    ajax = request.GET
    res = {
        'success':True
    }
    return JsonResponse(res)

# Create your views here.
def file_server(request):
    filename = 'roadMapMatching/DriveTrajectories/粤B2BB25_11556.csv'
    networkstuff = 'roadMapMatching/RoadNetWork/shenzhen-drive-20200813.osm'
    result =filePoints(networkstuff , filename)
    sdf = oriTra(filename)
    raw = sdf['rawpairs']
    ori = sdf['oripairs']
    res = [raw,ori,[result]]
    json_res = json.dumps(res)
    return JsonResponse(json_res , safe=False)
    # 一次相应15s左右
def get_setlist(request):
    filepath = 'roadMapMatching/DriveTrajectories/'
    dirs = os.listdir(filepath)
    res = {
        'datalist' : dirs
    }
    return JsonResponse(res)
def road_map_matching(request):
    print(request.body)
    thefilename = json.loads(request.body,encoding='utf-8')
    print(thefilename)
    filename = 'roadMapMatching/DriveTrajectories/' + thefilename['datasets']
    print(filename)
    networkstuff = 'roadMapMatching/RoadNetWork/shenzhen-drive-20200813.osm'
    result =filePoints(networkstuff , filename)
    sdf = oriTra(filename)
    raw = sdf['rawpairs']   
    ori = sdf['oripairs']
    res = [raw,ori,[result]]
    json_res = json.dumps(res)
    return JsonResponse(json_res , safe=False)

file_server("sdfas")