from matplotlib import colors

# Inspired from https://stackoverflow.com/questions/9707676/defining-a-discrete-colormap-for-imshow-in-matplotlib

# 1. Define a custom colormap, specifying the colors will be used. 

# There are only two colors (excluding white for no value or zero by default) in the output plot. So here we simply set two desired colors to present below or above the pollutant d_threshold.
# GoodColor refers to the color presenting the concentration of pollutant being below the threshold, while BadColor refers to the contrary. 
def ColorMap_Color(GoodColor, BadColor): 
    cmap = colors.ListedColormap([GoodColor,BadColor])
    return cmap

# 2. Define the bound of the colormap
# The bound defines how to map the values of concentration of pollutant to the corresponding color. (Zero or nan is default to white)
# Simply implement conditional statements to assign the corresponding concentration threshold value to normalize the colormap. 

def ColorMap_Threshold(ds_variable,d_timescale):
    if d_timescale == "Daily": 
        if ds_variable == 'nitrogen_dioxide':
            d_threshold = 25
        elif ds_variable == 'pm10_wildfires':
            d_threshold = 45
        elif ds_variable == 'nitrogen_monoxide':
            # not available?
            d_threshold = 0
        elif ds_variable == 'sulphur_dioxide':
            d_threshold = 40
        elif ds_variable == 'ozone':
            # set random to test, should be 100 instead
            d_threshold = 100
        elif ds_variable == 'carbon_monoxide':
            d_threshold = 4
        elif ds_variable == 'particulate_matter_2.5um':
            d_threshold = 15
    elif d_timescale == "Annual":
        if ds_variable == 'nitrogen_dioxide':
            d_threshold = 10
        elif ds_variable == 'pm10_wildfires':
            d_threshold = 15
        elif ds_variable == 'nitrogen_monoxide':
            # not available? 
            d_threshold = 0
        elif ds_variable == 'sulphur_dioxide':
            d_threshold = 40
        elif ds_variable == 'ozone':
            # only exists daily or peak season thresholds. Should do another conditional statement exclusively for ozone, in order to fetch the correct AQG. 
            d_threshold = 0
        elif ds_variable == 'carbon_monoxide':
            # only exists daily threshold
            d_threshold = 0
        elif ds_variable == 'particulate_matter_2.5um':
            d_threshold = 5
    else: 
        print("Neither 'Daily' nor 'Annual'!")
        return
    bounds=[0,d_threshold,1000]
    return bounds

# 3. Define the norm. 

def ColorMap_Norm(d_bounds,d_cmap):
    norm = colors.BoundaryNorm(d_bounds,d_cmap.N)
    return norm
