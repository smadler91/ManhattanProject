"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from FinalProject_Matan_Michal import app
import csv
import math



@app.route('/')
@app.route('/home')
def home():
    """
        Serve first page
    """
    return render_template('FirstPage.html')

@app.route('/getjson')
def getJson():
    """
        Received: None
        Returned: JSON
    """
    return  jsonify(username="MEME",email="example@email.com")


@app.route('/getname', methods=['POST'])
def getName():
    """
        Received: JSON
        Returned: String - the json field 'name' is returned back
    """
    x = request.values
    return x['name']


@app.route('/getNearestBusiness', methods=['POST'])
def getNearestBusiness():
    """
        Received: JSON of user's location (lat, lon).
        Returned: JSON of nearest business's location (lat, lon).
    """
    userLocation = request.values
    userLat = float(userLocation['Lat'])
    userLon = float(userLocation['Lon'])
    latCor, lonCor = SearchClosePOI(userLat, userLon)
    return  jsonify(Lat=latCor, Lon=lonCor)

def distfunction(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon1 - lon2

    EARTH_R = 6372.8

    y = math.sqrt((math.cos(lat2) * math.sin(dlon)) ** 2+ (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)) ** 2)
    x = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(dlon)
    c = math.atan2(y, x)
    return EARTH_R * c

def SearchClosePOI(latP, lonP):
    '''
        Importing Business data
    '''

    lat_data = []
    lon_data = []    
    with open(r'F:\Eli Safra Course\FinalProject_Matan_Michal\FinalProject_Matan_Michal\FinalProject_Matan_Michal\static\databases\POIs.csv') as csvfile:
        POIs_CSV = csv.reader(csvfile, delimiter=',')
        for POI in POIs_CSV:
            if (POI[0] == 'X'):  # header
                continue
            else:
                if (POI[0] != ""):
                    X = float(POI[0])
                    Y = float(POI[1])
                    name = POI[2]
                    id = int(POI[3])
                    Popularity = int(POI[4])
                    lat_data.append(X)
                    lon_data.append(Y)

    #  initialize:
    MinD = distfunction(lat_data[0], lon_data[0], latP, lonP)
    flagP = 0
    for i in range(len(lat_data)):
        chk = distfunction(lat_data[i], lon_data[i], latP, lonP)
        if (chk < MinD) :
            MinD = chk
            flagP = i

    return lat_data[flagP], lon_data[flagP]


@app.route('/getAllBusinesses')
def getAllBusinesses():
    #pois = [[11,12,13,14],[21,12,13,14],[31,12,13,14]]
    #return jsonify(POIs=pois,name='me')

    pois_list = []  # [List<JSON>]
    with open(r'F:\Eli Safra Course\FinalProject_Matan_Michal\FinalProject_Matan_Michal\FinalProject_Matan_Michal\static\databases\POIs.csv') as csvfile:
        POIs_CSV = csv.reader(csvfile, delimiter=',')
        for POI in POIs_CSV:
            if (POI[0] == 'X'):  # header
                continue
            else:
                if (POI[0] != ""):
                    lat = POI[0]
                    lon = POI[1]
                    name = POI[2]
                    id = POI[3]
                    popularity = POI[4]
                    type = POI[5]
                    pois_list.append([lat, lon, name, id, popularity, type])
    return jsonify(POIs=pois_list)
