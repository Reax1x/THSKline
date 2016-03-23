import os,sys
import logging


def readClosePrice(path):
    closeArray=[]
    highArray=[]
    lowArray=[]
    try:
        with open(path) as file:
            data = file.read()
	    array = data.split('\n')
	    for i in range(0 , len(array)-1):
		cell = array[i].split(' ')
		closeArray.append(float(cell[4]))
		highArray.append(float(cell[2]))
		lowArray.append(float(cell[3]))
		#print cell[4]
    except:
        logging.info('read file failed.')
	
    return closeArray, highArray , lowArray

def RSV(closeArray , highArray , lowArray ,n):
    if len(closeArray) < n:
	return
    k=15.128
    d=15.128
    
    for i in range(0,len(closePrice)-n):
	rsv = ((closeArray[n+i] - min(lowArray[i:n+i]))/(max(highArray[i:n+i]) - min(lowArray[i:n+i]))*100)
	print min(lowArray[i:n+i])
	k = (2/3.0)*k+(1/3.0)*rsv
	d = (2/3.0)*d +(1/3.0)*k
	j = 3*k - 2*d
	logging.warning("rsv=%f k=%f d=%f j=%f" , rsv , k , d , j)
	
if __name__ == '__main__':
    closePrice , highPrice , lowPrice = readClosePrice("../KLineData/sz/002322.txt")
    RSV(closePrice ,highPrice,lowPrice, 3)