# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:52:38 2021

@author: Group 1
"""
#!/usr/bin/python
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    Response,
    flash,
    jsonify
)
import os
import time
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import cdsapi
import xarray as xr
import rioxarray
from shapely.geometry import mapping
import getMean


# Create the application instance
app = Flask(__name__, template_folder="templates")

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/getBasicInfo')
def getBasicInfo():
    # carbon_monoxide --> co_conc
    # sulphur_dioxide --> so2_conc
    # nitrogen_dioxide --> no2_conc
    # ozone --> o3_conc
    # particulate_matter_2.5um --> pm2p5_conc
    # particulate_matter_10um  -->  pm10_conc
    # nitrogen_monoxide --> no_conc

    data_list = {}
    data_list['pollutants'] = list(['carbon_monoxide', 'sulphur_dioxide', 'nitrogen_dioxide',
                                   'ozone', 'particulate_matter_2', 'particulate_matter_10um', 'nitrogen_monoxide', 'song'])

    return Response(json.dumps(data_list), mimetype='application/json')

@app.route('/queryByNation')
def queryByNation():
    sdate = request.args.get('sdate')
    edate = request.args.get('edate')
    pollutants = request.args.get('pollutants')
    nation = request.args.get('nation')

    # 5.867697	47.270114	15.04116	55.058165
    # bounds is shape of the country, area is the four bounds of the country in rectangle
    [bounds, area] = getNationBounds(nation)
    capitalCoor = getCapitalCoordinates(nation)
    NWSE_area = [list(area.maxy.values)[0], list(area.minx.values)[
        0], list(area.miny.values)[0], list(area.maxx.values)[0]]

    mean_data = getRawData(NWSE_area, bounds,pollutants)
    #pd.DataFrame(mean_data).to_csv("clipped23.csv")
    mean_country = np.nanmean(mean_data)
    myColor = getColor(pollutants, mean_country)

    data_list = {}
    data_list['meandata'] = mean_country.tolist()
    data_list['capitalCoor'] = capitalCoor
    data_list['circle_color'] = myColor

    return Response(json.dumps(data_list), mimetype='application/json')

def getColor(pollutants, mean_country):
    ds_variable = pollutants
    ds_value = mean_country

    if ds_variable == 'nitrogen_dioxide':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'
    elif ds_variable == 'particulate_matter_10um':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'
    elif ds_variable == 'nitrogen_monoxide':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'
    elif ds_variable == 'sulphur_dioxide':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'
    elif ds_variable == 'ozone':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'
    elif ds_variable == 'carbon_monoxide':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'
    elif ds_variable == 'particulate_matter_2.5um':
        if mean_country > 100:
            myColor = 'red'
        else:
            myColor = 'green'

    return myColor

def getNationBounds(nation):
    code = nation
    data_dir = "data/"
    path_rg = data_dir + "NUTS_RG_01M_2021_4326_LEVL_0.shp"
    gdf_rg = gpd.read_file(path_rg)
    gdf_rg.crs = "EPSG:4326"
    #gdf_rg = gdf.to_crs("EPSG:4326")
    gdf_nation = gdf_rg[gdf_rg.CNTR_CODE == code]
    area = gdf_nation.bounds
    bounds = gdf_nation.geometry.apply(mapping)

    return bounds, area


def getCapitalCoordinates(nation):
    code = nation
    path_lb = "data/NUTS_LB_2021_4326_LEVL_0.shp"
    gdf_lb = gpd.read_file(path_lb)
    gdf_lb.crs = "EPSG:4326"
    gdf_nation = gdf_lb[gdf_lb.CNTR_CODE == code]
    capital = gdf_nation.geometry  # .apply(mapping)
    capitalCoor = [capital.y.values[0], capital.x.values[0]]

    return capitalCoor


def getRawData(NWSE_area, bounds,pollutants):
    ds_name = 'cams-europe-air-quality-forecasts'
    ds_time = '2022-01-01/2022-01-01'
    ds_variable = pollutants
    ds_area = NWSE_area
    ds_bounds = bounds

    [mean_data,fName] = getMean.get_mean(
        ds_name=ds_name, ds_time=ds_time, ds_variable=ds_variable, ds_area=ds_area, ds_bounds=ds_bounds)
    
    if os.path.exists(fName):
        os.remove(fName)

    return mean_data





if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        debug=True)
