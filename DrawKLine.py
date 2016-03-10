# -*- coding: utf-8 -*-
import sys
import pickle
import math
import datetime
import matplotlib
from pandas import Series , DataFrame
import pandas as pd
#matplotlib.use("WXAgg", warn=True)

import matplotlib.pyplot as pyplot
import numpy
from matplotlib.ticker import FixedLocator, MultipleLocator, LogLocator, FuncFormatter, NullFormatter, LogFormatter

def Plot(pfile, figpath, useexpo=False):
    #fileobj= open(name=pfile, mode='rb')
    #pdata= pickle.load(fileobj)
    #fileobj.close()
    
    
    data = pd.read_table('C:\\Users\\van\\Desktop\\KLineData\\cyb\\300004.txt' , sep=' ' , names=['date' , 'open' , 'high' , 'low' , 'close' , 'value' , 'vol' , 'change'])
    pdata = data.dropna(how='all')
    print pdata.ix[1]
    length= len(pdata[u'date'])
    
    highest_price= max(pdata[u'high'])
    lowest_price= min( [plow for plow in pdata[u'low'] if plow != None] )
    
    
    yhighlim_price=round(highest_price)
    ylowlim_price=round(lowest_price)
    
    xfactor= length/100/230.0 
    yfactor= 0.3

    if useexpo:
        expbase= 1.1
        if ylowlim_price != 0:
            ymulti_price= math.log(yhighlim_price, expbase) - math.log(ylowlim_price, expbase)
        else:
            ymulti_price= math.log(yhighlim_price, expbase)
    else:
        ymulti_price= (yhighlim_price - ylowlim_price) / 100

    ymulti_vol= 3.0
    ymulti_top= 0.2
    ymulti_bot= 0.8
    
    xmulti_left= 10.0
    xmulti_right= 3.0

    xmulti_all= length + xmulti_left + xmulti_right
    xlen_fig= xmulti_all * xfactor
    ymulti_all= ymulti_price + ymulti_vol + ymulti_top + ymulti_bot
    ylen_fig= ymulti_all * yfactor

    rect_1= (xmulti_left/xmulti_all, (ymulti_bot+ymulti_vol)/ymulti_all, length/xmulti_all, ymulti_price/ymulti_all)
    rect_2= (xmulti_left/xmulti_all, ymulti_bot/ymulti_all, length/xmulti_all, ymulti_vol/ymulti_all)
    print rect_1 , rect_2

    figfacecolor= 'white'
    figedgecolor= 'black'
    figdpi= 600
    figlinewidth= 5

    figobj= pyplot.figure(figsize=(xlen_fig, ylen_fig), dpi=figdpi, facecolor=figfacecolor, edgecolor=figedgecolor, linewidth=figlinewidth) # Figure 对象


    axes_2= figobj.add_axes(rect_2, axis_bgcolor='black')
    axes_2.set_axisbelow(True)

    for child in axes_2.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_color('lightblue')

    xaxis_2= axes_2.get_xaxis()
    yaxis_2= axes_2.get_yaxis()

    xaxis_2.grid(True, 'major', color='0.3', linestyle='solid', linewidth=0.2)
    xaxis_2.grid(True, 'minor', color='0.3', linestyle='dotted', linewidth=0.1)

    yaxis_2.grid(True, 'major', color='0.3', linestyle='solid', linewidth=0.2)
    yaxis_2.grid(True, 'minor', color='0.3', linestyle='dotted', linewidth=0.1)

    xindex= numpy.arange(length)

    zipoc= zip(pdata['open'], pdata['close'])
    up= numpy.array( [ True if po < pc and po != None else False for po, pc in zipoc] )
    down= numpy.array( [ True if po > pc and po != None else False for po, pc in zipoc] )
    side= numpy.array( [ True if po == pc and po != None else False for po, pc in zipoc] )

    volume= pdata['vol']
    rarray_vol= numpy.array(volume)
    volzeros= numpy.zeros(length)

    if True in up:
        axes_2.vlines(xindex[up], volzeros[up], rarray_vol[up], color='red', linewidth=1.0, label='_nolegend_')
    if True in down:
        axes_2.vlines(xindex[down], volzeros[down], rarray_vol[down], color='green', linewidth=1.0, label='_nolegend_')
    if True in side:
        axes_2.vlines(xindex[side], volzeros[side], rarray_vol[side], color='0.7', linewidth=1.0, label='_nolegend_')

    axes_2.set_xlim(-1, length)
    datelist= [ datetime.date(int(ys), int(ms), int(ds)) for ys, ms, ds in [ [str(dstr)[0:4] , str(dstr)[4:6] , str(dstr)[6:8]] for dstr in pdata['date'] ] ]
    mdindex= []
    years= set([d.year for d in datelist])

    for y in sorted(years):
        months= set([d.month for d in datelist if d.year == y])
        for m in sorted(months):
            monthday= min([dt for dt in datelist if dt.year==y and dt.month==m])
            mdindex.append(datelist.index(monthday))
            
    xMajorLocator= FixedLocator(numpy.array(mdindex))
    

    wdindex= []
    for d in datelist:
        if d.weekday() == 0: wdindex.append(datelist.index(d))
        
    xMinorLocator= FixedLocator(numpy.array(wdindex))

    def x_major_formatter_2(idx, pos=None):
        return datelist[idx].strftime('%Y-%m-%d')
    
    def x_minor_formatter_2(idx, pos=None):
        return datelist[idx].strftime('%m-%d')
    
    xMajorFormatter= FuncFormatter(x_major_formatter_2)
    xMinorFormatter= FuncFormatter(x_minor_formatter_2)
    
    xaxis_2.set_major_locator(xMajorLocator)
    xaxis_2.set_major_formatter(xMajorFormatter)

    xaxis_2.set_minor_locator(xMinorLocator)
    xaxis_2.set_minor_formatter(xMinorFormatter)

    for malabel in axes_2.get_xticklabels(minor=False):
        malabel.set_fontsize(3)
        malabel.set_horizontalalignment('right')
        malabel.set_rotation('30')

    for milabel in axes_2.get_xticklabels(minor=True):
        milabel.set_fontsize(2)
        milabel.set_horizontalalignment('right')
        milabel.set_rotation('30')

    maxvol= max(volume)
    axes_2.set_ylim(0, maxvol)

    vollen= len(str(maxvol))

    yMajorLocator_2= MultipleLocator(10**(vollen-1))
    yMinorLocator_2= MultipleLocator((10**(vollen-2))*5)

    def y_major_formatter_2(num, pos=None):
        return int(num)
    yMajorFormatter_2= FuncFormatter(y_major_formatter_2)

    yMinorFormatter_2= NullFormatter()

    yaxis_2.set_major_locator(yMajorLocator_2)
    yaxis_2.set_major_formatter(yMajorFormatter_2)

    yaxis_2.set_minor_locator(yMinorLocator_2)
    yaxis_2.set_minor_formatter(yMinorFormatter_2)

    for malab in axes_2.get_yticklabels(minor=False):
        malab.set_fontsize(3)

    for milab in axes_2.get_yticklabels(minor=True):
        milab.set_fontsize(2)

    axes_1= figobj.add_axes(rect_1, axis_bgcolor='black', sharex=axes_2)
    axes_1.set_axisbelow(True)

    if useexpo:
        axes_1.set_yscale('log', basey=expbase) # 使用对数坐标

    for child in axes_1.get_children():
        if isinstance(child, matplotlib.spines.Spine):
            child.set_color('lightblue')

    xaxis_1= axes_1.get_xaxis()
    yaxis_1= axes_1.get_yaxis()

    xaxis_1.grid(True, 'major', color='0.3', linestyle='solid', linewidth=0.2)
    xaxis_1.grid(True, 'minor', color='0.3', linestyle='dotted', linewidth=0.1)

    yaxis_1.grid(True, 'major', color='0.3', linestyle='solid', linewidth=0.2)
    yaxis_1.grid(True, 'minor', color='0.3', linestyle='dotted', linewidth=0.1)

    rarray_open= numpy.array(pdata['open'])
    rarray_close= numpy.array(pdata['close'])
    rarray_high= numpy.array(pdata['high'])
    rarray_low= numpy.array(pdata['low'])
    
    xlinewidth = 100*3.0/length
    
    if True in up:
        axes_1.vlines(xindex[up], rarray_low[up], rarray_high[up], color='red', linewidth=0.2, label='_nolegend_')
        axes_1.vlines(xindex[up], rarray_open[up], rarray_close[up], color='red', linewidth=xlinewidth, label='_nolegend_')
    if True in down:
        axes_1.vlines(xindex[down], rarray_low[down], rarray_high[down], color='green', linewidth=0.2, label='_nolegend_')
        axes_1.vlines(xindex[down], rarray_open[down], rarray_close[down], color='green', linewidth=xlinewidth, label='_nolegend_')
    if True in side:
        axes_1.vlines(xindex[side], rarray_low[side], rarray_high[side], color='0.7', linewidth=0.2, label='_nolegend_')
        axes_1.vlines(xindex[side], rarray_open[side], rarray_close[side], color='0.7', linewidth=xlinewidth, label='_nolegend_')

    #rarray_1dayave= numpy.array(pdata[u'1日权均'])
    #rarray_5dayave= numpy.array(pdata[u'5日均'])
    #rarray_30dayave= numpy.array(pdata[u'30日均'])

    #axes_1.plot(xindex, rarray_1dayave, 'o-', color='white', linewidth=0.1, markersize=0.7, markeredgecolor='white', markeredgewidth=0.1)
    #axes_1.plot(xindex, rarray_5dayave, 'o-', color='yellow', linewidth=0.1, markersize=0.7, markeredgecolor='yellow', markeredgewidth=0.1)
    #axes_1.plot(xindex, rarray_30dayave, 'o-', color='green', linewidth=0.1, markersize=0.7, markeredgecolor='green', markeredgewidth=0.1)

    axes_1.set_xlim(-1, length)

    xaxis_1.set_major_locator(xMajorLocator)
    xaxis_1.set_major_formatter(xMajorFormatter)

    xaxis_1.set_minor_locator(xMinorLocator)
    xaxis_1.set_minor_formatter(xMinorFormatter)

    for malab in axes_1.get_xticklabels(minor=False):
        malab.set_visible(False)

    for milab in axes_1.get_xticklabels(minor=True):
        milab.set_visible(False)

    axes_1.set_ylim(ylowlim_price, yhighlim_price)

    if useexpo:
        yMajorLocator_1= LogLocator(base=expbase)

        yMajorFormatter_1= NullFormatter()
        yaxis_1.set_major_locator(yMajorLocator_1)
        yaxis_1.set_major_formatter(yMajorFormatter_1)

        minorticks= range(int(ylowlim_price), int(yhighlim_price)+1, 100)

        yMinorLocator_1= FixedLocator(numpy.array(minorticks))

        def y_minor_formatter_1(num, pos=None):
            return str(num/100.0) + '0'

        yMinorFormatter_1= FuncFormatter(y_minor_formatter_1)

        yaxis_1.set_minor_locator(yMinorLocator_1)
        yaxis_1.set_minor_formatter(yMinorFormatter_1)

        for mil in axes_1.get_yticklabels(minor=True):
            mil.set_fontsize(3)

    else:
        yMajorLocator_1= MultipleLocator(100)

        def y_major_formatter_1(num, pos=None):
            return str(num/100.0) + '0'

        yMajorFormatter_1= FuncFormatter(y_major_formatter_1)

        yaxis_1.set_major_locator(yMajorLocator_1)
        yaxis_1.set_major_formatter(yMajorFormatter_1)

        for mal in axes_1.get_yticklabels(minor=False):
            mal.set_fontsize(3)
    print figlinewidth
    figobj.savefig(figpath, dpi=figdpi, facecolor=figfacecolor, edgecolor=figedgecolor, linewidth=figlinewidth)
    #figobj.show()

if __name__ == '__main__':
    Plot('', './1.jpg', useexpo=True)
