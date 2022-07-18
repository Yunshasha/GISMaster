#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import xarray as xr 


# In[3]:


# 因为CAMS数据接口出现问题，这里直接用官网手动下载的2021/05/01-2021/05/02的数据。

#直接打开数据
rdata = xr.open_dataset("ozone2days.nc")
rdata


# In[4]:


# 只选取前两天的数据，用这些数据计算第一天的daily maximum average
rdata = rdata.isel(time=slice(0,49))
# 注意左开右闭
print(rdata.time)
# 这样就得到了一个subset，只包含原始数据集中前两天的数据。不过代码中使用的本地数据已经是只包含五月前两天的数据。
rdata.o3_conc.values


# In[5]:


# 将原始数据的纳秒换算成小时以便于计算
# rdata.assign_coords(time=rdata.time/3600000000000)

# 不需要这一步，直接按照自然数列读取时间就行，纳秒只是数据存储的形式而已


# In[6]:


# 检查是否含有空数据
rdatacheck = rdata.isnull()
# 通过求和判断有多少个空数据
rdatacheck.o3_conc.values.sum()
# 如果有的话，需要额外的操作，这里先不管


# In[24]:


#从7:00到23:00每个小时都要计算一次平均值。计算方法是将该小时和后续七小时的数据求平均值。目前不考虑nan的情况
# 这里只求一天的指标，所以时间轴和高度轴都不需要了，直接用原始数据的经纬度和任意的臭氧浓度组成一个新的dataset（直接xr.dataset建立也可，但比较麻烦因为经纬度得额外写一段代码）
# dmax = np.zeros([700,420])
dmax = xr.DataArray(
    np.zeros((700,420)),
    [
        ("longitude",rdata.longitude.values),
        ("latitude",rdata.latitude.values),
    ]
)
dmax = dmax.to_dataset(name="o3_conc")
print(dmax)

for i in range(7,24,1):
    dmean = rdata.isel(time=slice(i,i+9)).mean(dim=['time','level'])
    dmax = np.fmax(dmax,dmean)
    print("turn" + str(i))
    # print(dmax)

dmax = dmax.rename({'o3_conc': 'highest8'})
print(dmax)

# 方法1
#对于每个点，依次计算出7:00-23:00每小时的8h均值，然后选出最大的放到o3_con里（替代o3_con；记得最后重命名维度一下）

# for x in range(0,700):
#     for y in range(0,420):
#         dmax = 0
#         for i in range(7,24,1):
#             dmean = rdata.isel(time=slice(i,i+9),longitude=x,latitude=y).mean(dim=['time','level'])
#             # print(dmean)
#             if dmax < dmean:
#                 dmax = dmean
#         ddata.where(ddata.isel(longitude=x,latitude=y),dmax)

# 方法2
# 依次求出每小时对应的8h平均值，然后每个经纬点依次遍历选出最大的。

# for i in range(7,24,1):
#     dmean = rdata.isel(time=slice(i,i+9)).mean(dim=['time','level'])
#     # print("turn" + str(i))
#     # print(dmean)
#     # 最大值比较
#     for x in range(0,700):
#         for y in range(0,420):
#             # print(dmax[x,y])
#             # print(dmean.isel(longitude=x,latitude=y).o3_conc.values)
#             if dmax[x,y] < dmean.isel(longitude=x,latitude=y).o3_conc.values:
#                 dmax[x,y] = dmean.isel(longitude=x,latitude=y).o3_conc.values

# print(dmax)

# ddata = xr.where(ddata.time==slice(i,i+9),dmean,ddata)


# In[26]:


# 2.00 µg/m3 = 1 ppb
dmax = dmax / 2
dmax


# In[27]:


# 1 ppb = 0.001 ppm
dmax = dmax / 1000
dmax


# In[25]:


# Concentration to AQI: https://forum.airnowtech.org/t/the-aqi-equation/169
dAQI = dmax
dAQI = dAQI.rename({'highest8': 'AQI'})

for x in range(0,700):
    for y in range(0,420):
        point = dmax.isel(longitude=x,latitude=y).highest8.values
        if point>0 and point<0.055
        dAQI[dict(longitude=x,latitude=y)] = (50-0)



# In[ ]:




