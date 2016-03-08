import re
import urllib2
import datetime
import string
import time
import json
import os


#URL = "http://hq.sinajs.cn/list=ml_sh000001"

class THSKlineBase:
	@staticmethod
	def ParseJson(content):
		patt = re.compile(r'\{(.*)\}')
		m = patt.search(content)
		encodedjson = json.loads(content[m.start():m.end()])
		array = encodedjson['data'].split(';')
		return array

	@staticmethod
	def GetStockDataByUrl(url):
		try:
			fp = urllib2.urlopen(url, timeout=2)
			content = fp.read()
		except Exception, e:
			return ''
		return content

	@staticmethod
	def ReadStockDict(filename):
		dictarray=[]
		try:
			with open(filename , 'r') as dictfile:
				all_the_text = dictfile.read( )
				array = all_the_text.split('\r\n')
				for i in range(1 , len(array)-1):
					cell = array[i].split('\t')
					dictarray.append(cell[1])
		except:
			print 'read stock dict failed.'
			return None
		return dictarray

	@staticmethod
	def GetMarket(code):
		if code[0] == '6':
			return "sh"
		elif code[0] == '0':
			return "sz"
		elif code[0] == '3':
			return "cyb"
		else:
			print "error market"
		return ""

	#根据数据倒叙排列一下
	@staticmethod
	def FixKLineDataFile(path , writepath):     
		for fpathe,dirs,fs in os.walk(path):
			for f in fs:
				try:
					with open(os.path.join(fpathe,f)) as file_object:
						all_the_text = file_object.read( )
						array = all_the_text.split('\r\n')
					
						code = f[0:6]
						market = GetMarket(code);
						filename = writepath
						filename += market
						filename += "/"
						filename += code
						filename += ".txt"
						try:
							with open(filename, 'w') as file_object1:
								for i in xrange(len(array)-2,-1,-1):
									file_object1.write(array[i]+"\n")
						except:
							print 'open file failed.' , filename
				except:
					print 'open file failed.' , os.path.join(fpathe,f)
		
	@staticmethod	 
	def ChDir(path): 
		for fpathe,dirs,fs in os.walk(path):
			for f in fs:
				if os.path.getsize(os.path.join(fpathe,f)) == 0 :
					dictarray.append(f[0:6])	  
     

class AllYearKLine:
	def __init__(self , url):
		self.year = datetime.date.today().year
		self.fileobj = None
		self.url = url
     
	def writeAllYearKLine(self , content):
		array = THSKlineBase().ParseJson(content)
		for i in xrange(len(array)-1,-1,-1):
			cell = array[i].split(",")
			#开高低收 成交量 成交额 换手率
			KLine = cell[0] + " " + cell[1] + " " + cell[2] + " " + cell[3] + " " + cell[4] + " " + cell[5]+ " " + cell[6] + " " + cell[7]+"\n"
			self.fileobj.write(KLine)     
			
	def Traversal(self , stockdict , path):
		dictarray = THSKlineBase().ReadStockDict(stockdict)
		for code in dictarray:
			yeartmp = self.year
			bret = True 
			try:
				market = THSKlineBase().GetMarket(code);
				filename = path
				filename += market
				filename += "/"
				filename += code
				filename += ".txt"
				with open(filename, 'a') as self.fileobj:  
					while len(ret)>0:
						URL = "http://d.10jqka.com.cn/v2/line/hs_"
						URL += code
						URL += "/01/"
						URL += str(yeartmp)
						URL += ".js"
						print URL
						ret = THSKlineBase().GetStockDataByUrl(URL)
						if len(ret)>0:
							writeAllYearKLine(ret)
						yeartmp = yeartmp - 1
						time.sleep(0.1)
					
			except:
				print 'filename=[' , filename , "] error"


class OneYearKLine:
	def __init__(self , url):
		self.year = datetime.date.today().year
		self.fileobj = None
		self.url = url
	  
	def writeOneYearKLine(self , content):
		array = THSKlineBase().ParseJson(content)
		cell = array[len(array)-1].split(",")
		#开高低收 成交量 成交额 换手率
		KLine = cell[0] + " " + cell[1] + " " + cell[2] + " " + cell[3] + " " + cell[4] + " " + cell[5]+ " " + cell[6] + " " + cell[7]+"\n"
		self.fileobj.write(KLine)       

	def Traversal(self , stockdict , path):
		dictarray = THSKlineBase().ReadStockDict(stockdict)
		for code in dictarray:
			yeartmp = self.year
			market = THSKlineBase().GetMarket(code);
			filename = path
			filename += market
			filename += "/"
			filename += code
			filename += ".txt"     
			try:
				with open(filename, 'a') as self.fileobj:
					URL = self.url
					URL += code
					URL += "/01/"
					URL += str(yeartmp)
					URL += ".js"
					print URL
					ret = THSKlineBase().GetStockDataByUrl(URL)
					if len(ret)>0:
						self.writeOneYearKLine(ret)
						time.sleep(0.05)
			except:
				raise 


if __name__ == '__main__':
	yearK = OneYearKLine('http://d.10jqka.com.cn/v2/line/hs_')
	yearK.Traversal('./thefile.txt' , './KLineData-2016-3-4/')


