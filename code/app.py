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
import time
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import cdsapi
import xarray as xr 
import rioxarray
from shapely.geometry import mapping



# Create the application instance
app = Flask(__name__, template_folder="templates")

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template("home.html")


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
    data_list['pollutants'] = list(['carbon_monoxide','sulphur_dioxide','nitrogen_dioxide','ozone','particulate_matter_2','particulate_matter_10um','nitrogen_monoxide'])

    return Response(json.dumps(data_list), mimetype='application/json')

@app.route('/getProcessing')
def getProcessing():
    ds_variable = 'particulate_matter_2.5um'


    rdata = xr.open_dataset("data/download.nc")

    if ds_variable == 'nitrogen_dioxide':
        rdata_values = rdata.no2_conc.values
    elif ds_variable == 'particulate_matter_10um':
        rdata_values = rdata.pm10_conc.values
    elif ds_variable == 'nitrogen_monoxide':
        rdata_values = rdata.no_conc.values
    elif ds_variable == 'sulphur_dioxide':
        rdata_values = rdata.so2_conc.values
    elif ds_variable == 'ozone':
        rdata_values = rdata.o3_conc.values
    elif ds_variable == 'carbon_monoxide':
        rdata_values = rdata.co_conc.values
    elif ds_variable == 'particulate_matter_2.5um':
        rdata_values = rdata.pm2p5_conc.values
    
    if ds_variable == 'ozone':        
        h1 = np.mean(rdata_values[0:8,:,:,:], axis=0)
        h2 = np.mean(rdata_values[8:16,:,:,:], axis=0)
        h3 = np.mean(rdata_values[16:24,:,:,:], axis=0)
        max_mean = np.fmax(h1,h2,h3)
        mean_data =  max_mean    
    # For other pollutants, just simply calculate the mean values in one day. 
    else:
        mean_data = np.mean(rdata_values[:,:,:,:], axis=0)

    data_list = {}
    # data_list['mean_data'] = list(mean_data[0])
    latitude = rdata.latitude.values.astype("float64")
    longitude = rdata.longitude.values.astype("float64")

    pos=[]
    for lat in latitude:
        for lon in longitude:
            pos.append([lat,lon])
    data_list['pos'] = pos
    return Response(json.dumps(data_list), mimetype='application/json')

@app.route('/queryByNation')
def queryByNation():
    sdate = request.args.get('sdate')
    stime = request.args.get('stime')
    edate = request.args.get('edate')
    etime = request.args.get('etime')
    pollutants = request.args.get('pollutants')
    nation = request.args.get('nation')

    bounds = getNationBounds(nation) #5.867697	47.270114	15.04116	55.058165

    data = xr.open_dataset("data/download.nc")   
    latitude = data.latitude.values.astype("float64")
    longitude = data.longitude.values.astype("float64") 

    r2 = data.where(data.longitude > bounds.minx.values, drop=True)
    r3 = r2.where(r2.longitude < bounds.maxx.values, drop=True)
    r4 = r3.where(r3.latitude > bounds.miny.values, drop=True)
    rdata = r4.where(r4.latitude < bounds.maxy.values, drop=True)

    ds_variable = 'particulate_matter_2.5um'

    if ds_variable == 'nitrogen_dioxide':
        rdata_values = rdata.no2_conc.values
    elif ds_variable == 'particulate_matter_10um':
        rdata_values = rdata.pm10_conc.values
    elif ds_variable == 'nitrogen_monoxide':
        rdata_values = rdata.no_conc.values
    elif ds_variable == 'sulphur_dioxide':
        rdata_values = rdata.so2_conc.values
    elif ds_variable == 'ozone':
        rdata_values = rdata.o3_conc.values
    elif ds_variable == 'carbon_monoxide':
        rdata_values = rdata.co_conc.values
    elif ds_variable == 'particulate_matter_2.5um':
        rdata_values = rdata.pm2p5_conc.values
    
    if ds_variable == 'ozone':        
        h1 = np.mean(rdata_values[0:8,:,:,:], axis=0)
        h2 = np.mean(rdata_values[8:16,:,:,:], axis=0)
        h3 = np.mean(rdata_values[16:24,:,:,:], axis=0)
        max_mean = np.fmax(h1,h2,h3)
        mean_data =  max_mean    
    # For other pollutants, just simply calculate the mean values in one day. 
    else:
        mean_data = np.mean(rdata_values[:,:,:,:], axis=0)

    data_list = {}
    # data_list['mean_data'] = list(mean_data[0])
    latitude = rdata.latitude.values.astype("float64")
    longitude = rdata.longitude.values.astype("float64")

    pos=[]
    for lat in latitude:
        for lon in longitude:
            pos.append([lat,lon])
    data_list['pos'] = pos

    return Response(json.dumps(data_list), mimetype='application/json')


def getNationBounds(nation):
    code = nation
    data_dir = "data/"
    path_rg = data_dir + "NUTS_RG_01M_2021_4326_LEVL_0.shp"
    gdf_rg = gpd.read_file(path_rg)
    #gdf_rg.crs = "EPSG:4326"
    #gdf_rg = gdf.to_crs("EPSG:4326")
    gdf_nation = gdf_rg[gdf_rg.CNTR_CODE == code]
    bounds = gdf_nation.bounds

    return bounds















@app.route('/queryByNation2')
def queryByNation2():
    sdate = request.args.get('sdate')
    stime = request.args.get('stime')
    edate = request.args.get('edate')
    etime = request.args.get('etime')
    pollutants = request.args.get('pollutants')
    nation = request.args.get('nation')

    bounds = getNationBounds2(nation) #5.867697	47.270114	15.04116	55.058165

    data = xr.open_dataset("data/download.nc") 
    data.rio.write_crs("epsg:4326", inplace=True)
    # data["pm2p5_conc"][0].rio.to_raster('test.tif')
    data = data.assign_coords(longitude=(((data.longitude + 180) % 360) - 180)).sortby('longitude')  
    rdata = data.rio.clip(bounds,'epsg:4326',all_touched=False)

    ds_variable = 'particulate_matter_2.5um'

    if ds_variable == 'nitrogen_dioxide':
        rdata_values = rdata.no2_conc.values
    elif ds_variable == 'particulate_matter_10um':
        rdata_values = rdata.pm10_conc.values
    elif ds_variable == 'nitrogen_monoxide':
        rdata_values = rdata.no_conc.values
    elif ds_variable == 'sulphur_dioxide':
        rdata_values = rdata.so2_conc.values
    elif ds_variable == 'ozone':
        rdata_values = rdata.o3_conc.values
    elif ds_variable == 'carbon_monoxide':
        rdata_values = rdata.co_conc.values
    elif ds_variable == 'particulate_matter_2.5um':
        rdata_values = rdata.pm2p5_conc.values
    
    if ds_variable == 'ozone':        
        h1 = np.mean(rdata_values[0:8,:,:,:], axis=0)
        h2 = np.mean(rdata_values[8:16,:,:,:], axis=0)
        h3 = np.mean(rdata_values[16:24,:,:,:], axis=0)
        max_mean = np.fmax(h1,h2,h3)
        mean_data =  max_mean    
    # For other pollutants, just simply calculate the mean values in one day. 
    else:
        mean_data = np.mean(rdata_values[:,:,:,:], axis=0)

    data_list = {}
    # data_list['mean_data'] = list(mean_data[0])
    latitude = rdata.latitude.values.astype("float64")
    longitude = rdata.longitude.values.astype("float64")

    pos=[]
    for lat in latitude:
        for lon in longitude:
            pos.append([lat,lon])
    data_list['pos'] = pos

    final_data= 100
    data_list['meandata'] = final_data



    return Response(json.dumps(data_list), mimetype='application/json')


def getNationBounds2(nation):
    code = nation
    data_dir = "data/"
    path_rg = data_dir + "NUTS_RG_01M_2021_4326_LEVL_0.shp"
    gdf_rg = gpd.read_file(path_rg)
    gdf_rg.crs = "EPSG:4326"
    #gdf_rg = gdf.to_crs("EPSG:4326")
    gdf_nation = gdf_rg[gdf_rg.CNTR_CODE == code]
    bounds = gdf_nation.geometry.apply(mapping)

    return bounds



if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        debug=True)
