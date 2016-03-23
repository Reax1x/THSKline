import os,sys
import logging
import math

def readClosePrice(path):
    closeArray=[]
    try:
        with open(path) as file:
            data = file.read()
	    array = data.split('\n')
	    for i in range(0 , len(array)-1):
		cell = array[i].split(' ')
		closeArray.append(float(cell[4]))
		logging.warning(cell[4])
    except:
        logging.info('read file failed.')
	
    return closeArray

def square(x):
    return x*x

def BOLL(closePrice , n):
    
    if len(closePrice) > n:
	for i in range(0,len(closePrice)-n):
	    print closePrice[n+i]
	    totalprice = sum(closePrice[i:n+i])
	    totalprice /= n
	    logging.warning('avg=%s' , totalprice)
	    det = round((sum([square(price-totalprice) for price in closePrice[i:n+i]])/n)**0.5 , 3)
	    upper = round(totalprice+2*det,2)
	    lower = round(totalprice-2*det,2)
	    logging.warning("up=%f mid=%f down=%f" , upper , totalprice , lower)
	    

		    
if __name__ == '__main__':
    closePrice = readClosePrice("../KLineData/sz/002322.txt")
    BOLL(closePrice , 20)