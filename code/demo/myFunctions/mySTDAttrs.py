from datetime import date, datetime
import xarray as xr
import pandas as pd
import numpy as np
from numpy import datetime64

# Standardize time from nanosecond to datetime64
def TimetoDate64(rdata):
    timestamp = rdata.time.long_name[19:27]
    timestamp_ini = datetime.strptime(timestamp,"%Y%m%d")
    time_coords = pd.date_range(timestamp_ini,periods=len(rdata.time),freq='h').strftime("%Y%m%d %H:%M:%S").astype("timedate64[ns]")
    # Return a pandas DateTimeIndex. Then dataset.assign_coords() should be used to overwrite coordinate of original dataset. 
    return time_coords

# Standardize longitude from 0-360 to (-180)-180
def Lon360to180(rdata):
    longitude = (rdata.longitude + 180) % 360 - 180
    longitude = longitude.sortby('longtitude')
    #Return a DataArray. Then dataset.assign_coords() should be used to overwrite coordinate of original dataset. 
    return longitude

# Transfer the attributes of variable from original dataset to the current dataset. This is used when current dataset is generated from original dataset by performing mathematic computation. Don't forget that after using this function, usually it is also required to rename mannualy again the name or the unit. 
# In most cases, this function is just used to simply copy identical attributes from original dataset to current dataset. 

# No need to build a function. Just do like this: (Ditionary copy)
# rdata.o3_aot.attrs = rdata.o3_conc.attrs.copy()
