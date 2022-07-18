#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import xarray as xr 


# In[3]:


# 因为CAMS数据接口出现问题，这里直接用官网手动下载的2021/05/01-2021/05/31的数据进行测试，以计算AOT40。AOT40只有年度指标。

#直接打开数据
rdata = xr.open_dataset("ozonemay.nc")
rdata


# In[4]:


# # 纳秒单位换算成小时。不用了，直接把小时的个数拿来去算闰年与否
# rdataHour = rdata.time
# rdataHour.shape[0]
# 判断闰年与否
# if rdataHour.shape[0] == 4392:
#     rdataLeap = 1;
# else:
#     rdataLeap = 0;
# rdataLeap
# 读取五月-七月的数据

# 以上方法全部obsolete
# 直接下载五月份到七月份的三个月的数据，每天的小时只选择8:00-20:00的即可，不需要在代码里索引
# dataset读取后，直接进行作差

# 注意单位，CAMS下载的单位是µg m-3，但是AOT40的标准定义用的是40ppb，牢记 -> 40 ppb = 80 µg m-3
print(rdata.o3_conc.values)


# In[22]:


# 取正数，非正数部分全部直接划零而非删除，毕竟最后是求和，所以不影响终值
rdatapos = rdata.where(rdata>0,rdata,0)
print(rdatapos.o3_conc.values)


# In[19]:


# 直接求和
rdatasum = rdatapos.sum(dim=["time","level"]) 

# 理论上应该采用这个公式求和，而非只对time一个维度进行求和，尽管level维度是唯一值。只有这样最后的ndarray才是二维的，单纯的经纬度。
# rdatasum = rdatapos.sum(dim="time")
print(rdatasum.o3_conc.values)


# In[ ]:


# PLUS 分月份的代码 不过AOT40并不需要 先搁置
# 思路：鉴于CAMS的数据里的时间的单位都是纳秒，所以应该不能使用日历或者时间函数，需要自己进行分割。好在如果只考虑五六七月的数据，闰年的因素就无须考虑

