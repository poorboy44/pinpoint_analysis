import pandas as pd
import sys
from pymongo import MongoClient

#set up client connection
client = MongoClient()
db = client.pinpoint
result=db.result

#create empty data frame
d=pd.DataFrame()

#iterate through data and append to data frame
line_num=0
for rec in result.find():
	line_num+=1
	#if line_num>10:
	#	break
	try:
		d=d.append(rec, ignore_index=True)
	except:
		sys.stderr.write( "Error on line:{}\n".format(line_num))
		continue
d.to_csv('data.csv')

