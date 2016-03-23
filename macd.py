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
        logging.info('read file failed.')
	
    return closeArray

def EMA(lastEma , price , w):
    ema = lastEma + (price - lastEma)*2.0/(w+1)
    return round(ema , 4)

def MACD(closePrice , fast , slow , mid):
    diff=dea=macd=bar = 0
    ema12= ema26=0
    
    for i in range(1 , len(closePrice)-1):
	ema12 = EMA(closePrice[i-1] if i==1 else ema12 ,  closePrice[i], fast)
	ema26 = EMA(closePrice[i-1] if i==1 else ema26 ,  closePrice[i], slow)
	diff = round(ema12 - ema26 , 4)
	dea = round(dea+(diff-dea)*2.0/(mid+1) , 4)
	bar = round(2*(diff-dea) , 4)
	print ema12 , " " , ema26 , " " , diff , " " , dea , " " , bar
	    
	    
if __name__ == '__main__':
    closePrice = readClosePrice("../KLineData/sz/002322.txt")
    MACD(closePrice , 12 , 26 , 9)
    