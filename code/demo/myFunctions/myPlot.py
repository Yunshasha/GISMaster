import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.cm import get_cmap
from matplotlib.axes import Axes
from matplotlib import colors

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature

from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh

# There are only two colors (excluding white for no value or zero by default) in the output plot. So here we simply set two desired colors to present below or above the pollutant threshold.
# GoodColor refers to the color presenting the concentration of pollutant being below the threshold, while BadColor refers to the contrary. 
# The input are both strings. 
def plot_ColorMap(GoodColor, BadColor): 
    cmap = colors.ListedColormap([GoodColor,BadColor])
    return cmap

def plot_Threshold(ds_variable,d_timescale):
    if d_timescale == "Daily": 
        if ds_variable == 'nitrogen_dioxide':
            d_threshold = 25
        elif ds_variable == 'particulate_matter_10um':
            d_threshold = 45
       
        elif ds_variable == 'sulphur_dioxide':
            d_threshold = 40    
           
        elif ds_variable == 'ozone':
            print("daily timescale is not available for ozone. ")
            return
        elif ds_variable == 'carbon_monoxide':
            d_threshold = 4000
        elif ds_variable == 'particulate_matter_2.5um':
            d_threshold = 15
    elif d_timescale == "Annual":
        if ds_variable == 'nitrogen_dioxide':
            d_threshold = 10
        elif ds_variable == 'particulate_matter_10um':
            d_threshold = 15
        elif ds_variable == 'particulate_matter_2.5um':
            d_threshold = 5
        
        elif ds_variable == 'sulphur_dioxide':
            print("Annual timescale is not available for sulphur dioxide. ")
            return
        elif ds_variable == 'ozone':
            print("Annual timescale is not available for ozone. ")
            return 
        elif ds_variable == 'carbon_monoxide':
            # only exists daily threshold
            print("Annual timescale is not available for carbon monoxide. ")
            return 
        
    else: 
        print("Neither 'Daily' nor 'Annual'!")
        return
    return d_threshold

def plot_Final(data_array, longitude, latitude, projection, color_scale, unit, long_name, vmin, vmax, threshold,
                         set_global=True, lonmin=-180, lonmax=180, latmin=-90, latmax=90, GoodColor='Green', BadColor='Red',):
    """ 
    Visualizes a xarray.DataArray with matplotlib's pcolormesh function.
    
    Parameters:
        data_array(xarray.DataArray): xarray.DataArray holding the data values
        longitude(xarray.DataArray): xarray.DataArray holding the longitude values
        latitude(xarray.DataArray): xarray.DataArray holding the latitude values
        projection(str): a projection provided by the cartopy library, e.g. ccrs.PlateCarree()
        color_scale(str): string taken from matplotlib's color ramp reference
        unit(str): the unit of the parameter, taken from the NetCDF file if possible
        long_name(str): long name of the parameter, taken from the NetCDF file if possible
        vmin(int): minimum number on visualisation legend
        vmax(int): maximum number on visualisation legend
        set_global(boolean): optional kwarg, default is True
        lonmin,lonmax,latmin,latmax(float): optional kwarg, set geographic extent is set_global kwarg is set to 
                                            False

    """
    fig=plt.figure(figsize=(20, 10))

    ax = plt.axes(projection=projection)
   
    # img = plt.pcolormesh(longitude, latitude, data_array, 
    #                     cmap=plt.get_cmap(color_scale), transform=ccrs.PlateCarree(),
    #                     vmin=vmin,
    #                     vmax=vmax,
    #                     shading='auto')

    img = plt.pcolormesh(longitude, latitude, data_array, 
                    cmap=colors.ListedColormap([GoodColor,BadColor]), transform=ccrs.PlateCarree(),
                    norm=colors.BoundaryNorm([vmin,threshold,vmax],colors.ListedColormap([GoodColor,BadColor]).N),
                    shading='auto'
                    )

    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=1)
    ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=1)

    if (projection==ccrs.PlateCarree()):
        ax.set_extent([lonmin, lonmax, latmin, latmax], projection)
        gl = ax.gridlines(draw_labels=True, linestyle='--')
        gl.top_labels=False
        gl.right_labels=False
        gl.xformatter=LONGITUDE_FORMATTER
        gl.yformatter=LATITUDE_FORMATTER
        gl.xlabel_style={'size':14}
        gl.ylabel_style={'size':14}

    if(set_global):
        ax.set_global()
        ax.gridlines()

    cbar = fig.colorbar(img, ax=ax, orientation='horizontal', fraction=0.04, pad=0.1)
    cbar.set_label(unit, fontsize=16)
    cbar.ax.tick_params(labelsize=14)
    ax.set_title(long_name, fontsize=20, pad=20.0)

 #   plt.show()
    return fig, ax
