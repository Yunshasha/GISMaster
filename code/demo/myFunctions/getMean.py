import cdsapi
import numpy as np
import pandas as pd
import xarray as xr

# 获取原始数据 采用不同的方法
# nitrogen_dioxide --> no2_conc   
# particulate_matter_10um  -->  pm10_conc 
# nitrogen_monoxide --> no_conc
# sulphur_dioxide --> so2_conc
# ozone --> o3_conc
# carbon_monoxide --> co_conc
# particulate_matter_2.5um --> pm2p5_conc
def get_mean(ds_name, ds_time, ds_variable):

    c = cdsapi.Client()
    c.retrieve(
        ds_name,
        {
            'model': 'ensemble',
            'date': ds_time,
            'format': 'netcdf',
            'variable': ds_variable,
            'level': '0',
            'type': 'analysis',
            'leadtime_hour': '0',
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
        },
        'download.nc')
    # 打开数据到 rdata
    rdata = xr.open_dataset("download.nc")
    # rdata

    # 获取原始数据 采用不同的方法
    # nitrogen_dioxide --> no2_conc   
    # particulate_matter_10um  -->  pm10_conc 
    # nitrogen_monoxide --> no_conc
    # sulphur_dioxide --> so2_conc
    # ozone --> o3_conc
    # carbon_monoxide --> co_conc
    # particulate_matter_2.5um --> pm2p5_conc

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
    else:
        # 拿到 原始数据 的 values array 信息
        # rdata_values
        mean_data = np.mean(rdata_values[:,:,:,:], axis=0)
        latitude = rdata.latitude.values
        longitude = rdata.longitude.values


    return [mean_data, latitude, longitude, rdata]

