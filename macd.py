import os,sys
import logging


def readClosePrice(path):
    closeArray=[]
    try:
        with open(path) as file:
            data = file.read()
	    array = data.split('\n')
	    for i in range(0 , len(array)-1):
		cell = array[i].split(' ')
		closeArray.append(float(cell[4]))
		#print cell[4]
    except:
        logging.info('This is info message')
	
    return closeArray

def MACD(closePrice , fast , slow , mid):
    diff=dea=macd=bar = 0
    ema12= ema26=0
    
    for i in range(1 , len(closePrice)-1):
	if i == 1:
	    ema12 = closePrice[i-1] + (closePrice[i] - closePrice[i-1])*2/(fast+1)
	    ema26 = closePrice[i-1] + (closePrice[i] - closePrice[i-1])*2/(slow+1)
	else:
	    ema12 = ema12+(closePrice[i] - ema12)*2/(fast+1)
	    ema26 = ema26+(closePrice[i] - ema26)*2/(slow+1)
	diff = ema12 - ema26
	dea = 0+(diff)*2/(mid+1)
	bar = 2*(diff-dea)
	print ema12 , " " , ema26 , " " , diff , " " , dea , " " , bar
	    
	    

closePrice = readClosePrice("../KLineData/sz/002322.txt")
MACD(closePrice , 12 , 26 , 9)
    