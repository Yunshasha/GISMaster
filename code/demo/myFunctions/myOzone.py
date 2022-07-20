import numpy as np
import pandas as pd
import xarray as xr 

# Currently rdata is supposed to contain only data from May to July, and for each day in this period only contains data from 8:00 to 20:00. 
# To-do: Instead of limiting the time period and hours of input data, it is advised to use index and slice to retrieve a subset for AOT40 calculation. But at this momemnt, it is unnecessary, since it is easier to just define the time period and hours when querying data through API, as well as for annual values there don't exist lots of options for users to choose. 
def aotOzone(rdata):
    # Check if the dataset has variable O3. This condition is experimental. Here use dict.get() to check 'title' in Attributes of dataset. 
    if rdata.attrs.get('title')[0:2] == 'O3':
        odata = rdata / 2
        odata = odata - 40
        odata = xr.where(odata>0,odata,0)
        odata = odata.sum(dim=['time','level'])
        odata.o3_conc.attrs = {{'species': 'Ozone','units':'ppb','value': 'AOT40 value','standard_name': rdata.o3_conc.standard_name}}
        # Return a dataset. Then use this dataset to plot aot40, instead of using raw data. 
        return odata
    else:
        print("Input dataset must only contain O3")
        return

# Currently the minimum unit of time period of input dataset is one day. 
# In order to calculate the daily average value of ozone, it is required at least to download data of two days. Therefore, the time period of downloaded data is always one day greater than the time period defined by the user, which also indicates that the users are not allowed to choose yesterday or today as part of input dataset. 
def dailyOzone(rdata):
    days = rdata.time.count().values/24 - 1 # The last day can only be used to calculate the daily average value of ozone of the second last day. 

    # Create a dataset to save the final daily average value of ozone. 
    dmax = xr.DataArray(
        np.zeros((len(rdata.longitude),len(rdata.latitude),days)),
            [   
            ("longitude",rdata.longitude.values),
            ("latitude",rdata.latitude.values)
            ("days",np.arrange(days))
            ]
        )
    # The name of the variable in dmax is temporarily defined as the same of ozone dataset. This is useful in the following loop section. 
    dmax = dmax.to_dataset(name="o3_conc")

    # Check if the dataset has variable O3. This condition is experimental. 
    if rdata.attrs.get('title')[0:2] == 'O3':

        # Go through each day
        for i in range(0,days,1):

            # Get hours from 7:00 to 6:00 in the next day
            odata = rdata.isel(time=slice(7+24*i,31+24*i))

            # # Currently we don't consider the case where there is missing value
            # odatacheck = odata.isnull()
            # if odatacheck.o3_conc.values.sum() == 0: 

            # Go through each hour from 7:00 to 23:00 in one day
            for j in range(7,24,1):
                dmean = rdata.isel(time=slice(j,j+8)).mean(dim=['time','level'])
                dmax.loc[dict(days=i)] = np.fmax(dmax.loc[dict(days=i)],dmean)

        # Copy the attributes from original dataset. Then rename the name of variable. 
        dmax.o3_conc.attrs = {'species': 'Ozone','units':'μg/m3','value': 'daily highest 8-hour value','standard_name': rdata.o3_conc.standard_name}
        dmax = dmax.rename({'o3_conc': 'o3_daily_highest8'})

        # Return a dataset. Then use this dataset to plot daily average value of ozone, instead of using raw data. 
        return dmax
    else: 
        print("Input dataset must only contain O3")
        return